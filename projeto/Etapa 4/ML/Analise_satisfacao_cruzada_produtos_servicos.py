import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from math import sqrt
import mysql.connector
import requests
from datetime import datetime, timedelta
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# Dados de acesso ao banco de dados
user = 'admin'
password = 'Samoht123.'
host = 'banco-pucminas.cyqkssq3ycqa.us-east-2.rds.amazonaws.com'
database = 'dw_salao_de_beleza'
port = '3306'

# Conectar ao banco de dados
db_connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
cursor = db_connection.cursor()

# Query para extrair os dados necessários das tabelas do DW
query = """
SELECT a.id_cliente, a.id_servico, a.data_id, a.valor_pago
FROM fato_pagamento AS a
left JOIN d_cliente AS c ON a.id_cliente = c.id_cliente 
left JOIN d_servico AS s ON a.id_servico = s.id_servico;
"""
try:
    cursor.execute(query)
    result = cursor.fetchall()
    df_servicos = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])
finally:
    cursor.close()
    db_connection.close()

# Pré-processamento de dados
df_servicos['data_id'] = pd.to_datetime(df_servicos['data_id'])
df_servicos['dia_da_semana'] = df_servicos['data_id'].dt.dayofweek
df_servicos['dia_do_mes'] = df_servicos['data_id'].dt.day
df_servicos['mes'] = df_servicos['data_id'].dt.month
df_servicos = df_servicos.drop('data_id', axis=1)

# Normalização dos valores pagos
scaler = StandardScaler()
df_servicos['valor_pago_normalizado'] = scaler.fit_transform(df_servicos[['valor_pago']])

# Codificação One-Hot para 'id_servico'
column_transformer = ColumnTransformer([
    ('one_hot_encoder', OneHotEncoder(), ['id_servico'])
], remainder='passthrough')

X = column_transformer.fit_transform(df_servicos[['dia_da_semana', 'dia_do_mes', 'mes', 'id_servico']])
y = df_servicos['valor_pago_normalizado']

# Divisão dos dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Construção e treinamento do modelo
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Previsões
previsoes = modelo.predict(X_test)

# Avaliação do modelo
rmse = sqrt(mean_squared_error(y_test, previsoes))
print(f'RMSE: {rmse}')


# Avaliação do modelo com métricas adicionais
mae = mean_absolute_error(y_test, previsoes)
r2 = r2_score(y_test, previsoes)

print(f'RMSE: {rmse}')
print(f'MAE: {mae}')
print(f'R²: {r2}')

# Importância das variáveis
importancias = modelo.feature_importances_
print(f'Importância das Variáveis: {importancias}')

# Dados das métricas
metricas = {
    'Metrica': ['RMSE', 'MAE', 'R²'],
    'Valor': [rmse, mae, r2],
    'Explicacao': [
        'RMSE (Erro Quadrático Médio Raiz): Mede a qualidade do modelo, indicando o desvio padrão dos resíduos (erros de previsão). Quanto menor, melhor o modelo.Exemplo: É como a média da distância que suas flechas caem do centro do alvo. Um RMSE de 0.4442 significa que, em média, suas flechas caem a cerca de 0.4442 metros do ponto que você queria acertar. Quanto menor esse número, mais perto do centro suas flechas estão caindo, o que significa que suas previsões são mais precisas.',
        'MAE (Erro Absoluto Médio): Média dos erros absolutos das previsões, fornece uma ideia da magnitude dos erros sem considerar sua direção. Exemplo: É a média de quão longe suas flechas estão do centro do alvo, sem se preocupar se elas caíram para a esquerda ou para a direita, apenas o quão longe elas estão. Um MAE de 0.1207 significa que, em média, suas flechas estão a 0.1207 metros do centro.',
        'R² (Coeficiente de Determinação): Proporção da variância da variável dependente que é previsível a partir das variáveis independentes. Varia de 0 a 1, com valores mais altos indicando melhor ajuste. Exemplo: Diz o quanto o modelo que você está usando para mirar é bom em prever onde as flechas vão cair. Um R² de 0.8217 significa que 82.17% do tempo, o modelo pode prever com sucesso onde a flecha vai cair baseado em como você está mirando.'
    ]
}

# Criar DataFrame das métricas
df_metricas = pd.DataFrame(metricas)

# Dados da importância das variáveis
importancias_df = pd.DataFrame(importancias, columns=['Importancia'])
importancias_df.index.name = 'Variavel'
importancias_df.reset_index(inplace=True)
importancias_df['Variavel'] = importancias_df['Variavel'].apply(lambda x: f'Variavel_{x+1}')

# Juntar os DataFrames
df_final = pd.concat([df_metricas, importancias_df], axis=1)

# Salvar em um arquivo .csv
df_final.to_csv('./analise_modelo_satisfacao_produto_servico.csv', index=False)

# Visualização dos Resultados

plt.scatter(y_test, previsoes)
plt.xlabel('Valores Reais')
plt.ylabel('Previsões')
plt.title('Comparação entre Valores Reais e Previsões')
plt.savefig('./analise_satisfacao_produto_servico.png')
plt.show()
