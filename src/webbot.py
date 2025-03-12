from config import *
from botcity.web import By
from botcity.web.util import element_as_select
from src.configurar_logs import user_logger

def abrir_url (url, bot_driver):
    """
    Tenta abrir a url, caso de erro tenta até no maximo o numero setado na config na variavel "MAXIMOS_TENTATIVAS_ERRO"
    """
    for tentativa in range(MAXIMOS_TENTATIVAS_ERRO):
        user_logger.info(f"Abrindo navegador: tentativa {tentativa+1}")
        try:
            bot_driver.browse(url)
            bot_driver.wait_for_new_page(waiting_time=10000, activate=True)
            break
        except Exception as error:
            user_logger.info(f'Apos {tentativa+1} tentativa; Erro ao abrir o site {url}: {error}')
            print(f'Tentativa {tentativa+1}; Erro ao abrir o site {url}: {error}')

    if tentativa >= MAXIMOS_TENTATIVAS_ERRO:
        user_logger.info(f'Nao foi possivel abrir o navegador apos o maximo de tentivas')
        raise Exception(f'Erro ao iniciar o site {url}')
   
def encontrar_elemento_xpath(xpath_, bot_driver):
    #Encontra o elemento pelo XPATH e retorna o mesmo
    elemento = bot_driver.find_element(xpath_, By.XPATH, waiting_time = 30000)
    return elemento

def preencher_xpath(text, xpath_, bot_driver):
    #Encontra o elemento usando o XPATH e envia o texto para o elemento
    elemento = encontrar_elemento_xpath(xpath_, bot_driver)
    elemento.send_keys(text)
   
def capturar_xpath(xpath_, bot_driver):
    #Encontra o elemento usando o XPATH e retorna o texto presente no elemento
    elemento = encontrar_elemento_xpath(xpath_, bot_driver)
    texto = elemento.text
    return texto

def capturar_cssselector(cssselector_, bot_driver):
    #Encontra o elemento usando o cssselector e envia o texto para o elemento
    texto = bot_driver.find_element(cssselector_, By.CSS_SELECTOR, waiting_time = 30000).text
    return texto

def clicar_xpath(xpath_, bot_driver):
    #Encontra o elemento usando o XPATH e clica no elemento
    elemento = encontrar_elemento_xpath(xpath_, bot_driver)
    elemento.click()

def capturar_seletor_xpath(xpath_, bot_driver):
    #Encontra o elemento usando o XPATH e retorna o seletor do elemento
    seletor = encontrar_elemento_xpath(xpath_, bot_driver)
    seletor = element_as_select(seletor)
    return seletor

def selecionar_por_texto(texto, seletor):
    #Usando o seletor do elemento, seleciona baseado no texto
    seletor.select_by_visible_text(texto)

def selecionar_por_valor(valor, seletor):
    #Usando o seletor do elemento, seleciona baseado no valor
    seletor.select_by_value(valor)

def close_browser (bot_driver):
    #Fecha o navegador
    bot_driver.stop_browser()

def clear_preencher(text, xpath, bot_driver):
    #Encontra o elemento usando o XPATH, apaga o conteudo de dentro do elemento e entao envia o texto para o elemento
    elemento = encontrar_elemento_xpath(xpath, bot_driver)
    elemento.clear()
    elemento.send_keys(text)
