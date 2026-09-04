import pandas as pd

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

def classificar_kp(valor_kp):
    if valor_kp < 4:
        return "Calmo"
    elif valor_kp < 5:
        return "Ativo"
    else:
        return "Tempestade"

tabela_diaria['Classificacao'] = tabela_diaria['KP_Maximo_Diario'].apply(classificar_kp)

with pd.ExcelWriter('resultados_kp.xlsx', engine='openpyxl') as writer:
    resumo.to_excel(writer, sheet_name='Media_Parcial', index=False)
    tabela_diaria.to_excel(writer, sheet_name='Diario', index=False)
