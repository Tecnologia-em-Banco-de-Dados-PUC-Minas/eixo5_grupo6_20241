**Arquitetura de Coleta:**

A arquitetura de coleta terá integração com a API REST fornecida. Os serviços da AWS serão utilizados para criar funções Lambda que disparem a coleta de dados em intervalos regulares apenas os dados climáticos, devido a questão de segurança e privacidade do salão parceiro Fios de Luxo os dados serão fornecidos por ele quando solicitado os dados referentes as tabelas cliente, serviço, pagamento e agenda. A API REST fornecida será usada para obter os dados atualizados.

**Orquestração do pipeline de dados**

Capturando	dados	históricos	climáticos	com	Python	e	API (OpenWeather)


# Definindo a data inicial e a data final data_inicial = datetime(2023, 5, 2)
data_final = datetime(2023, 5, 31)

# Função para converter de Kelvin para Celsius def kelvin_para_celsius(temp_kelvin):
return temp_kelvin - 273.15

# Função para obter dados climáticos da API OpenWeather def obter_temperatura(data):
print("Iniciando coleta") link =
f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={latitu de}&lon={longitude}&date={data.strftime('%Y-%m-%d')}&appid={API_KEY}"
requisicao = requests.get(link) requisicao_dic = requisicao.json() temperatura_min =
kelvin_para_celsius(requisicao_dic['temperature']['min']) temperatura_max =
kelvin_para_celsius(requisicao_dic['temperature']['max']) temperatura_tarde =
kelvin_para_celsius(requisicao_dic['temperature']['afternoon']) temperatura_noite =
kelvin_para_celsius(requisicao_dic['temperature']['night']) temperatura_noite =
kelvin_para_celsius(requisicao_dic['temperature']['evening']) temperatura_manha =
kelvin_para_celsius(requisicao_dic['temperature']['morning']) return temperatura_min, temperatura_max, temperatura_tarde,
temperatura_noite, temperatura_manha

# Loop para coletar os dados para cada data while data_inicial <= data_final:
temperatura_min, temperatura_max, temperatura_tarde, temperatura_noite, temperatura_manha = obter_temperatura(data_inicial)
if temperatura_min is not None and temperatura_max is not None and temperatura_tarde is not None and temperatura_noite is not None and temperatura_manha is not None:
# Conectar ao banco de dados db_connection = mysql.connector.connect(
host=host, user=user, password=password, database=database
)
cursor = db_connection.cursor()

# Inserir os dados no banco de dados

![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/c1bd554c-5d6c-4b6b-a521-6cac39fdab85)
![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/4a442a6f-ec75-4828-87f3-205fa668a978)
![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/a7c807eb-dfa0-45b9-a5a5-ff8f5cc8aa14)
![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/89c79382-b070-4c66-a92b-cf8a096b573c)




 
 
Figura 4 – Código python




**Desenvolvimento das atividades**


A captura dos dados climáticas se inicia com a inserção da chave API que se dá através do cadastro no site, https://openweathermap.org/, após isso foi necessário fazer uma requisição HTTPS que gera um JSON como resultado da coleta dos dados climáticos. Coletados os dados o código faz uma conexão com o Banco de Dados MySQL, quando conectado ele transforma os dados JSON chaves em colunas para inserção dos valores armazenados. Assim ele retorna um “Coletando dados” quando inicia a coleta e “Dados coletados e inseridos no banco de dados com sucesso” quando a inserção no banco não retorna erro. Os dados fornecidos pelo salão parceiro como agenda, clientes, pagamento e serviço passou por um tratamento de LGPD e foi inserido dentro do banco, para compreensão e análise do tratamento das tabelas (desenvolvido em python) estão no seguinte contexto:
**[projeto/Etapa 3/Tratamento de dados](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/tree/main/projeto/Etapa%203/Tratamento%20de%20dados)**


Tabela dimensão D_clima

A tabela “d_clima” iniciou sem dados
 
 ![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/22b6df33-7d2f-41bd-a5b4-7d6df993887f)

Figura 5 - Exibição da tabela d_clima no MySQL


Executando o código em Python

![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/9e7f01ef-2bac-4a69-a031-793e5724ae6c)

Figura 6 – Teste no Visual Studio Code

![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/c5674ba6-8f86-46d6-9f10-3840d8a20f7d)

Figura 7 - Continuação dos testes no Visual Studio Code


![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/fbfd8100-fce2-4e50-912d-67a87391eabf)

Figura 8 - Inserção de novos dados no MySQL


**Acessando o ambiente RDS AWS**

Para um entedimento do processo feito em duas partes, vale ressaltar que a primeira etapa se deu pela coleta dos dados climáticos e a segunda coleta via csv. enviado pelo salão parceiro foram inseridos os dados no banco e assim tratado pela LGPD e padrão de segurança criado, acesse o banco via dbeaver.

•	pucminas.cz1qlmufl8xa.sa-east-1.rds.amazonaws.com (acesso ao bd puc minas salao fios de luxo) 
•	porta: 3306
•	nome usuario: admin	
•	senha: Samoht123.
•	DB: dw_salao_de_beleza

![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/2e0dff34-6503-457a-b5a1-d5fc4d0ae1d1)

Figura 9 - Configuração do DBeaver com o RDS da AWS 

