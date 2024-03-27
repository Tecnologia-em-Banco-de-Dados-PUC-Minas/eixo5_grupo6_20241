Componentes de Arquitetura

Modelagem: SQL Relacional - MySQL SGBD: MySQL
Plataforma e serviços de nuvem: AWS 
Frameworks: Api Rest e Open Weather Linguagem de programação: 
Python Ferramenta de banco de dados: Dbeaver IDE: Visual Studio Code


	Segurança dos Dados e LGPD

	Ocultação de Dados Reais dos Clientes do Salão Parceiro
 
Segurança de Dados:
O projeto de Meteorologia prioriza a segurança dos dados coletados e armazenados. As medidas tomadas para garantir a segurança incluem:
•	Uso de protocolos seguros: 
o	HTTPS para comunicação com a API de meteorologia.
o	SSH para acesso ao banco de dados RDS.
•	Criptografia de dados: 
o	Senhas armazenadas em formato criptografado.
o	Banco de dados RDS criptografado em repouso e em trânsito.
•	Controle de acesso: 
o	Permissões granulares para acesso ao banco de dados e aos dados coletados.
o	Autenticação de usuários com senhas fortes e chaves SSH.
•	Monitoramento e registro: 
o	Monitoramento da atividade do sistema para detectar e prevenir acessos não autorizados.
o	Registro de todas as atividades do sistema para fins de auditoria.

Importância da Privacidade:
No projeto de Meteorologia, a privacidade dos clientes do salão parceiro é de suma importância. Para garantir a confidencialidade das informações, os dados reais dos clientes foram ocultados durante todo o processo de análise.


Processo de Ocultação:
As tabelas que continham dados reais dos clientes foram tratadas para torná-las fictícias. Isso foi feito através de técnicas como:
•	Pseudonimização: 
o	Os nomes dos clientes foram substituídos por pseudônimos aleatórios.
•	Remoção de dados sensíveis: 
o	Quaisquer dados que poderiam ser usados para identificar ou contatar os clientes foram removidos.
•	Adição de ruído: 
o	Ruído aleatório foi adicionado a alguns dados para torná-los menos precisos e menos úteis para fins de identificação.
Benefícios da Ocultação:
A ocultação dos dados reais dos clientes oferece diversos benefícios, como:
•	Proteção da privacidade dos clientes: 
o	Os clientes podem ter certeza de que seus dados pessoais não serão expostos ou vazados.
•	Maior segurança: 
o	O risco de violação de dados é reduzido, pois os dados reais dos clientes não estão disponíveis.
•	Maior confiabilidade dos resultados: 
o	A ocultação dos dados reais ajuda a garantir que os resultados da análise sejam imparciais e confiáveis.

Arquitetura da Solução


Figura 1- Arquitetura da solução
![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/734d8f8d-b04d-4ea0-a7ba-f7ab578123a9)

 
Coleta do Histórico



Figura 2- Coleta do hitstórico
![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/42d225b4-bd40-4624-95ef-9a32222b3046)






Modelagem de Dados:

O projeto utilizará o esquema de banco de dados no MySQL para armazenar os dados meteorológicos, como temperatura, clima, turno. Seguindo a estrutura de Data Warehouse Star Schema.
 
Tabela dimensão d_agenda:

    data_id DATE NOT NULL PRIMARY KEY,
    dia INT DEFAULT NULL,
    UNIQUE(data_id) 


Tabela dimensão  d_clima: 

    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    temperatura_min DOUBLE DEFAULT NULL,
    temperatura_max DOUBLE DEFAULT NULL,
    temperatura_tarde DOUBLE DEFAULT NULL,
    temperatura_noite DOUBLE DEFAULT NULL,
    temperatura_manha DOUBLE DEFAULT NULL,
    dia DATE NOT NULL,
    data_atual DATE NOT NULL,
    FOREIGN KEY (dia) REFERENCES d_agenda(data_id),
    UNIQUE (dia)



 Tabela dimensão d_cliente: 

    id int unsigned not null  auto_increment,
    nome varchar(120) not null primary key,
    telefone varchar(45) default null


Tabela dimensãod_funcionario: 

    id int unsigned primary key not null auto_increment,
    nome varchar(120) not null,
    cargo varchar(64) default null,
    telefone varchar(20) default null



Tabela dimensão d_servico: 

    id int unsigned not null primary key auto_increment,
    nome varchar(120) not null,
    valor int DEFAULT 0


Tabela fato_pagamento:

    id_cliente int unsigned not null,
    data_id date not null,
    id_funcionario int unsigned not null,
    id_servico int unsigned not null,
    valor_pago float default 0,
    primary key (id_cliente, data_id, id_funcionario, id_servico),
    foreign key FK_FatoPagamento_Cliente(id_cliente)   references d_cliente(id),
    foreign key FK_FatoPagamento_Agenda(data_id) references d_agenda(data_id),
    foreign key FK_FatoPagamento_Funcionario(id_funcionario) references d_funcionario(id),
    foreign key FK_FatoPagamento_Servico(id_servico) references d_servico(id)
 
 
Figura 3 – Modelagem de dados no   Mysql 
![image](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo6_20241/assets/161390146/815772d5-103a-4e2a-a5de-fac7060b6edb)


Coleta de Dados:

O sistema de coleta de dados que obterá informações meteorológicas para as cidades especificadas a partir da API REST fornecida. Os dados serão coletados em intervalos regulares (por exemplo, a cada hora) e inseridos na tabela "d_Clima" do RDS. Assim como os dados do salão coletados pelo site https://trinks.com.br, os dados serão em .csv e incluidos nas tabelas "d_agenda", "d_cliente", "d_funcionario", "d_servico" e "f_pagamento"


Arquitetura de Coleta:


A arquitetura de coleta terá integração com a API REST fornecida. Os serviços da AWS serão utilizados para criar funções Lambda que disparem a coleta de dados em intervalos regulares apenas os dados climáticos, devido a questão de segurança e privacidade do salão parceiro Fios de Luxo os dados serão fornecidos por ele quando solicitado. A API REST fornecida será usada para obter os dados atualizados.
