from config import *
from botcity.web import By
from botcity.web.util import element_as_select
from src.configurar_logs import user_logger

def abrir_url (url, bot_driver):
    for tentativa in range(MAX_TRY_ERRORS):
        user_logger.info(f"Abrindo navegador: tentativa {tentativa+1}")
        try:
            bot_driver.browse(url)
            bot_driver.wait_for_new_page(waiting_time=10000, activate=True)
            break
        except Exception as error:
            user_logger.info(f'Apos {tentativa+1} tentativa; Erro ao abrir o site {url}: {error}')
            print(f'Tentativa {tentativa+1}; Erro ao abrir o site {url}: {error}')

    if tentativa >= MAX_TRY_ERRORS:
        user_logger.info(f'Nao foi possivel abrir o navegador apos o maximo de tentivas')
        raise Exception(f'Erro ao iniciar o site {url}')
   
def preencher_xpath(text, xpath_, bot_driver):
    bot_driver.find_element(xpath_, By.XPATH, waiting_time = 30000).send_keys(text)
   

def capturar_xpath(xpath_, bot_driver):
    texto = bot_driver.find_element(xpath_, By.XPATH, waiting_time = 30000).text
    return texto

def capturar_cssselector(cssselector_, bot_driver):
    texto = bot_driver.find_element(cssselector_, By.CSS_SELECTOR, waiting_time = 30000).text
    return texto

def clicar_xpath(xpath_, bot_driver):
    bot_driver.find_element(xpath_, By.XPATH, waiting_time = 30000).click()

def capturar_seletor_xpath(xpath_, bot_driver):
    seletor = bot_driver.find_element(xpath_, by=By.XPATH, waiting_time = 30000)
    seletor = element_as_select(seletor)
    return seletor

def selecionar_por_texto(texto, seletor):
    seletor.select_by_visible_text(texto)

def selecionar_por_valor(valor, seletor):
    seletor.select_by_value(valor)

def close_browser (bot_driver):
    bot_driver.stop_browser()

def clear_preencher(text, xpath, bot_driver):
    elemento = bot_driver.find_element(xpath, By.XPATH, waiting_time = 30000)
    elemento.clear()
    elemento.send_keys(text)
