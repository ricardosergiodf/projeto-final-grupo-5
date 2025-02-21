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

print("Hello world!")

RAISE_NOT_CONNECTED = False

def main():
    # user_logger.info("Iniciando a tarefa.") 
    # user_logger.info("Grupo 5.")
    # dev_logger.info("Grupo 5.") 

    bot = bot_driver_setup()

    criar_diretorios()
    preencher_tabela_saida()

    correios_cotacao(bot)

    # dev_logger.info("Tarefa concluída com sucesso.")  
    # dev_logger.error("Ocorreu um erro ao executar a tarefa.", exc_info=True)  # Log para usuário e dev  
    
if __name__ == '__main__':
    main()
