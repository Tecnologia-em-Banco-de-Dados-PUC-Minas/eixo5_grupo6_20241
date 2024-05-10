import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
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

try:
    # Especifique o delimitador como ponto e vírgula
    dados = pd.read_csv('C:/Users/thoma/eixo5_grupo6_20241/projeto/Etapa 3/tabelas/servicosDoEstabelecimento.csv', delimiter=';')
    
    # Criar um dicionário para mapear nomes repetidos
    nomes_repetidos = {}

    def preencher_tabela():
        # Carregar os dados do arquivo CSV
        dados = pd.read_csv('C:/Users/thoma/eixo5_grupo6_20241/projeto/Etapa 3/tabelas/servicosDoEstabelecimento.csv',  delimiter=';')

        # Imprimir os nomes das colunas
        print(dados.columns)

        # Percorrer os dados do arquivo CSV e inserir na tabela
        for _, row in dados.iterrows():
            id = row ['id_servico']
            nome = row['nome']
            valor = row['valor']

            # Executar o comando SQL para inserir os dados na tabela
            print(f'inserindo dados na tabela serviços')
            sql = 'INSERT INTO d_servico (id_servico,nome, valor) VALUES (%s,%s, %s)'
            values = (id,nome, valor)
            cursor.execute(sql, values)
    # Chamar a função para preencher a tabela
    preencher_tabela()

except pd.errors.ParserError as e:
    with open('C:/Users/thoma/OneDrive/Área de Trabalho/salao - fios de luxo/Tratamento de dados/servicosDoEstabelecimento.csv', 'r') as file:
        lines = file.readlines()
        problematic_line = lines[4]  # Os números das linhas começam em 0, então a linha 5 está no índice 4
        print(f"Erro ao analisar o CSV: {e}\nLinha problemática: {problematic_line}")


# Commit das alterações e fechar a conexão com o banco de dados
conn.commit()
cursor.close()
conn.close()
print(f"Dados coletados e inseridos no banco de dados com sucesso.{hora_coleta}")
