from .criar_diretorios import *
from webdriver_manager.chrome import ChromeDriverManager
from botcity.web import WebBot, Browser

def bot_driver_setup():
    """
    Configura e retorna uma instância do bot para automação.
    """
    try:
        bot = WebBot()
        bot.headless = False
        bot.browser = Browser.CHROME
        bot.driver_path = ChromeDriverManager().install()

        return bot
    
    except Exception as e:
        raise Exception(f"Erro: {e}")

def setup():
    """
    Realiza a configuração inicial do sistema, incluindo a criação de diretórios e 
    a configuração do bot para automação.
    """
    try:
        criar_diretorios()
        bot = bot_driver_setup()
        return bot
    
    except Exception as e:
        raise Exception(f"Erro ao fazer o setup do bot. {e}")

