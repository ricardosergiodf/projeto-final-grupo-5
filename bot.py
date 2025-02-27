"""
Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
"""
# from botcity.maestro import *
from src.setup import *
from src.brasil_api import *
from src.criar_diretorios import *
from src.configurar_logs import user_logger, dev_logger
from src.cotacao_correios import *
from src.setup import *
from src.cotacao_jadlog import *
from src.emailf import *
from src.excelf import *
from src.capturar_tela import *
from src.preencher_input import *

print("Grupo 5.")

RAISE_NOT_CONNECTED = False

def main():
    try:
        user_logger.info("Iniciando: Cadastro de Clientes no Sistema Challenge e Cotação de Novos Pedidos") 
        user_logger.info("Grupo 5")
        bot = setup()
        criar_planilha_saida()
        df = preencher_com_dados_existentes()
        preencher_tabela_saida(df)
        preencher_input(bot)
        correios_cotacao(bot)
        cotacao_jadlog(bot)
        pintar_menor_cotacao()
        mandar_email("Cadastro de Clientes no Sistema Challenge e Cotação de Novos Pedidos", ARQUIVO_SAIDA)
        user_logger.info("Tarefa concluída com sucesso.")
    except Exception as error:
        arquivo_print = capturar_tela(bot)
        user_logger.error(f"Ocorreu um erro durante o processo: {error}")
        mandar_email("Cadastro de Clientes no Sistema Challenge e Cotação de Novos Pedidos", arquivo_print, False)

    
if __name__ == '__main__':
    main()