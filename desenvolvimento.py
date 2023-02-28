# RECOMENDAÇÃO DE AMBIENTE PARA EXECUÇÃO: JUPYTER NOTEBOOK
# Importação dos módulos
import pandas as pd

# Carregamento das informações
df = pd.read_excel('BASE-DE-DADOS.xlsx')

# Definição de rotinas
def operacoes_maior_menor(dataframe, rsi):
    saida_rsi = []
    entrada_rsi = []
    flag = 1
    operacoes = 0
    entrada_vendido = 0
    saida_vendido = 0
    
    for index, value in enumerate(df['RSI14']):
        if flag == 1:
            if value >= rsi and entrada_vendido == 0:
                entrada_vendido = df['Close'][index]
                entrada_rsi.append(entrada_vendido)
                entrada_vendido = 0
                flag = -1
                continue
            else: 
                continue
        elif flag == -1:
            if value <= rsi and saida_vendido == 0:
                saida_vendido = df['Close'][index]
                saida_rsi.append(saida_vendido)
                saida_vendido = 0
                flag = 1
                continue
                
    return entrada_rsi, saida_rsi


def operacoes_menor_maior(dataframe, rsi):
    saida_rsi = []
    entrada_rsi = []
    flag = 1
    operacoes = 0
    entrada_comprado = 0
    saida_comprado = 0
    
    for index, value in enumerate(df['RSI14']):
        if flag == 1:
            if value <= rsi and entrada_comprado == 0:
                entrada_comprado = df['Close'][index]
                entrada_rsi.append(entrada_comprado)
                entrada_comprado = 0
                flag = -1
                continue
            else: 
                continue
        elif flag == -1:
            if value >= rsi and saida_comprado == 0:
                saida_comprado = df['Close'][index]
                saida_rsi.append(saida_comprado)
                saida_comprado = 0
                flag = 1
                continue
                
    return entrada_rsi, saida_rsi

# Executando as rotinas e retornando o resultado nas variáveis
# O código maior_menor vai iniciar com o valor de fechamento que primeiro se aproxima da região 70 do RSI
# O código menor_maior vai iniciar com o valor de fechamento que primeiro se aproxima da região 30 do RSI

entrada_maior_menor, saida_maior_menor = operacoes_maior_menor(df, IFR_DE_SOBRECOMPRA)
entrada_menor_maior, saida_menor_maior = operacoes_menor_maior(df, IFR_DE_SOBREVENDA)

# Verifica se toda entrada tem uma saída correspondente
len(entrada_maior_menor), len(saida_maior_menor), len(entrada_menor_maior), len(saida_menor_maior)

# Corrige o item anterior caso haja divergência para um dos datasets
entrada_maior_menor.pop()
entrada_menor_maior.pop()

# Coleta dos resultados em uma nova tabela
resultado_maior_menor = pd.DataFrame()
resultado_maior_menor['Entrada'] = entrada_maior_menor
resultado_maior_menor['Saida'] = saida_maior_menor
resultado_maior_menor['Resultado'] = resultado_maior_menor['Saida'] - resultado_maior_menor['Entrada'] 

resultado_menor_maior = pd.DataFrame()
resultado_menor_maior['Entrada'] = entrada_menor_maior
resultado_menor_maior['Saida'] = saida_menor_maior
resultado_menor_maior['Resultado'] = resultado_menor_maior['Saida'] - resultado_menor_maior['Entrada'] 

# Definição das rotinas que calculam o retorno das operações
def retorno_venda(df):
    operacoes_ganhadoras = 0
    operacoes_perdedoras = 0
    for i in range(0, len(df)):
        if df['Resultado'][i] < 0:
            operacoes_ganhadoras+=1
        else:
            operacoes_perdedoras+=1
        
    return round((operacoes_ganhadoras/len(df))*100,2)

def retorno_compra(df):
    operacoes_ganhadoras = 0
    operacoes_perdedoras = 0
    for i in range(0, len(df)):
        if df['Resultado'][i] > 0:
            operacoes_ganhadoras+=1
        else:
            operacoes_perdedoras+=1
        
    return round((operacoes_ganhadoras/len(df))*100,2)

# Retorno das operações
retorno_venda(resultado_maior_menor)
retorno_compra(resultado_menor_maior)

# Transformando para dados financeiros (coluna valor contém a quantia em reais)
# e soma dos lucros com prejuízos para verificação do saldo final
resultado_maior_menor['Valor'] = resultado_maior_menor['Resultado'] * 0.2
resultado_maior_menor['Valor'].sum()

resultado_menor_maior['Valor'] = resultado_menor_maior['Resultado'] *0.2
resultado_menor_maior['Valor'].sum()