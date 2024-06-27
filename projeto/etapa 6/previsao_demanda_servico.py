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
else:
    print("Não foi possível estabelecer uma conexão com o banco de dados.")


# Pré-processamento de dados
df_servicos['data_id'] = pd.to_datetime(df_servicos['data_id'])
df_servicos['dia_da_semana'] = df_servicos['data_id'].dt.dayofweek
df_servicos['dia_do_mes'] = df_servicos['data_id'].dt.day
df_servicos['mes'] = df_servicos['data_id'].dt.month
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

#resultados no terminal

print(rmse)
print(mae)
print(r2)

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