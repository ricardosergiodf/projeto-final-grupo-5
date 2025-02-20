from botcity.core import DesktopBot
import logging

path_prints = r"C:\RPA\Logs\Prints"
def capturar_tela(bot: DesktopBot, path_prints: str):
    # Tira um screenshot da tela
    try:
        bot.save_screenshot(path_prints)
        logging.info("Screenshot salvo com sucesso!")
    except Exception as error:
        logging.error(f'Erro ao salvar o screenshot: {error}')
        raise Exception('Erro ao salvar o screenshot')
