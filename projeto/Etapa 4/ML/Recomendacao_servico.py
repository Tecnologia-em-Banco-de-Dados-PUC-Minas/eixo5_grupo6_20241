import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import mysql.connector
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

# Supondo que 'id_servico' seja a classe alvo e que cada cliente tenha um único 'id_servico' associado
# Se 'id_servico' não for único por cliente, você precisará ajustar essa parte
y = df_agregado.groupby('id_cliente')['id_servico'].first()  # Obter o primeiro 'id_servico' para cada cliente

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
for id_cliente in X_train.index:
    distancias, indices = modelo_knn.kneighbors(X_train.loc[[id_cliente]])
    # Serviços recomendados
    vizinhos_servicos = X.iloc[indices[0]]
    servicos_recomendados = vizinhos_servicos.sum(axis=0).sort_values(ascending=False).index.tolist()
    print(f'Serviços recomendados para o cliente {id_cliente}: {servicos_recomendados}')

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

# Visualização gráfica da frequência dos serviços recomendados
frequencias = df_recomendacoes['servicos_recomendados'].explode().value_counts()
plt.figure(figsize=(10, 6))
frequencias.plot(kind='bar')
plt.title('Frequência dos Serviços Recomendados')
plt.xlabel('ID do Serviço')
plt.ylabel('Frequência')
plt.show()
