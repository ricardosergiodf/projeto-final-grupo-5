"""
Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
"""
from botcity.maestro import *
from src.setup import *
from src.cotacao_correios import *

BotMaestroSDK.RAISE_NOT_CONNECTED = False

print("Hello world!")

def main():
    bot = setup()
    correios_cotacao(bot)
    return

if __name__ == '__main__':
    main()
