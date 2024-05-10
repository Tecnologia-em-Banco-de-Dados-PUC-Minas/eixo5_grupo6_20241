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