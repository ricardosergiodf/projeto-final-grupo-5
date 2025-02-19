"""
Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
"""
from botcity.web import WebBot, Browser, By
from botcity.maestro import *
BotMaestroSDK.RAISE_NOT_CONNECTED = False
from src.criar_diretorios import *


def main():
    criar_diretorios()
    return

if __name__ == '__main__':
    main()
