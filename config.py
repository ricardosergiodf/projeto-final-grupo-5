'''

'''

#from src import criar-diretorios

MAX_TRY_ERRORS = 3

#URLS
URL_BRASIL_API = 'https://brasilapi.com.br/api/cnpj/v1/'
URL_RPA_CHALLENGE = 'https://www.rpachallenge.com/'
URL_CORREIOS = 'https://www2.correios.com.br/sistemas/precosPrazos/'
URL_JADLOG = 'https://www.jadlog.com.br/jadlog/simulacao'

#Nome arquivos
NOME_EXCEL_PROCESSAR = 'Planilha de Entrada Grupos.xlsx'

#PATHS
PATH_RPA = r"C:\RPA"
PATH_FALHAS = f"{PATH_RPA}\Falhas"
PATH_LOGS = rf"{PATH_RPA}\Logs"
PATH_DEVLOGS = rf"{PATH_LOGS}\DevLogs"
PATH_PROCESSADOS = rf"{PATH_RPA}\Processados"
PATH_PROCESSAR = rf"{PATH_RPA}\Processar"
PATH_PRINTS = rf"{PATH_LOGS}\Prints"
#criar planilha de saída com o nome “cnpjs_dd-mm-aaaa_hh-mm-ss”