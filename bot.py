"""
Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
"""
# from botcity.maestro import *
import traceback
from src.setup import *
from src.brasil_api import *
from src.criar_diretorios import *
from src.configurar_logs import user_logger, dev_logger
from src.cotacao_correios import *
from src.setup import *
from src.cotacao_jadlog import *
from src.emailf import *
from src.excelf import *
from src.utilidades import *
from src.rpa_challenge import *

RAISE_NOT_CONNECTED = False

def main():
    try:
        user_logger.info("Iniciando: Cadastro de Clientes no Sistema Challenge e Cotação de Novos Pedidos")
        user_logger.info("Grupo 5")

        bot = setup()
        criar_planilha_saida()
        df = preencher_com_dados_existentes()
        processar_brasil_api(df)
        preencher_rpa_challenge()
        cotacao_correios(bot)
        cotacao_jadlog(bot)
        finalizar_planilha()
        mandar_email("Cadastro de Clientes no Sistema Challenge e Cotação de Novos Pedidos", ARQUIVO_SAIDA)

        maestro_finalizar_sucesso()
        user_logger.info("Processo concluído com sucesso.")
        
    except Exception as error:
        try:
            dev_logger.error(traceback.format_exc())
            tarefa_atual = traceback.extract_tb(error.__traceback__)[-1].name # Utiliza do traceback para retornar o nome da funcao que gerou erro
            tarefa_atual = tarefa_atual.replace("_", " ") 
            user_logger.error(f"Ocorreu um erro durante o processo {tarefa_atual}: {error}")
            arquivo_print = capturar_tela()
            mandar_email("Cadastro de Clientes no Sistema Challenge e Cotação de Novos Pedidos", arquivo_print, False, tarefa_atual)
        except Exception as error:
            dev_logger.error(f"ERRO NO EXECPTION DO BOT.PY: {error}")
            user_logger.error(f"Ocorreu um erro durante o processo {tarefa_atual}: {error}")

if __name__ == '__main__':
    main()
