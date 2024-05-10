import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import requests
import mysql.connector
from datetime import datetime, timedelta

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

query = """
SELECT a.id_cliente, a.id_servico, a.data_id, a.valor_pago
FROM fato_pagamento AS a
LEFT JOIN d_cliente AS c ON a.id_cliente = c.id_cliente 
LEFT JOIN d_servico AS s ON a.id_servico = s.id_servico 
WHERE a.valor_pago IS NOT NULL;
"""

try:
    cursor.execute(query)
    result = cursor.fetchall()
    df_historico = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])
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

# Agregação dos dados
df_agregado = df_historico.groupby(['id_cliente', 'id_servico']).agg({
    'valor_pago_normalizado': 'mean',
    'id_servico': 'count'
}).rename(columns={'id_servico': 'frequencia_servico'}).reset_index()

# Matriz de serviços
df_matriz_servicos = df_agregado.pivot(index='id_cliente', columns='id_servico', values='frequencia_servico').fillna(0)

# Divisão dos dados
X_train, X_test = train_test_split(df_matriz_servicos, test_size=0.2, random_state=42)

# Modelo KNN
modelo_knn = NearestNeighbors(n_neighbors=5, algorithm='auto')
modelo_knn.fit(X_train)

# Modelo KNN
modelo_knn = NearestNeighbors(n_neighbors=5, algorithm='auto')
modelo_knn.fit(X_train)

# Recomendação para todos os clientes
for id_cliente in X_train.index:
    distancias, indices = modelo_knn.kneighbors(X_train.loc[[id_cliente]])
    # Serviços recomendados
    vizinhos_servicos = df_matriz_servicos.iloc[indices[0]]
    servicos_recomendados = vizinhos_servicos.sum(axis=0).sort_values(ascending=False).index.tolist()
    print(f'Serviços recomendados para o cliente {id_cliente}: {servicos_recomendados}')