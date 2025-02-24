from botcity.core import DesktopBot
from config import *
import logging
import os
import time

def capturar_tela(bot: DesktopBot):
    try:
        # Define o diretório de prints
        path_prints = os.path.join(PATH_LOGS, "Prints")

        # Gera um nome único para o arquivo
        nome_arquivo = time.strftime("%d-%m-%Y_%H-%M-%S.png")
        arquivo_print = os.path.join(path_prints, nome_arquivo)

        # Salva o screenshot
        bot.save_screenshot(arquivo_print)
        logging.info(f"Screenshot salvo com sucesso em {arquivo_print}!")

        return arquivo_print  # Retorna o caminho do print salvo

    except Exception as error:
        logging.error(f"Erro ao salvar o screenshot: {error}")
        raise Exception("Erro ao salvar o screenshot")
    
    #teste
