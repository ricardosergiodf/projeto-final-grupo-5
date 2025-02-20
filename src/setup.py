from .criar_diretorios import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from botcity.web import WebBot, Browser, By

def bot_driver_setup():
    try:
        bot = WebBot()
        bot.headless = False
        bot.browser = Browser.CHROME
        bot.driver_path = ChromeDriverManager().install()

        return bot
    
    except Exception():
        # error_exception()
        return False

def setup():
    try:
        criar_diretorios()
        # setup_log()
        bot = bot_driver_setup()
        return bot
    
    except Exception:
        # error_exception()
        return None

