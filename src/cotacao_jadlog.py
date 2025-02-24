from src.webbot import *
from config import *
import pandas as pd
import logging
from selenium.webdriver.support.ui import Select
from botcity.web import By

def cotacao_jadlog(bot):
    try:
        logging.info("Iniciando cotacao JadLog.")

        logging.info("Lendo planilha de saida.")
        planilha_saida = pd.read_excel(ARQUIVO_SAIDA)

        for index, row in  planilha_saida.iterrows():
            logging.info(f"Processando linha {index + 1}.")
            

            cep_destino = str(row[9])
            logging.info(f"Verificando CEP destino: {cep_destino}")

            cep_field = capturar_xpath("//input[@id='origem']", bot)

            abrir_url(URL_JADLOG)
            
            print() 

        return True
    except Exception:
        # error_exception()
        return False