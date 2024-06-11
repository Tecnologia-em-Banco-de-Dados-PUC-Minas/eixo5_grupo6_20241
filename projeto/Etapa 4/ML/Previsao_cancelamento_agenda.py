import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.compose import ColumnTransformer
import mysql.connector
from datetime import datetime
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
LEFT JOIN d_servico AS s ON a.id_servico = s.id_servico;
"""

try:
    cursor.execute(query)
    result = cursor.fetchall()
    df_agendamentos = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])
finally:
    cursor.close()
    db_connection.close()

# Converta 'data_id' para o tipo datetime e extraia características relevantes
df_agendamentos['data_id'] = pd.to_datetime(df_agendamentos['data_id'])
df_agendamentos['dia_da_semana'] = df_agendamentos['data_id'].dt.dayofweek
df_agendamentos['dia_do_mes'] = df_agendamentos['data_id'].dt.day
df_agendamentos['mes'] = df_agendamentos['data_id'].dt.month

# Aplicar codificação one-hot em 'id_servico'
if 'id_servico' in df_agendamentos.columns:
    column_transformer = ColumnTransformer([
        ('one_hot_encoder', OneHotEncoder(), ['id_servico'])
    ], remainder='passthrough')

    # Preparar os dados para o modelo
    X = column_transformer.fit_transform(df_agendamentos[['id_servico', 'dia_da_semana', 'dia_do_mes', 'mes']])
    y = df_agendamentos['valor_pago']

    # Dividir os dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Construir e treinar o modelo de classificação
    modelo = GradientBoostingClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Fazer previsões no conjunto de teste
    previsoes = modelo.predict(X_test)

    # Avaliar o modelo
    print("Relatório de Classificação:")
    print(classification_report(y_test, previsoes))

    # Matriz de Confusão
    print("Matriz de Confusão:")
    matriz_confusao = confusion_matrix(y_test, previsoes)
    print(matriz_confusao)

    # Acurácia
    print("Acurácia do Modelo:")
    print(accuracy_score(y_test, previsoes))
    

    # Exportar os resultados para um arquivo CSV
    df_resultados = pd.DataFrame({'Real': y_test, 'Previsão': previsoes})
    df_resultados.to_csv('./previsões_cancelamento_acuracia.csv', index=False)

    # Adicionar uma explicação sobre a acurácia ao CSV
    with open('resultados_modelo.csv', 'a') as f:
        f.write("\nAcurácia do Modelo: {:.2f}%\n".format(accuracy_score(y_test, previsoes) * 100))
        f.write("A acurácia é uma medida de quão bem o modelo faz previsões corretas. "
                "É a proporção de previsões corretas em relação ao total de previsões feitas. "
                "Neste modelo, a acurácia de aproximadamente {:.2f}% indica que, das previsões que o modelo fez, "
                "cerca de {:.2f}% estavam corretas.".format(accuracy_score(y_test, previsoes) * 100,
                                                            accuracy_score(y_test, previsoes) * 100))
    # Gerar gráficos
    plt.figure(figsize=(10, 7))
    plt.matshow(matriz_confusao, cmap='viridis', fignum=1)
    plt.title('Matriz de Confusão')
    plt.colorbar()
    plt.ylabel('Valores Reais')
    plt.xlabel('Previsões')
    plt.savefig('./previsões_cancelamento_agenda_matriz_confusao.png')
    plt.show()

    # Gráfico de barras para comparar a quantidade de previsões corretas e incorretas
    plt.figure(figsize=(10, 7))
    df_resultados['Correto'] = df_resultados['Real'] == df_resultados['Previsão']
    df_resultados['Correto'].value_counts().plot(kind='bar', color=['green', 'red'])
    plt.title('Comparação de Previsões Corretas e Incorretas')
    plt.xticks([0, 1], ['Corretas', 'Incorretas'], rotation=0)
    plt.ylabel('Quantidade')
    plt.savefig('./previsões_cancelamento_agenda_corretas_incorretas.png')
    plt.show()
else:
    print("A coluna 'id_servico' não foi encontrada no DataFrame.")
