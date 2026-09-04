import pandas as pd

tabela = pd.read_csv('dados_agosto.txt', sep=r'\s+', header=None)

indice_hora = 2
indice_minuto = 3
col_dia = tabela.iloc[:, 1]

criterio_horario = (
    ((tabela.iloc[:, indice_hora] == 14) & (tabela.iloc[:, indice_minuto] >= 16)) |
    ((tabela.iloc[:, indice_hora] > 14) & (tabela.iloc[:, indice_hora] < 18)) |
    ((tabela.iloc[:, indice_hora] == 18) & (tabela.iloc[:, indice_minuto] == 0))
)
dados_filtrados = tabela[criterio_horario]

coluna5 = tabela.iloc[:, 4]
coluna6 = tabela.iloc[:, 5]

parcial5 = dados_filtrados.iloc[:, 4]
parcial6 = dados_filtrados.iloc[:, 5]

resumo_geral = pd.DataFrame({
    'Metrica': ['Media Geral', 'Maximo Geral', 'Minimo Geral', 'Media Parcial (14h16-18h)', 'Maximo Parcial (14h16-18h)', 'Minimo Parcial (14h16-18h)'],
    'Coluna_5_AE': [coluna5.mean(), coluna5.max(), coluna5.min(), parcial5.mean(), parcial5.max(), parcial5.min()],
    'Coluna_6_SYMH': [coluna6.mean(), coluna6.max(), coluna6.min(), parcial6.mean(), parcial6.max(), parcial6.min()]
})

dias_agrupamento = tabela.groupby(col_dia)
tabela_diaria = pd.DataFrame({
    'Dia_Do_Ano': list(dias_agrupamento.groups.keys()),
    'Media_Col5': dias_agrupamento[4].mean().values,
    'Max_Col5': dias_agrupamento[4].max().values,
    'Min_Col5': dias_agrupamento[4].min().values,
    'Media_Col6': dias_agrupamento[5].mean().values,
    'Max_Col6': dias_agrupamento[5].max().values,
    'Min_Col6': dias_agrupamento[5].min().values
})

media_parcial5 = parcial5.mean()
max_parcial5 = parcial5.max()
min_parcial5 = parcial5.min()

media_parcial6 = parcial6.mean()
max_parcial6 = parcial6.max()
min_parcial6 = parcial6.min()

media5 = coluna5.mean()
max_5 = coluna5.max()
min_5 = coluna5.min()

media6 = coluna6.mean()
max_6 = coluna6.max()
min_6 = coluna6.min()

texto = f"""RESULTADOS DA ANÁLISE: 

COLUNA 5: 
Media: {media5:.2f}        Media parcial: {media_parcial5:.2f}
Maximo: {max_5}            Maximo parcial: {max_parcial5}
Minimo: {min_5}            Minimo parcial: {min_parcial5}

COLUNA 6:
Media: {media6:.2f}        Media parcial: {media_parcial6:.2f}
Maximo: {max_6}            Maximo parcial: {max_parcial6}
Minimo: {min_6}            Minimo parcial: {min_parcial6}
"""

with pd.ExcelWriter('relatorio_final_agosto.xlsx', engine='openpyxl') as writer:
    resumo_geral.to_excel(writer, sheet_name='Resumo_Geral_e_Parcial', index=False)
    tabela_diaria.to_excel(writer, sheet_name='Resumo_Diario', index=False)


with open('resultados_agosto.txt', 'w', encoding='utf-8') as arquivo_txt:
    arquivo_txt.write(texto) 

