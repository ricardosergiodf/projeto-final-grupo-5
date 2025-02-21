from botcity.core import DesktopBot
import logging
from config import *

def capturar_tela(bot: DesktopBot, PATH_PRINTS: str):
    # Tira um screenshot da tela
    try:
        bot.save_screenshot(PATH_PRINTS)
        logging.info(f"Screenshot salvo com sucesso em {PATH_PRINTS}!")
    except Exception as error:
        logging.error(f'Erro ao salvar o screenshot: {error}')
        raise Exception('Erro ao salvar o screenshot')
