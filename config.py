import time
# from src import criar-diretorios

MAX_TRY_ERRORS = 3
FORMATO_DATA = time.strftime("%d-%m-%Y_%H-%M-%S")

# URLs
URL_BRASIL_API = 'https://brasilapi.com.br/api/cnpj/v1/'
URL_RPA_CHALLENGE = 'https://www.rpachallenge.com/'
URL_CORREIOS = 'https://www2.correios.com.br/sistemas/precosPrazos/'
URL_JADLOG = 'https://www.jadlog.com.br/jadlog/simulacao'

# Nome de arquivos
NOME_EXCEL_ENTRADA = 'Planilha de Entrada Grupos.xlsx'
NOME_EXCEL_SAIDA = "CNPJ"
NOME_EXCEL_PROCESSAR = "tabela_inicial2.xlsx"

# Paths principais
PATH_RPA = r"C:\RPA"
PATH_PROCESSAR = rf"{PATH_RPA}\Processar"
PATH_PROCESSADOS = rf"{PATH_RPA}\Processados"
PATH_FALHAS = rf"{PATH_RPA}\Falhas"
PATH_LOGS = rf"{PATH_RPA}\Logs"
PATH_DEVLOGS = rf"{PATH_LOGS}\DevLogs"
PATH_PRINTS = rf"{PATH_LOGS}\Prints"

# Paths de arquivos
PATH_PLANILHA_ENTRADA = rf"{PATH_PROCESSAR}\{NOME_EXCEL_ENTRADA}"
PATH_PLANILHA_SAIDA = rf"{PATH_PROCESSADOS}"
ARQUIVO_ENTRADA = rf"{PATH_PROCESSAR}\{NOME_EXCEL_PROCESSAR}" 
ARQUIVO_SAIDA = rf"{PATH_PROCESSADOS}\cnpjs_{FORMATO_DATA}.xlsx"

# CEP de origem
CEP_ORIGEM = "38182-428"

# Definição das colunas da planilha de saída
COLUNAS_SAIDA = [
    "CNPJ", "RAZÃO SOCIAL", "NOME FANTASIA", "ENDEREÇO", "CEP",
    "DESCRIÇÃO MATRIZ FILIAL", "TELEFONE + DDD", "E-MAIL",
    "VALOR DO PEDIDO", "DIMENSÕES CAIXA", "PESO DO PRODUTO",
    "TIPO DE SERVIÇO JADLOG", "TIPO DE SERVIÇO CORREIOS",
    "VALOR COTAÇÃO JADLOG", "VALOR COTAÇÃO CORREIOS",
    "PRAZO DE ENTREGA CORREIOS", "Status"
]
