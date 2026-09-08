import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

tabela = pd.read_csv('valorKp.txt', sep=r'\s+', header=None)

col_dia = tabela.iloc[:, 1]
hora = 2

kp_ajustado = tabela.iloc[:, 3] / 10

criterio_hora = (tabela.iloc[:, hora] >= 2) & (tabela.iloc[:, hora] <= 5)
media_parcial = kp_ajustado[criterio_hora].mean()

resumo = pd.DataFrame({
    'Media_Das_2h_as_5h': [media_parcial]
})

dias_agrupamento = kp_ajustado.groupby(col_dia)

tabela_diaria = pd.DataFrame({
    'Dia do ano': list(dias_agrupamento.groups.keys()),
    'KP_Maximo_Diario': dias_agrupamento.max().values
})

kp_madrugada = kp_ajustado[criterio_hora]
dias_madrugada = col_dia[criterio_hora]

agrupamento = kp_madrugada.groupby(dias_madrugada)
tabela_diaria['Kp parcial (02h até 05h)'] = agrupamento.max().values

def classificar_kp(valor_kp):
    if valor_kp < 4:
        return "Calmo"
    elif valor_kp < 5:
        return "Ativo"
    else:
        return "Tempestade"

tabela_diaria['Classificacao'] = tabela_diaria['KP_Maximo_Diario'].apply(classificar_kp)

dias_calmos = tabela_diaria[tabela_diaria['Classificacao'] == 'Calmo']
dias_ativos = tabela_diaria[tabela_diaria['Classificacao'] == 'Ativo']
dias_tempestades = tabela_diaria[tabela_diaria['Classificacao'] == 'Tempestade']

#histograma calmo
plt.figure(figsize=(8, 5))
plt.hist(dias_calmos['KP_Maximo_Diario'], bins=4, range=(0, 4), color='lightblue', edgecolor='black')
plt.title('Histograma 1: Dias Calmos', fontsize=14)
plt.xlabel('Valores do KP', fontsize=12)
plt.ylabel('Quantidade de Dias', fontsize=12)
plt.savefig('hist_categoria_calmo.png', dpi=300, bbox_inches='tight')
plt.show

#histograma dias ativos
plt.figure(figsize=(8, 5))
plt.hist(dias_ativos['KP_Maximo_Diario'], bins=4, range=(0, 4), color='lightblue', edgecolor='black')
plt.title('Histograma 2: Dias ativos', fontsize=14)
plt.xlabel('Valores do KP', fontsize=12)
plt.ylabel('Quantidade de Dias', fontsize=12)
plt.savefig('hist_categoria_ativo.png', dpi=300, bbox_inches='tight')
plt.show

#histograma tempestade
plt.figure(figsize=(8, 5))
plt.hist(dias_tempestades['KP_Maximo_Diario'], bins=4, range=(0, 4), color='lightblue', edgecolor='black')
plt.title('Histograma 3: Dias de tempestade', fontsize=14)
plt.xlabel('Valores do KP', fontsize=12)
plt.ylabel('Quantidade de Dias', fontsize=12)
plt.savefig('hist_categoria_tempestade.png', dpi=300, bbox_inches='tight')
plt.show


with pd.ExcelWriter('resultados_kp.xlsx', engine='openpyxl') as writer:
    resumo.to_excel(writer, sheet_name='Media_Parcial', index=False)
    tabela_diaria.to_excel(writer, sheet_name='Diario', index=False)
