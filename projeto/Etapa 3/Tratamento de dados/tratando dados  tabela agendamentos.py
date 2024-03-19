import pandas as pd

## O codigo abaixo serve para qualquer coluna que eu queira trocar o nome por outro
## O codigo foi aproveitado também agendamentos na coluna Cliente, onde alterei o nome verdadeiro por um iterador de Cliente + 1
## Codigo usado em agendamentos, coluna Profissionais

try:
    # Especifique o delimitador como ponto e vírgula
    dados = pd.read_csv('C:/Users/thoma/OneDrive/Área de Trabalho/salao - fios de luxo/Tratamento de dados/Clientes.csv', delimiter=';')
    
    # Criar um dicionário para mapear nomes repetidos
    nomes_repetidos = {}
    contador = 1
    
    # Substituir os nomes na coluna "Cliente"
    for i, nome in enumerate(dados['Profissional']):
        if nome in nomes_repetidos:
            dados.at[i, 'Profissional'] = nomes_repetidos[nome]
        else:
            novo_nome = f"Profissional {contador}"
            nomes_repetidos[nome] = novo_nome
            dados.at[i, 'Profissional'] = novo_nome
            contador += 1
    
    # Salvar o arquivo CSV atualizado
    dados.to_csv('C:/Users/thoma/OneDrive/Área de Trabalho/salao - fios de luxo/Tratamento de dados/agendamentos_atualizado.csv', index=False)
    
except pd.errors.ParserError as e:
    with open('C:/Users/thoma/OneDrive/Área de Trabalho/salao - fios de luxo/Tratamento de dados/agendamentos_atualizado.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        problematic_line = lines[4]  # Os números das linhas começam em 0, então a linha 5 está no índice 4
        print(f"Erro ao analisar o CSV: {e}\nLinha problemática: {problematic_line}")
