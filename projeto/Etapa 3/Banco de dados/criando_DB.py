import mysql.connector

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

# Criando o banco de dados
create_database_query = "CREATE DATABASE IF NOT EXISTS dw_salao_de_beleza;"
cursor.execute(create_database_query)
print("Banco de dados criado com sucesso")

# Selecionando o banco de dados
use_database_query = "USE dw_salao_de_beleza;"
cursor.execute(use_database_query)
print("Acessando o banco de dados")

# Inserindo a query de criação das tabelas
insert_query_data = """
DROP TABLE IF EXISTS d_agenda;

CREATE TABLE IF NOT EXISTS d_agenda (
    data_id DATE NOT NULL PRIMARY KEY,
    dia INT DEFAULT NULL
);

DROP TABLE IF EXISTS d_clima;

CREATE TABLE IF NOT EXISTS d_clima (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    temperatura_min DOUBLE DEFAULT NULL,
    temperatura_max DOUBLE DEFAULT NULL,
    temperatura_tarde DOUBLE DEFAULT NULL,
    temperatura_noite DOUBLE DEFAULT NULL,
    temperatura_manha DOUBLE DEFAULT NULL,
    dia DATE NOT NULL,
    data_atual DATE NOT NULL,
    FOREIGN KEY (dia) REFERENCES d_agenda(data_id)
);

DROP TABLE IF EXISTS d_cliente;

CREATE TABLE IF NOT EXISTS d_cliente (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    telefone VARCHAR(45) DEFAULT NULL
);

DROP TABLE IF EXISTS d_funcionario;

CREATE TABLE IF NOT EXISTS d_funcionario (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    cargo VARCHAR(64) DEFAULT NULL,
    telefone VARCHAR(20) DEFAULT NULL
);

DROP TABLE IF EXISTS d_servico;

CREATE TABLE IF NOT EXISTS d_servico (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    valor INT DEFAULT 0
);

DROP TABLE IF EXISTS fato_pagamento;

CREATE TABLE IF NOT EXISTS fato_pagamento (
    id_cliente INT UNSIGNED NOT NULL,
    data_id DATE NOT NULL,
    id_funcionario INT UNSIGNED NOT NULL,
    id_servico INT UNSIGNED NOT NULL,
    valor_pago FLOAT DEFAULT 0,
    PRIMARY KEY (id_cliente, data_id, id_funcionario, id_servico),
    FOREIGN KEY (id_cliente) REFERENCES d_cliente(id),
    FOREIGN KEY (data_id) REFERENCES d_agenda(data_id),
    FOREIGN KEY (id_funcionario) REFERENCES d_funcionario(id),
    FOREIGN KEY (id_servico) REFERENCES d_servico(id)
);
"""

# Execute o script de criação das tabelas
cursor.execute(insert_query_data, multi=True)
print("Tabelas criadas com sucesso!")

# Faça o commit das alterações
db_connection.commit()

# Fechar o cursor e a conexão
cursor.close()
db_connection.close()
