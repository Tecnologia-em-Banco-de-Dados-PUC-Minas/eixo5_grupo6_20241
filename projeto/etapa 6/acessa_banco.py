import mysql.connector
import pandas as pd

def conectar_banco_dados(host, user, password, database, port):
    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None

def acessa_tabela(db_connection):
    cursor = db_connection.cursor()
    query = """
        SELECT a.id_cliente, a.id_servico, a.data_id, a.valor_pago
        FROM fato_pagamento AS a
        LEFT JOIN d_cliente AS c ON a.id_cliente = c.id_cliente 
        LEFT JOIN d_servico AS s ON a.id_servico = s.id_servico;
    """
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        # Certifique-se de que os nomes das colunas correspondam aos dados selecionados
        df_historico = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])
        return df_historico
    finally:
        cursor.close()


def acessa_tabela_servico(db_connection):
    cursor = db_connection.cursor()
    query = """
        SELECT a.id_cliente, s.nome AS nome_servico, a.data_id, a.valor_pago
        FROM fato_pagamento AS a
        INNER JOIN d_servico AS s ON a.id_servico = s.id_servico
        WHERE a.valor_pago IS NOT NULL;
    """

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        # Inclua a coluna nome_servico ao criar o DataFrame
        df_historico = pd.DataFrame(result, columns=['id_cliente', 'nome_servico', 'data_id', 'valor_pago'])
        return df_historico
    finally:
        cursor.close()
        db_connection.close()