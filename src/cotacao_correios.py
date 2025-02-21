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

        logging.info("Abrindo página dos Correios.")
        abrir_url(URL_CORREIOS, bot)

        for index, row in planilha_saida.iterrows():
            logging.info(f"Processando linha {index + 1}.")

            logging.info("Preenchendo o cep de origem e cep de destino.")
            preencher_xpath(CEP_ORIGEM, "//input[@name ='cepOrigem']", bot)  # CEP origem
            preencher_xpath(row[9], "//input[@name ='cepDestino']", bot)  # CEP destino

            logging.info("Selecionando tipo de serviço.")
            select_tipo_servico = Select(bot.find_element("//select[@name ='servico']", By.XPATH))
            if row[5] == "PAC":
                select_tipo_servico.select_by_visible_text("PAC")
            elif row[5] == "SEDEX":
                select_tipo_servico.select_by_visible_text("SEDEX")
            else:
                raise ValueError("Tipo de serviço incorreto.")
            
            bot.wait(500)

            logging.info("Selecionando tipo de embalagem.")
            select_embalagem = Select(bot.find_element("//select[@name ='embalagem1']", By.XPATH))
            select_embalagem.select_by_visible_text("Outra Embalagem")

            bot.wait(500)
            
            logging.info("Extraindo dimensões do produto.")
            dimensoes = row[2].split(" x ")
            altura_produto = dimensoes[0].strip()
            largura_produto = dimensoes[1].strip()
            comprimento_produto = dimensoes[2].strip()

            peso_produto = str(row[3])

            logging.info("Preenchendo dimensões e peso.")
            preencher_xpath(altura_produto, "//input[@name ='Altura']", bot)
            preencher_xpath(largura_produto, "//input[@name ='Largura']", bot)
            preencher_xpath(comprimento_produto, "//input[@name='Comprimento']", bot)
            
            select_peso = Select(bot.find_element("//select[@name ='peso']", By.XPATH))
            select_peso.select_by_visible_text(peso_produto)

            logging.info("Clicando no botão Calcular.")
            clicar_xpath("//input[@name ='Calcular']", bot)  

            bot.wait(500)

            logging.info("Capturando valores de prazo de entrega e custo.")
            entrega_prazo = capturar_xpath("/html[1]/body[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/table[1]/tbody[1]/tr[2]/td[1]", bot)
            valor_total = capturar_cssselector("tfoot td", bot)

            logging.info("Registrando valores na planilha.")
            planilha_saida.at[index, planilha_saida.columns[15]] = valor_total
            planilha_saida.at[index, planilha_saida.columns[16]] = entrega_prazo

        logging.info("Salvando planilha atualizada.")
        planilha_saida.to_excel(ARQUIVO_SAIDA, index=False)

        logging.info("Cotação finalizada com sucesso.")
        return True

    except Exception as e:
        # error_exception()
        return False
