from .criar_diretorios import *
from webdriver_manager.chrome import ChromeDriverManager
from botcity.web import WebBot, Browser

def bot_driver_setup():
    try:
        bot = WebBot()
        bot.headless = False
        bot.browser = Browser.CHROME
        bot.driver_path = ChromeDriverManager().install()

        return bot
    
    except Exception as e:
        raise Exception(f"Erro: {e}")

def setup():
    try:
        criar_diretorios()
        bot = bot_driver_setup()
        return bot
    
    except Exception as e:
        raise Exception(f"Erro ao fazer o setup do bot. {e}")

