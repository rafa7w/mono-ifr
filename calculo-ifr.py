# Importação das bibliotecas utilizadas
import pandas as pd
import matplotlib.pyplot as plt

# Carregamento dos dados
df = pd.read_excel('BASE-DE-DADOS.xlsx')
df = df.set_index(pd.DatetimeIndex(df['Data']))

# Visualização gráfica das informações
plt.figure(figsize=(15,5))
plt.plot(df.index, df['Fechamento'], label='Fechamento')
plt.title('Preço de Fechamento BVSP Futuro')
plt.xlabel('Data')
plt.ylabel('Preço em R$')
plt.show()

# Calcula a diferença entre Preço Atual e Preço do dia anterior
delta = df['Fechamento'].diff(1)

# Remove dados do tipo "Not a Number"
delta = delta.dropna()

# Criação das tabelas que serviram como base para calcular as médias de ganhos e as médias de perdas
up = delta.copy()
down = delta.copy()

# Inserção de 0 para valores da tabela up que são menores que 0
# Filtrando apenas valores positivos
up[ up < 0 ] = 0

# Inserção de 0 para valores da tabela down que são maiores que 0
# Filtrando apenas valores negativos
down[ down > 0 ] = 0

# Cálculo da média de GANHOS móvel para um período de 14 dias
time_period = 14
AVG_GAIN = up.rolling(window=time_period).mean()

# Cálculo da média de PERDAS móvel para um período de 14 dias
AVG_LOSS = abs(down.rolling(window=time_period).mean())

# Determinando a força relativa
FR = AVG_GAIN / AVG_LOSS

# Concluindo o cálculo do índice de força relativa
IFR = 100 - (100 / (1 + FR))

# Exporta em formato excel a tabela IFR
IFR.to_excel('RSI14.xlsx')
