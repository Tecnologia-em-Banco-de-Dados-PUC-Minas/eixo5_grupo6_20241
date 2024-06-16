import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from math import sqrt
import mysql.connector
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

# Carregar variáveis de ambiente
load_dotenv()

# Substitua os valores abaixo pelos nomes das suas variáveis de ambiente
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')
port = os.getenv('DB_PORT')

# Certifique-se de que a porta é um número inteiro
if port is not None:
    port = int(port)

# Função para conectar ao banco de dados
def conectar_banco_dados():
    # Verifique se todas as informações de conexão estão disponíveis
    if not all([host, user, password, database, port]):
        print("Informações de conexão com o banco de dados estão faltando.")
        return None
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

# Função para pré-processamento de dados
def preprocessamento(df):
    df['data_id'] = pd.to_datetime(df['data_id'])
    df['dia_da_semana'] = df['data_id'].dt.dayofweek
    df['dia_do_mes'] = df['data_id'].dt.day
    df['mes'] = df['data_id'].dt.month
    df = df.drop('data_id', axis=1)
    
    # Normalização dos valores pagos
    scaler = StandardScaler()
    df['valor_pago_normalizado'] = scaler.fit_transform(df[['valor_pago']])
    
    return df

# Função para treinamento e avaliação do modelo
def treinar_avaliar_modelo(X_train, X_test, y_train, y_test):
    # Codificação One-Hot para 'id_servico' com handle_unknown='ignore'
    column_transformer = ColumnTransformer([
        ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore'), ['id_servico'])
    ], remainder='passthrough')

    X_train_transformed = column_transformer.fit_transform(X_train)
    X_test_transformed = column_transformer.transform(X_test)
    
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train_transformed, y_train)
    
    previsoes = modelo.predict(X_test_transformed)
    
    rmse = sqrt(mean_squared_error(y_test, previsoes))
    mae = mean_absolute_error(y_test, previsoes)
    r2 = r2_score(y_test, previsoes)
    
    print(f'RMSE: {rmse}')
    print(f'MAE: {mae}')
    print(f'R²: {r2}')
    
    # Importância das variáveis
    importancias = modelo.feature_importances_
    print(f'Importância das Variáveis: {importancias}')
    
    # Dados das métricas
    metricas = {
        'Metrica': ['RMSE', 'MAE', 'R²'],
        'Valor': [rmse, mae, r2],
        'Explicacao': [
            'RMSE (Erro Quadrático Médio Raiz): Mede a qualidade do modelo, indicando o desvio padrão dos resíduos (erros de previsão). Quanto menor, melhor o modelo.',
            'MAE (Erro Absoluto Médio): Média dos erros absolutos das previsões, fornece uma ideia da magnitude dos erros sem considerar sua direção.',
            'R² (Coeficiente de Determinação): Proporção da variância da variável dependente que é previsível a partir das variáveis independentes.'
        ]
    }
    
    # Criar DataFrame das métricas
    df_metricas = pd.DataFrame(metricas)
    
    # Dados da importância das variáveis
    importancias_df = pd.DataFrame(importancias, columns=['Importancia'])
    importancias_df.index.name = 'Variavel'
    importancias_df.reset_index(inplace=True)
    importancias_df['Variavel'] = importancias_df['Variavel'].apply(lambda x: f'Variavel_{x+1}')
    
    # Juntar os DataFrames
    df_final = pd.concat([df_metricas, importancias_df], axis=1)
    
    # Salvar em um arquivo .csv
    df_final.to_csv('./analise_modelo_satisfacao_produto_servico.csv', index=False)
    
    # Visualização dos Resultados
    plt.scatter(y_test, previsoes)
    plt.xlabel('Valores Reais')
    plt.ylabel('Previsões')
    plt.title('Comparação entre Valores Reais e Previsões')
    plt.savefig('./analise_satisfacao_produto_servico.png')
    plt.show()
    
    return modelo, column_transformer

# Principal
def main():
    db_connection = conectar_banco_dados()
    if db_connection is not None:
        cursor = db_connection.cursor()
        query = """
        SELECT a.id_cliente, a.id_servico, a.data_id, a.valor_pago
        FROM fato_pagamento AS a
        JOIN d_cliente AS c ON a.id_cliente = c.id_cliente 
        JOIN d_servico AS s ON a.id_servico = s.id_servico;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        df_servicos = pd.DataFrame(result, columns=['id_cliente', 'id_servico', 'data_id', 'valor_pago'])
        cursor.close()
        db_connection.close()
        
        df_servicos = preprocessamento(df_servicos)
        X = df_servicos[['dia_da_semana', 'dia_do_mes', 'mes', 'id_servico']]
        y = df_servicos['valor_pago_normalizado']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        modelo, transformer = treinar_avaliar_modelo(X_train, X_test, y_train, y_test)
        
        
if __name__ == "__main__":
    main()
