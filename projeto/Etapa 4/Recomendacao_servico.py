import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

# Modifique a consulta SQL para incluir o INNER JOIN com a tabela d_servico
query = """
SELECT a.id_cliente, s.nome AS nome_servico, a.data_id, a.valor_pago
FROM fato_pagamento AS a
INNER JOIN d_servico AS s ON a.id_servico = s.id_servico
WHERE a.valor_pago IS NOT NULL;
"""

try:
    cursor.execute(query)
    result = cursor.fetchall()
    # Inclua a coluna nome_servico ao criar o DataFrame
    df_historico = pd.DataFrame(result, columns=['id_cliente', 'nome_servico', 'data_id', 'valor_pago'])
finally:
    cursor.close()
    db_connection.close()

# Pré-processamento de dados
df_historico['data_id'] = pd.to_datetime(df_historico['data_id'])
df_historico['dia_da_semana'] = df_historico['data_id'].dt.dayofweek
df_historico['dia_do_mes'] = df_historico['data_id'].dt.day
df_historico['mes'] = df_historico['data_id'].dt.month
df_historico = df_historico.drop('data_id', axis=1)

# Normalização dos valores pagos
scaler = StandardScaler()
df_historico['valor_pago_normalizado'] = scaler.fit_transform(df_historico[['valor_pago']])

# Agregação dos dados usando nome_servico
df_agregado = df_historico.groupby(['id_cliente', 'nome_servico']).agg({
    'valor_pago_normalizado': 'mean',
    'nome_servico': 'count'
}).rename(columns={'nome_servico': 'frequencia_servico'}).reset_index()

# Matriz de serviços usando nome_servico
df_matriz_servicos = df_agregado.pivot(index='id_cliente', columns='nome_servico', values='frequencia_servico').fillna(0)

# Supondo que 'nome_servico' seja a classe alvo
y = df_agregado.groupby('id_cliente')['nome_servico'].first()  # Obter o primeiro 'nome_servico' para cada cliente

# Certifique-se de que o índice de 'y' corresponda ao índice de 'df_matriz_servicos'
y = y.reindex(df_matriz_servicos.index)

# Divisão dos dados
X = df_matriz_servicos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo KNN
modelo_knn = KNeighborsClassifier(n_neighbors=5)
modelo_knn.fit(X_train, y_train)

# Predição para o conjunto de teste
y_pred = modelo_knn.predict(X_test)

# Recomendação para todos os clientes
recomendacoes = []
for id_cliente in X_train.index:
    distancias, indices = modelo_knn.kneighbors(X_train.loc[[id_cliente]])
    vizinhos_servicos = X.iloc[indices[0]]
    servicos_recomendados = vizinhos_servicos.sum(axis=0).sort_values(ascending=False).index.tolist()
    recomendacoes.append((id_cliente, servicos_recomendados))

df_recomendacoes = pd.DataFrame(recomendacoes, columns=['id_cliente', 'servicos_recomendados'])
df_recomendacoes.to_csv('recomendacao_servico_cliente.csv', index=False)

# Métricas de avaliação
acuracia = accuracy_score(y_test, y_pred)
matriz_confusao = confusion_matrix(y_test, y_pred)
relatorio_classificacao = classification_report(y_test, y_pred)

print(f'Acurácia: {acuracia}')
print('Matriz de Confusão:')
print(matriz_confusao)
print('Relatório de Classificação:')
print(relatorio_classificacao)

# explicação a ser colocada no csv
explicacao_acuracia = 'A acurácia é a medida de quão frequentemente as previsões estão corretas.'
explicacao_matriz = 'A matriz de confusão mostra onde o modelo fez previsões corretas e onde errou.'

# Criando DataFrames separados
df_acuracia = pd.DataFrame({
    'Métrica': ['Acurácia'],
    'Valor': [acuracia],
    'Explicação': [explicacao_acuracia]
})

df_matriz_confusao = pd.DataFrame({
    'Matriz de Confusão': [matriz_confusao],
    'Explicação': [explicacao_matriz]
})

# Salvando os DataFrames em arquivos .csv
df_acuracia.to_csv('Recomendacao_servico_acuracia.csv', index=False)
df_matriz_confusao.to_csv('Recomendacao_servico_matriz_confusao.csv', index=False)

# Visualização gráfica da frequência dos serviços recomendados
frequencias = df_recomendacoes['servicos_recomendados'].explode().value_counts()
plt.figure(figsize=(10, 6))
frequencias.plot(kind='bar')
plt.title('Frequência dos Serviços Recomendados')
plt.xlabel('Nome do Serviço')
plt.ylabel('Frequência')
plt.savefig('./Recomendacao_servico.png')
plt.show()

# Primeiro, vamos transformar o relatório de classificação em um DataFrame
report_df = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose()

# Agora, vamos criar um gráfico de barras para visualizar as pontuações de precisão, recall e f1-score para cada classe
plt.figure(figsize=(12, 8))
sns.barplot(x=report_df.index, y=report_df['f1-score'], palette='viridis')
plt.xticks(rotation=45)
plt.title('F1-Score por Classe')
plt.xlabel('Classe')
plt.ylabel('F1-Score')
plt.tight_layout()
plt.show()

# Vamos usar o heatmap do seaborn para visualizar a matriz de confusão
plt.figure(figsize=(10, 8))
sns.heatmap(matriz_confusao, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(y_pred), yticklabels=np.unique(y_pred))
plt.title('Matriz de Confusão')
plt.xlabel('Valores Previstos')
plt.ylabel('Valores Verdadeiros')
plt.show()
