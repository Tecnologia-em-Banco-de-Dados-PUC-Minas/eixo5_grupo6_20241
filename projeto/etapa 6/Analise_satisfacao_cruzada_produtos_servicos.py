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
from dotenv import load_dotenv
import os
import acessa_banco
from sklearn.ensemble import GradientBoostingClassifier

# Agora você pode criar uma instância de GradientBoostingClassifier sem erros
modelo = GradientBoostingClassifier(n_estimators=100, random_state=42)

# Carregar variáveis de ambiente
load_dotenv()

# Substitua os valores abaixo pelos nomes das suas variáveis de ambiente
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')
port = os.getenv('DB_PORT')

# Certifique-se de que a porta é um número inteiro
if port is not None:
    port = int(port)

# Conectar ao banco de dados
db_connection = acessa_banco.conectar_banco_dados(host, user, password, database, port)

# Verificar se a conexão foi bem-sucedida
if db_connection is not None:
    # Acessar a tabela e obter o DataFrame
    df_servicos = acessa_banco.acessa_tabela(db_connection)
    # ... (restante do seu código de pré-processamento)
else:
    print("Não foi possível estabelecer uma conexão com o banco de dados.")

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
