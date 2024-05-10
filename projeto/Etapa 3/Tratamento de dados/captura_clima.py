import requests
import mysql.connector
from datetime import datetime, timedelta

# Dados de acesso ao banco de dados
user = 'admin'
password = 'Samoht123.'
host = 'banco-pucminas.cyqkssq3ycqa.us-east-2.rds.amazonaws.com'
database = 'dw_salao_de_beleza' 
port = '3306' 

# Chave de API OpenWeather
API_KEY = "221f164d35f7154a527c7b3146fa2129"

# Coordenadas de Salvador
latitude = -12.9704
longitude = -38.5124

# Função para converter de Kelvin para Celsius
def kelvin_para_celsius(temp_kelvin):
    return temp_kelvin - 273.15


# Função para obter dados climáticos da API OpenWeather
contador = 0
def obter_temperatura(data):
    print(f"Iniciando coleta {contador}" )
    link = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={latitude}&lon={longitude}&date={data.strftime('%Y-%m-%d')}&appid={API_KEY}"
    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    temperatura_min = kelvin_para_celsius(requisicao_dic['temperature']['min'])
    temperatura_max = kelvin_para_celsius(requisicao_dic['temperature']['max'])
    temperatura_tarde = kelvin_para_celsius(requisicao_dic['temperature']['afternoon'])
    temperatura_noite = kelvin_para_celsius(requisicao_dic['temperature']['night'])
    temperatura_noite = kelvin_para_celsius(requisicao_dic['temperature']['evening'])
    temperatura_manha = kelvin_para_celsius(requisicao_dic['temperature']['morning'])
    return temperatura_min, temperatura_max, temperatura_tarde, temperatura_noite, temperatura_manha


# Conectar ao banco de dados
db_connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
cursor = db_connection.cursor()

# Loop para coletar os dados para cada data
data_inicial = datetime(2023, 5, 2)
data_final = datetime.now()

while data_inicial <= data_final:
    temperatura_min, temperatura_max, temperatura_tarde, temperatura_noite, temperatura_manha = obter_temperatura(data_inicial)
    if temperatura_min is not None and temperatura_max is not None and temperatura_tarde is not None and temperatura_noite is not None and temperatura_manha is not None:
        # Inserir ou atualizar os dados na tabela d_agenda
        insert_query_agenda = """ 
            INSERT INTO d_agenda(data_id) 
            VALUES (%s) 
            ON DUPLICATE KEY UPDATE 
            data_id = VALUES(data_id);
        """
        data_insercao_agenda = (data_inicial.strftime('%Y-%m-%d'),)
        cursor.execute(insert_query_agenda, data_insercao_agenda)

        # Inserir ou atualizar os dados na tabela d_clima com a referência da tabela d_agenda
        insert_query_clima = """ 
            INSERT INTO d_clima (temperatura_min, temperatura_max, temperatura_tarde, temperatura_noite, temperatura_manha, dia, data_atual) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
            dia = VALUES(dia);
        """
        data_insercao_clima = (temperatura_min, temperatura_max, temperatura_tarde, temperatura_noite, temperatura_manha, data_inicial.strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d'))
        cursor.execute(insert_query_clima, data_insercao_clima)

    # Incrementar a data inicial em um dia
    data_inicial += timedelta(days=1)
    contador+=1
# Commit e fechar a conexão com o banco de dados
db_connection.commit()
cursor.close()
db_connection.close()

print("Dados coletados e inseridos no banco de dados com sucesso.")
