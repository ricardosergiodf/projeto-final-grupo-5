from config import *
from botcity.web import By

def abrir_url (url, bot_driver):
    for tentativa in range(MAX_TRY_ERRORS):
        #log (f"Abrindo navegador: tentativa {tentativa+1}")
        try:
            bot_driver.browse(url)
            #Talvez colocar um teste melhor se o site carregou corretamente
            break
        except Exception as error:
            #log (f'Tentativa {tentativa+1}; Erro ao abrir o site {url}: {error}')
            print(f'Tentativa {tentativa+1}; Erro ao abrir o site {url}: {error}')

    if tentativa >= MAX_TRY_ERRORS:
        #log (f'Nao foi possivel abrir o navegador apos o maximo de tentivas')
        raise Exception(f'Erro ao iniciar o site {url}')
   
def preencher_xpath(text, xpath_, bot_driver):
    bot_driver.find_element(xpath_, By.XPATH).send_keys(text)

def capturar_xpath(xpath_, bot_driver):
    texto = bot_driver.find_element(xpath_, By.XPATH).text
    return texto

def capturar_cssselector(cssselector_, bot_driver):
    texto = bot_driver.find_element(cssselector_, By.CSS_SELECTOR).text
    return texto

def clicar_xpath(xpath_, bot_driver):
    bot_driver.find_element(xpath_, By.XPATH).click()

def close_browser (bot_driver):
    bot_driver.stop_browser()
