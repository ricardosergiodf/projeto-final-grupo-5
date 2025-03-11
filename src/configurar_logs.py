import logging
import os
from botcity.maestro import *
from config import *
from src.criar_diretorios import *

maestro = BotMaestroSDK.from_sys_args()

criar_diretorios()

# Define o diretório onde os logs serão salvos
log_filepath = os.path.join(PATH_LOGS)
dev_log_filepath = os.path.join(PATH_DEVLOGS)

# Criando logger para o usuário
user_logger = logging.getLogger("user_logger")
user_logger.setLevel(logging.INFO)

user_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
user_handler = logging.FileHandler(os.path.join(log_filepath, f"user_log-{FORMATO_DATA}.txt"), encoding="utf-8")
user_handler.setFormatter(user_format)
user_logger.addHandler(user_handler)

# Criando logger para o desenvolvedor
dev_logger = logging.getLogger("dev_logger")
dev_logger.setLevel(logging.DEBUG)

dev_format = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
dev_handler = logging.FileHandler(os.path.join(dev_log_filepath, f"dev_log-{FORMATO_DATA}.txt"), encoding="utf-8")
dev_handler.setFormatter(dev_format)
dev_logger.addHandler(dev_handler)

def enviar_log_maestro(message):
    try: 
        logging.info(message)
        maestro.new_log_entry(activity_label="DEFAULT", values={"Message": message}) 

    except Exception as e:
        logging.error(f"Erro ao configurar log maestro.")
        raise 
