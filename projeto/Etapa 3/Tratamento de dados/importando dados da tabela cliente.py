import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
# Dados de acesso ao banco de dados
user = 'admin'
password = 'Samoht123.'
host = 'pucminas.cz1qlmufl8xa.sa-east-1.rds.amazonaws.com'
database = 'dw_salao_de_beleza' 
port = '3306' 

# Conectar ao banco de dados
conn = mysql.connector.connect(user=user, password=password, host=host, database=database, port=port)
cursor = conn.cursor()
hora_coleta = datetime.now()

def preencher_tabela():
    # Carregar os dados do arquivo CSV
    dados = pd.read_csv("C:/Users/thoma/OneDrive/Área de Trabalho/salao - fios de luxo/Tratamento de dados/Clientes.csv", delimiter=';')

    # Imprimir os nomes das colunas
    print(dados.columns)

    # Percorrer os dados do arquivo CSV e inserir na tabela
    for _, row in dados.iterrows():
        nome = row['Nome']
        telefone = row['Telefone']

        # Executar o comando SQL para inserir os dados na tabela
        print("inserindo dados na tabela clientes")
        sql = "INSERT INTO d_cliente (nome, telefone) VALUES (%s, %s)"
        values = (nome, telefone)
        cursor.execute(sql, values)

# Chamar a função para preencher a tabela
preencher_tabela()

# Commit das alterações e fechar a conexão com o banco de dados
conn.commit()
cursor.close()
conn.close()
print(f"Dados coletados e inseridos no banco de dados com sucesso. {hora_coleta}")
