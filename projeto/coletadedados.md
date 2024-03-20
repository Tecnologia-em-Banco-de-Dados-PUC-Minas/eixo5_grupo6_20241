Componentes de Arquitetura

Modelagem: SQL Relacional - MySQL SGBD: MySQL
Plataforma e serviços de nuvem: AWS Frameworks: Api Rest e Open Weather Linguagem de programação: Python Ferramenta de banco de dados: Dbeaver IDE: Visual Studio Code




Arquitetura da Solução


Figura 1- Arquitetura da solução
 
Coleta do Histórico




Figura 2- Coleta do hitstórico






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
