import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
import requests
import mysql.connector
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
LEFT JOIN d_cliente AS c ON a.id_cliente = c.id_cliente 
LEFT JOIN d_servico AS s ON a.id_servico = s.id_servico 
WHERE a.valor_pago IS NOT NULL;
"""

try:
    cursor.execute(query)
    result = cursor.fetchall()
    df_servicos = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])
finally:
    cursor.close()
    db_connection.close()

# Suponha que 'df_servicos' seja o seu DataFrame e já contenha 'data_id', 'id_servico' e 'valor_pago'


# Pré-processamento de dados
# Converta 'data_id' para o tipo datetime e extraia características relevantes
df_servicos['data_id'] = pd.to_datetime(df_servicos['data_id'])
df_servicos['dia_da_semana'] = df_servicos['data_id'].dt.dayofweek
df_servicos['dia_do_mes'] = df_servicos['data_id'].dt.day
df_servicos['mes'] = df_servicos['data_id'].dt.month

# Agora, remova a coluna 'data_id', pois ela não será mais necessária
df_servicos = df_servicos.drop('data_id', axis=1)

# Divida os dados em conjuntos de treinamento e teste
X = df_servicos[['dia_da_semana', 'dia_do_mes', 'mes', 'id_servico']]
y = df_servicos['valor_pago']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Construa e treine o modelo de regressão
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Faça previsões no conjunto de teste
previsoes = modelo.predict(X_test)

# Avalie o modelo usando o erro quadrático médio (RMSE)
rmse = sqrt(mean_squared_error(y_test, previsoes))
mae = mean_absolute_error(y_test, previsoes)
r2 = r2_score(y_test, previsoes)

# Exportar métricas para um arquivo CSV
df_metricas = pd.DataFrame({
    'RMSE': [rmse],
    'MAE': [mae],
    'R2': [r2]
})
df_metricas.to_csv('previsao_demanda_servico_metricas_modelo.csv', index=False)

# Importância das variáveis
importancias = modelo.feature_importances_
variaveis = ['dia_da_semana', 'dia_do_mes', 'mes', 'id_servico']
df_importancias = pd.DataFrame({
    'Variável': variaveis,
    'Importância': importancias
}).sort_values(by='Importância', ascending=False)

# Exportar importâncias para um arquivo CSV
df_importancias.to_csv('previsao_demanda_servico_importancia_variaveis.csv', index=False)

# Visualização dos resultados
plt.figure(figsize=(15, 5))

# Gráfico de valores reais vs previsões
plt.subplot(1, 3, 1)
plt.scatter(y_test, previsoes, alpha=0.5)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Valores Reais')
plt.ylabel('Previsões')
plt.title('Valores Reais vs Previsões')

# Gráfico de resíduos
plt.subplot(1, 3, 2)
residuos = y_test - previsoes
plt.scatter(previsoes, residuos, alpha=0.5)
plt.hlines(y=0, xmin=residuos.min(), xmax=residuos.max(), colors='k', linestyles='--', lw=2)
plt.xlabel('Previsões')
plt.ylabel('Resíduos')
plt.title('Gráfico de Resíduos')

# Gráfico de importância das variáveis
plt.subplot(1, 3, 3)
plt.barh(variaveis, importancias, color='skyblue')
plt.xlabel('Importância')
plt.title('Importância das Variáveis')

plt.tight_layout()
plt.savefig('previsao_demanda_servico_resultados_visualizacao.png')
plt.show()