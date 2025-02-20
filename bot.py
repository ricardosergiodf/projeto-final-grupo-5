"""
Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
"""
from botcity.maestro import *
BotMaestroSDK.RAISE_NOT_CONNECTED = False
from src.setup import *

print("Hello world!")

def main():
    bot = setup()
    bot.browse("https://www.google.com")
    return

if __name__ == '__main__':
    main()
