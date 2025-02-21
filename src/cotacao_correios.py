from src.webbot import *
from config import *
import pandas as pd
import logging
from selenium.webdriver.support.ui import Select
from botcity.web import By

def correios_cotacao(bot):
    try:
        logging.info("Iniciando cotação dos Correios.")

        logging.info("Lendo planilha de saída.")
        planilha_saida = pd.read_excel(ARQUIVO_SAIDA)

        for index, row in planilha_saida.iterrows():

            cep_destino = str(row[9])

            if verifica_cep_valido(cep_destino) == False:
                celula_incorreta(planilha_saida, index)
                continue

            if cep_destino == "nan":
                celula_incorreta(planilha_saida, index)
                continue

            tipo_servico = str(row[5])

            if tipo_servico == "nan":
                celula_incorreta(planilha_saida, index)
                close_browser(bot)
                continue

            logging.info("Extraindo dimensões do produto.")
            dimensoes = str(row[2])

            if dimensoes == "nan":
                celula_incorreta(planilha_saida, index)
                close_browser(bot)
                continue

            peso_produto = row[3]
        
            if str(peso_produto) == "nan":
                celula_incorreta(planilha_saida, index)
                close_browser(bot)
                continue

            logging.info("Abrindo página dos Correios.")
            abrir_url(URL_CORREIOS, bot)

            logging.info(f"Processando linha {index + 1}.")            

            logging.info("Preenchendo o cep de origem e cep de destino.")
            preencher_xpath(CEP_ORIGEM, "//input[@name ='cepOrigem']", bot)  # CEP origem
            preencher_xpath(cep_destino, "//input[@name ='cepDestino']", bot)  # CEP destino

            logging.info("Selecionando tipo de serviço.")
            select_tipo_servico = Select(bot.find_element("//select[@name ='servico']", By.XPATH))

            if tipo_servico == "PAC":
                select_tipo_servico.select_by_visible_text("PAC")
            elif tipo_servico == "SEDEX":
                select_tipo_servico.select_by_visible_text("SEDEX")
            else:
                raise ValueError("Tipo de serviço incorreto.")
            
            bot.wait(1000)

            logging.info("Selecionando tipo de embalagem.")
            select_embalagem = Select(bot.find_element("//select[@name ='embalagem1']", By.XPATH))
            select_embalagem.select_by_visible_text("Outra Embalagem")

            bot.wait(1000)

            dimensoes = dimensoes.split(" x ")
            altura_produto = dimensoes[0].strip()
            largura_produto = dimensoes[1].strip()
            comprimento_produto = dimensoes[2].strip()

            peso_produto = int(peso_produto)

            logging.info("Preenchendo dimensões e peso.")
            preencher_xpath(altura_produto, "//input[@name ='Altura']", bot)    # fazer verificações de altura válida
            preencher_xpath(largura_produto, "//input[@name ='Largura']", bot)    # fazer verificações de largura válida
            preencher_xpath(comprimento_produto, "//input[@name='Comprimento']", bot)    # fazer verificações de comprimento válido

            bot.wait(1000)
            
            select_peso = Select(bot.find_element("//select[@name ='peso']", By.XPATH))
            select_peso.select_by_visible_text(str(peso_produto))

            logging.info("Clicando no botão Calcular.")
            clicar_xpath("//input[@name ='Calcular']", bot)  

            captura_resultado(bot, planilha_saida, index)

            logging.info("Salvando planilha atualizada.")
            planilha_saida.to_excel(ARQUIVO_SAIDA, index=False)

            close_browser(bot)

        logging.info("Cotação finalizada com sucesso.")
        return True

    except Exception as e:
        # error_exception()
        return False


def celula_incorreta(planilha_saida, index):
    planilha_saida.at[index, planilha_saida.columns[15]] = "N/A"
    planilha_saida.at[index, planilha_saida.columns[16]] = "N/A"
    logging.info("Salvando planilha atualizada.")
    planilha_saida.to_excel(ARQUIVO_SAIDA, index=False)
    

def verifica_cep_valido(cep):
    try:
        cep = str(cep).replace("-", "").split(".")[0]
        return len(cep) == 8 and cep.isdigit()
    except ValueError:
        # error_exception()
        return False
    
def captura_resultado(bot, planilha_saida, index):
    try:
        abas = bot.driver.window_handles
        bot.driver.switch_to.window(abas[-1])

        bot.wait(500)

        logging.info("Capturando valores de prazo de entrega e custo.")
        entrega_prazo = capturar_xpath("/html[1]/body[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/table[1]/tbody[1]/tr[2]/td[1]", bot)
        valor_total = capturar_cssselector("tfoot td", bot)

        logging.info("Registrando valores na planilha.")
        planilha_saida.at[index, planilha_saida.columns[15]] = valor_total
        planilha_saida.at[index, planilha_saida.columns[16]] = entrega_prazo

    except Exception as e:
        print(e)
        # error_exception()
        return False