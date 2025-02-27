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
from src.preencher_input import *

print("Grupo 5.")

RAISE_NOT_CONNECTED = False

def main():
    # user_logger.info("Iniciando a tarefa.") 
    # user_logger.info("Grupo 5.")
    # dev_logger.info("Grupo 5.") 
    bot = setup()
    criar_planilha_saida()
    df = preencher_com_dados_existentes()
    preencher_tabela_saida(df)
    preencher_input(bot)
    correios_cotacao(bot)
    #mandar_email("Cadastro de Clientes no Sistema Challenge e Cotação de Novos Pedidos", ARQUIVO_SAIDA)
    # dev_logger.info("Tarefa concluída com sucesso.")  
    # dev_logger.error("Ocorreu um erro ao executar a tarefa.", exc_info=True)  # Log para usuário e dev  
    
if __name__ == '__main__':
    main()