# Importações necessárias
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from math import sqrt
import mysql.connector
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import acessa_banco
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

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
    df_agendamentos = acessa_banco.acessa_tabela(db_connection)
    # ... (restante do seu código de pré-processamento)
else:
    print("Não foi possível estabelecer uma conexão com o banco de dados.")

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

    # Construção e treinamento do modelo de classificação
    modelo = GradientBoostingClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Previsões
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
