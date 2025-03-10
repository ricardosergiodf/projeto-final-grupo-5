'''

'''
import time
#from src import criar-diretorios

MAX_TRY_ERRORS = 3
FORMATO_DATA = time.strftime("%d-%m-%Y_%H-%M-%S")
QUEBRA_LOG = "-"*50
#URLS
URL_BRASIL_API = 'https://brasilapi.com.br/api/cnpj/v1/'
URL_RPA_CHALLENGE = 'https://www.rpachallenge.com/'
URL_CORREIOS = 'https://www2.correios.com.br/sistemas/precosPrazos/'
URL_JADLOG = 'https://www.jadlog.com.br/jadlog/simulacao'

# CEP de origem
CEP_ORIGEM = "38182-428"

#Nome arquivos
NOME_EXCEL_PROCESSAR = "tabela_inicial2.xlsx"
NOME_EXCEL_DESTINATARIOS = "emails.xlsx"
NOME_COLUNA_DESTINATARIOS = "emails"


# Paths principais
PATH_RPA = r"C:\RPA"
PATH_FALHAS = rf"{PATH_RPA}\Falhas"
PATH_PROCESSAR = rf"{PATH_RPA}\Processar"
PATH_PROCESSADOS = rf"{PATH_RPA}\Processados"
PATH_FALHAS = rf"{PATH_RPA}\Falhas"
PATH_LOGS = rf"{PATH_RPA}\Logs"
PATH_DEVLOGS = rf"{PATH_LOGS}\DevLogs"
PATH_PROCESSADOS = rf"{PATH_RPA}\Processados"
PATH_PROCESSAR = rf"{PATH_RPA}\Processar"
PATH_PRINTS = rf"{PATH_LOGS}\Prints"
PATH_DESTINATARIOS = PATH_RPA

# Path Arquivos
ARQUIVO_ENTRADA = rf"{PATH_PROCESSAR}\{NOME_EXCEL_PROCESSAR}" 
ARQUIVO_SAIDA = rf"{PATH_PROCESSADOS}\cnpjs_{FORMATO_DATA}.xlsx"
ARQUIVO_DESTINATARIOS = rf"{PATH_DESTINATARIOS}/{NOME_EXCEL_DESTINATARIOS}"

# Definição das colunas da planilha de saída
COLUNAS_SAIDA = [
    "CNPJ", "RAZÃO SOCIAL", "NOME FANTASIA", "ENDEREÇO", "CEP",
    "DESCRIÇÃO MATRIZ FILIAL", "TELEFONE + DDD", "E-MAIL",
    "VALOR DO PEDIDO", "DIMENSÕES CAIXA", "PESO DO PRODUTO",
    "TIPO DE SERVIÇO JADLOG", "TIPO DE SERVIÇO CORREIOS",
    "VALOR COTAÇÃO JADLOG", "VALOR COTAÇÃO CORREIOS",
    "PRAZO DE ENTREGA CORREIOS", "Status"
]

tarefa_atual = ""