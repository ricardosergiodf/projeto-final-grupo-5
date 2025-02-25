from botcity.web import WebBot, Browser, By
from datetime import datetime
from config import *
import pandas as pd
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from src.setup import *
from src.webbot import *

# Configuração do log para debug
#logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuração do BotCity WebBot
bot = bot_driver_setup()

def preencher_input(bot):
    try:
        logging.info("Iniciando o RPA Challenge.")
        abrir_url(URL_RPA_CHALLENGE, bot)
        # Abrindo o site
        #bot.browse(URL_RPA_CHALLENGE)
        time.sleep(3)  # Aguarda a página carregar

        logging.info("Abrindo o Excel com os dados.")
        df = pd.read_excel(r"C:\\RPA\\Processados\\cnpjs_24-02-2025_11-14-49.xlsx", dtype=str)

        total_linhas = len(df)

        print(df)

        # Esperando o botão "Start" ficar clicável
        wait = WebDriverWait(bot._driver, 10)

        # Verificação do botão start
        start_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start')]")))
        if start_btn:
            start_btn.click()
            logging.info("Botão 'Start' clicado com sucesso.")
        else:
            logging.error("Botão 'Start' não encontrado. Finalizando.")
            return
            
        time.sleep(2)  # Aguarda a página carregar

        # Contadores
        tentativa_atual = 1
        linha_atual = 2
        indice_linha = 0
        total_preenchidos = 0

        while indice_linha < total_linhas:
            for _ in range(10):
                if indice_linha >= total_linhas:
                    break

                row = df.iloc[indice_linha]
                fields = [
                    ("First Name", row['RAZÃO SOCIAL']),
                    ("Last Name", row['Status']),
                    ("Company Name", row['NOME FANTASIA']),
                    ("Role in Company", row['DESCRIÇÃO MATRIZ FILIAL']),
                    ("Address", row['ENDEREÇO']),
                    ("Email", row['E-MAIL']),
                    ("Phone Number", row['TELEFONE + DDD'])
                ]

                for label, value in fields:
                    wait.until(EC.presence_of_element_located((By.XPATH, f"//div[label[text()='{label}']]/input"))).send_keys(value)
                
                logging.info(f"{tentativa_atual}ª Tentativa: Preenchendo os campos de entrada com a linha {linha_atual}.")

                # Verificação do botão submit
                submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
                if submit_btn:
                    submit_btn.click()
                    logging.info("Botão 'Submit' clicado com sucesso.")
                else:
                    logging.error("Botão 'Submit' não encontrado. Finalizando.")
                    return

                tentativa_atual += 1
                linha_atual += 1
                indice_linha += 1
                total_preenchidos += 1

            if indice_linha >= total_linhas:
                logging.info("RPA Challenge concluído com sucesso. Finalizando...")
                break  # Sai do while

            logging.info("Limite de 10 registros atingido. Reiniciando o desafio.")
            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Reset')]")))
            reset_btn.click()
            time.sleep(2)       
            start_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start')]")))
            if start_btn:
                start_btn.click()
                logging.info("Botão 'Start' clicado com sucesso.")
            else:
                logging.error("Botão 'Start' não encontrado. Finalizando.")
    
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado: {str(e).splitlines()[0]}.")
        
    finally:
        time.sleep(5)
        logging.info("Finalizando o navegador.")
        close_browser(bot)
