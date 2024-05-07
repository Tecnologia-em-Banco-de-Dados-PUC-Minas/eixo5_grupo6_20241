# Machine Learning:

Nos scripts apresentados, foram utilizadas técnicas de regressão, classificação e sistemas de recomendação, que são pilares fundamentais do Machine Learning. A eficácia desses métodos varia conforme a complexidade dos dados e o objetivo da análise. O Random Forest é eficaz para prever valores contínuos e capturar complexidades não lineares. O Gradient Boosting Classifier é poderoso para classificação, lidando bem com dados desbalanceados. Já o Nearest Neighbors é ideal para recomendações, pois identifica padrões de consumo similares entre clientes. Cada técnica tem seu método e aplicação específica, demonstrando a versatilidade e o potencial do Machine Learning para fornecer insights valiosos e decisões baseadas em dados. Essas abordagens são fundamentais para transformar grandes volumes de dados em ações estratégicas e personalizadas, impulsionando negócios e melhorando a experiência do cliente.

# Análise de satisfação cruzada entre produto e serviço

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

#### Dados de acesso ao banco de dados
user = 'admin'
password = 'Samoht123.'
host = 'pucminas.cz1qlmufl8xa.sa-east-1.rds.amazonaws.com'
database = 'dw_salao_de_beleza'
port = '3306'

#### Conectar ao banco de dados
db_connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
cursor = db_connection.cursor()

#### Query para extrair os dados necessários das tabelas do DW
query = """
SELECT a.id_cliente, a.id_servico, a.data_id, a.valor_pago
FROM fato_agendamento AS a
JOIN d_cliente AS c ON a.id_cliente = c.id
JOIN d_servico AS s ON a.id_servico = s.id
WHERE a.valor_pago IS NOT NULL;
"""
try:
    cursor.execute(query)
    result = cursor.fetchall()
    df_servicos = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])
finally:
    cursor.close()
    db_connection.close()

#### Pré-processamento de dados
df_servicos['data_id'] = pd.to_datetime(df_servicos['data_id'])
df_servicos['dia_da_semana'] = df_servicos['data_id'].dt.dayofweek
df_servicos['dia_do_mes'] = df_servicos['data_id'].dt.day
df_servicos['mes'] = df_servicos['data_id'].dt.month
df_servicos = df_servicos.drop('data_id', axis=1)

#### Normalização dos valores pagos
scaler = StandardScaler()
df_servicos['valor_pago_normalizado'] = scaler.fit_transform(df_servicos[['valor_pago']])

#### Codificação One-Hot para 'id_servico'
column_transformer = ColumnTransformer([
    ('one_hot_encoder', OneHotEncoder(), ['id_servico'])
], remainder='passthrough')

X = column_transformer.fit_transform(df_servicos[['dia_da_semana', 'dia_do_mes', 'mes', 'id_servico']])
y = df_servicos['valor_pago_normalizado']

#### Divisão dos dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#### Construção e treinamento do modelo
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

#### Previsões
previsoes = modelo.predict(X_test)

#### Avaliação do modelo
rmse = sqrt(mean_squared_error(y_test, previsoes))
print(f'RMSE: {rmse}')


############ comentario do grupo  e analise ################





# Previsão de cancelamento na agenda


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

#### Dados de acesso ao banco de dados
user = 'admin'
password = 'Samoht123.'
host = 'pucminas.cz1qlmufl8xa.sa-east-1.rds.amazonaws.com'
database = 'dw_salao_de_beleza'
port = '3306'

#### Conectar ao banco de dados
db_connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
cursor = db_connection.cursor()

#### Query para extrair os dados necessários das tabelas do DW
query = """
SELECT a.id_cliente, a.id_servico, a.data_id, a.valor_pago
FROM fato_agendamento AS a
JOIN d_cliente AS c ON a.id_cliente = c.id
JOIN d_servico AS s ON a.id_servico = s.id
WHERE a.valor_pago IS NOT NULL;
"""

#### Execute a query e armazene o resultado em um DataFrame
cursor.execute(query)
result = cursor.fetchall()
df_agendamentos = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])

#### Feche a conexão com o banco de dados
cursor.close()
db_connection.close()

#### Agora você tem o DataFrame 'df_agendamentos' pronto para ser usado
print(df_agendamentos.head())

#### Converta 'data_id' para o tipo datetime e extraia características relevantes
df_agendamentos['data_id'] = pd.to_datetime(df_agendamentos['data_id'])
df_agendamentos['dia_da_semana'] = df_agendamentos['data_id'].dt.dayofweek
df_agendamentos['dia_do_mes'] = df_agendamentos['data_id'].dt.day
df_agendamentos['mes'] = df_agendamentos['data_id'].dt.month

#### Aplicar codificação one-hot em 'id_servico'
column_transformer = ColumnTransformer([
    ('one_hot_encoder', OneHotEncoder(), ['id_servico'])
], remainder='passthrough')

#### Normalização dos valores pagos
scaler = StandardScaler()
df_agendamentos['valor_pago_normalizado'] = scaler.fit_transform(df_agendamentos[['valor_pago']])

#### Preparar os dados para o modelo
X = column_transformer.fit_transform(df_agendamentos[['dia_da_semana', 'dia_do_mes', 'mes']])
y = df_agendamentos['valor_pago_normalizado']

