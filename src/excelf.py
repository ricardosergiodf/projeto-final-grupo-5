import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from config import *

def pintar_menor_cotacao():
    # Carregar os dados em um DataFrame
    df = pd.read_excel(ARQUIVO_SAIDA)

    # Carregar o arquivo Excel
    wb = load_workbook(ARQUIVO_SAIDA)
    ws = wb.active

    # Definir a cor de preenchimento verde
    fill_green = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')

 # Encontrar as colunas pelo nome
    coluna_jadlog = df.columns.get_loc('VALOR COTAÇÃO JADLOG') + 1
    coluna_correios = df.columns.get_loc('VALOR COTAÇÃO CORREIOS') + 1



# Iterar sobre as linhas e aplicar a formatação ao valor mais barato
    for row in range(2, len(df) + 2):  # A primeira linha é o cabeçalho, então começamos na linha 2
        cotacao_jadlog = ws.cell(row=row, column=coluna_jadlog).value
        cotacao_correios = ws.cell(row=row, column=coluna_correios).value

        # Verificar se os valores são números e diferentes de "-"
        try:
            cotacao_jadlog = float(cotacao_jadlog) if cotacao_jadlog != "-" else None
        except ValueError:
            cotacao_jadlog = None
        
        try:
            cotacao_correios = float(cotacao_correios) if cotacao_correios != "-" else None
        except ValueError:
            cotacao_correios = None

        # Aplicar a cor verde ao valor mais barato ou ao valor válido
        if cotacao_jadlog is not None and cotacao_correios is not None:
            if cotacao_jadlog < cotacao_correios:
                ws.cell(row=row, column=coluna_jadlog).fill = fill_green
            else:
                ws.cell(row=row, column=coluna_correios).fill = fill_green
        elif cotacao_jadlog is None and cotacao_correios is not None:
            ws.cell(row=row, column=coluna_correios).fill = fill_green
        elif cotacao_correios is None and cotacao_jadlog is not None:
            ws.cell(row=row, column=coluna_jadlog).fill = fill_green

    # Salvar as alterações no arquivo Excel
    wb.save(ARQUIVO_SAIDA)