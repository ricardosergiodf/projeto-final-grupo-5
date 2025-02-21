"""
Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
"""
# from botcity.maestro import *
from src.setup import *
from src.configurar_logs import user_logger, dev_logger


print("Hello world!")

RAISE_NOT_CONNECTED = False

def main():
    # bot = setup()
    #configurar_log_dev()
    # bot.browse("https://www.google.com")
    # Exemplo de uso
    user_logger.info("Iniciando a tarefa.")  
    dev_logger.info("Tarefa concluída com sucesso.")  
    dev_logger.error("Ocorreu um erro ao executar a tarefa.", exc_info=True)  # Log para usuário e dev  

    user_logger.info("Bem vindo ao projeto 5.")
    dev_logger.info("Bem vindo ao projeto 5.")

    
if __name__ == '__main__':
    main()