#### Dividir os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#### Construir e treinar o modelo de classificação
modelo = GradientBoostingClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

#### Fazer previsões no conjunto de teste
previsoes = modelo.predict(X_test)

#### Avaliar o modelo usando relatório de classificação
relatorio = classification_report(y_test, previsoes)
print(relatorio)



############ comentario do grupo  e analise ################



# Previsão de demanda

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
import requests
import mysql.connector
from datetime import datetime, timedelta

#### Dados de acesso ao banco de dados
user = 'admin'
password = 'Samoht123.'
host = 'pucminas.cz1qlmufl8xa.sa-east-1.rds.amazonaws.com'
database = 'dw_salao_de_beleza'
port = '3306'

#### Conectar ao banco de dados
db_connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
cursor = db_connection.cursor()

#### Query para extrair os dados necessários das tabelas do DW
query = """
SELECT a.id_cliente, a.id_servico, a.data_id, a.valor_pago
FROM fato_agendamento AS a
JOIN d_cliente AS c ON a.id_cliente = c.id
JOIN d_servico AS s ON a.id_servico = s.id
WHERE a.valor_pago IS NOT NULL;
"""

#### Execute a query e armazene o resultado em um DataFrame
cursor.execute(query)
result = cursor.fetchall()
df_servicos = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])

#### Suponha que 'df_servicos' seja o seu DataFrame e já contenha 'data_id', 'id_servico' e 'valor_pago'


#### Pré-processamento de dados
#### Converta 'data_id' para o tipo datetime e extraia características relevantes
df_servicos['data_id'] = pd.to_datetime(df_servicos['data_id'])
df_servicos['dia_da_semana'] = df_servicos['data_id'].dt.dayofweek
df_servicos['dia_do_mes'] = df_servicos['data_id'].dt.day
df_servicos['mes'] = df_servicos['data_id'].dt.month

#### Agora, remova a coluna 'data_id', pois ela não será mais necessária
df_servicos = df_servicos.drop('data_id', axis=1)

#### Divida os dados em conjuntos de treinamento e teste
X = df_servicos[['dia_da_semana', 'dia_do_mes', 'mes', 'id_servico']]
y = df_servicos['valor_pago']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#### Construa e treine o modelo de regressão
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

#### Faça previsões no conjunto de teste
previsoes = modelo.predict(X_test)

#### Avalie o modelo usando o erro quadrático médio (RMSE)
rmse = sqrt(mean_squared_error(y_test, previsoes))
print(f'RMSE: {rmse}')

#### O RMSE dará uma ideia de quão bem o modelo está prevendo a demanda



############ comentario do grupo  e analise ################




# Recomendação de serviço

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import requests
import mysql.connector
from datetime import datetime, timedelta

#### Dados de acesso ao banco de dados
user = 'admin'
password = 'Samoht123.'
host = 'pucminas.cz1qlmufl8xa.sa-east-1.rds.amazonaws.com'
database = 'dw_salao_de_beleza'
port = '3306'

#### Conectar ao banco de dados
db_connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
cursor = db_connection.cursor()

#### Query para extrair os dados necessários das tabelas do DW
query = """
SELECT a.id_cliente, a.id_servico, a.data_id, a.valor_pago
FROM fato_agendamento AS a
JOIN d_cliente AS c ON a.id_cliente = c.id
JOIN d_servico AS s ON a.id_servico = s.id
WHERE a.valor_pago IS NOT NULL;
"""

try:
    cursor.execute(query)
    result = cursor.fetchall()
    df_historico = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])
finally:
    cursor.close()
    db_connection.close()

#### Pré-processamento de dados
df_historico['data_id'] = pd.to_datetime(df_historico['data_id'])
df_historico['dia_da_semana'] = df_historico['data_id'].dt.dayofweek
df_historico['dia_do_mes'] = df_historico['data_id'].dt.day
df_historico['mes'] = df_historico['data_id'].dt.month
df_historico = df_historico.drop('data_id', axis=1)

#### Normalização dos valores pagos
scaler = StandardScaler()
df_historico['valor_pago_normalizado'] = scaler.fit_transform(df_historico[['valor_pago']])

#### Agregação dos dados
df_agregado = df_historico.groupby(['id_cliente', 'id_servico']).agg({
    'valor_pago_normalizado': 'mean',
    'id_servico': 'count'
}).rename(columns={'id_servico': 'frequencia_servico'}).reset_index()

#### Matriz de serviços
df_matriz_servicos = df_agregado.pivot(index='id_cliente', columns='id_servico', values='frequencia_servico').fillna(0)

#### Divisão dos dados
X_train, X_test = train_test_split(df_matriz_servicos, test_size=0.2, random_state=42)

#### Modelo KNN
modelo_knn = NearestNeighbors(n_neighbors=5, algorithm='auto')
modelo_knn.fit(X_train)

#### Recomendação
id_cliente_especifico = 10  #### Substitua pelo ID do cliente desejado
distancias, indices = modelo_knn.kneighbors(X_train.loc[[id_cliente_especifico]])

#### Serviços recomendados
vizinhos_servicos = df_matriz_servicos.iloc[indices[0]]
servicos_recomendados = vizinhos_servicos.sum(axis=0).sort_values(ascending=False).index.tolist()

print(f'Serviços recomendados para o cliente {id_cliente_especifico}: {servicos_recomendados}')

############ comentario do grupo  e analise ################
