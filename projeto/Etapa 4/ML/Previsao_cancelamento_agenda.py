import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import classification_report
import mysql.connector
from sklearn.compose import ColumnTransformer
import requests
import mysql.connector
from datetime import datetime, timedelta

import mysql.connector
import pandas as pd

# Dados de acesso ao banco de dados
user = 'admin'
password = 'Samoht123.'
host = 'pucminas.cz1qlmufl8xa.sa-east-1.rds.amazonaws.com'
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
FROM fato_agendamento AS a
JOIN d_cliente AS c ON a.id_cliente = c.id
JOIN d_servico AS s ON a.id_servico = s.id
WHERE a.valor_pago IS NOT NULL;
"""

# Execute a query e armazene o resultado em um DataFrame
cursor.execute(query)
result = cursor.fetchall()
df_agendamentos = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])

# Feche a conexão com o banco de dados
cursor.close()
db_connection.close()

# Agora você tem o DataFrame 'df_agendamentos' pronto para ser usado
print(df_agendamentos.head())

# Converta 'data_id' para o tipo datetime e extraia características relevantes
df_agendamentos['data_id'] = pd.to_datetime(df_agendamentos['data_id'])
df_agendamentos['dia_da_semana'] = df_agendamentos['data_id'].dt.dayofweek
df_agendamentos['dia_do_mes'] = df_agendamentos['data_id'].dt.day
df_agendamentos['mes'] = df_agendamentos['data_id'].dt.month

# Aplicar codificação one-hot em 'id_servico'
column_transformer = ColumnTransformer([
    ('one_hot_encoder', OneHotEncoder(), ['id_servico'])
], remainder='passthrough')

# Normalização dos valores pagos
scaler = StandardScaler()
df_agendamentos['valor_pago_normalizado'] = scaler.fit_transform(df_agendamentos[['valor_pago']])

# Preparar os dados para o modelo
X = column_transformer.fit_transform(df_agendamentos[['dia_da_semana', 'dia_do_mes', 'mes']])
y = df_agendamentos['valor_pago_normalizado']

# Dividir os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Construir e treinar o modelo de classificação
modelo = GradientBoostingClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
previsoes = modelo.predict(X_test)

# Avaliar o modelo usando relatório de classificação
relatorio = classification_report(y_test, previsoes)
print(relatorio)