import mysql.connector
import pandas as pd
from datetime import datetime

# Dados de acesso ao banco de dados
user = 'admin'
password = 'Samoht123.'
host = 'banco-pucminas.cyqkssq3ycqa.us-east-2.rds.amazonaws.com'
database = 'dw_salao_de_beleza'
port = '3306'

# Conectar ao banco de dados
conn = mysql.connector.connect(user=user, password=password, host=host, database=database, port=port)
cursor = conn.cursor()
hora_coleta = datetime.now()

def preencher_tabela():
    # Carregar os dados do arquivo CSV
    dados = pd.read_csv('C:/Users/thoma/eixo5_grupo6_20241/projeto/Etapa 3/tabelas/tabela_fato.csv', delimiter=';')
    print(dados.columns)

    # Percorrer os dados do arquivo CSV e inserir na tabela
    for _, row in dados.iterrows():
        Cliente = row['id_cliente']
        Data = row['data_id']
        Profissional = row['id_funcionario']
        Serviço = row['id_servico']
        Valor = row['valor_pago']

        try:
            # Executar o comando SQL para inserir os dados na tabela
            print("Inserindo dados na tabela fato_pagamento")
            sql = "INSERT INTO fato_pagamento (id_cliente, data_id, id_funcionario, id_servico, valor_pago) VALUES (%s, %s, %s, %s, %s)"
            values = (Cliente, Data, Profissional, Serviço, Valor)
            cursor.execute(sql, values)
        except mysql.connector.Error as err:
            print(f"Erro ao inserir dados: {err}")

# Chamar a função para preencher a tabela
preencher_tabela()

# Commit das alterações e fechar a conexão com o banco de dados
conn.commit()
cursor.close()
conn.close()
print(f"Dados coletados e inseridos no banco de dados com sucesso. {hora_coleta}")
