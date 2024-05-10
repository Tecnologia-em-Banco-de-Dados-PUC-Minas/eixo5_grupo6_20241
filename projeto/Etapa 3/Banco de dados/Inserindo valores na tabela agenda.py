import mysql.connector
from  datetime import datetime
import timedelta


# Dados de acesso ao banco de dados
user = 'admin'
password = 'Samoht123.'
host = 'banco-pucminas.cyqkssq3ycqa.us-east-2.rds.amazonaws.com'
port = '3306'

# Conectar ao banco de dados
db_connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    port=port
)
cursor = db_connection.cursor()

# Selecionando o banco de dados
use_database_query = "USE dw_salao_de_beleza;"
cursor.execute(use_database_query)
print("Acessando o banco de dados")

start_date = datetime(2023, 5, 1)
end_date = datetime(2023, 12, 14)

# Gerar e inserir as datas
current_date = start_date
while current_date <= end_date:
    insert_query = "INSERT INTO d_agenda (data_id, dia) VALUES (%s, null);"
    cursor.execute(insert_query, (current_date,))
    current_date += timedelta(days=1)

# Commit e fechar a conexão
db_connection.commit()
cursor.close()
db_connection.close()