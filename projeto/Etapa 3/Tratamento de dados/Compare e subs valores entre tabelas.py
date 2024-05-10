import pandas as pd

# Carregar os arquivos CSV em dataframes do Pandas
agendamentos = pd.read_csv('agendamentos_atualizado.csv', encoding='utf-8-sig', sep=';')
clientes = pd.read_csv('servicosDoEstabelecimento.csv', encoding='utf-8-sig', sep=';')

# Iterar sobre os valores da coluna "Cliente" em agendamentos_atualizado.csv
for index, row in agendamentos.iterrows():
    cliente_agendamento = row['Serviço']
    
    # Verificar se o valor existe na coluna "Nome" em clientes.csv
    matching_client = clientes[clientes['nome'] == cliente_agendamento]
    
    # Se houver correspondência, atualizar o valor da coluna "Cliente" em agendamentos_atualizado.csv
    if not matching_client.empty:
        id_cliente = matching_client.iloc[0]['Id']
        agendamentos.at[index, 'Serviço'] = id_cliente

# Salvar o arquivo com as modificações
agendamentos.to_csv('agendamentos_atualizado_modificado.csv', index=False, sep=';')
