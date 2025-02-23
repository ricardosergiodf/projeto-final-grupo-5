from src.webbot import *
from config import *
import pandas as pd
import logging
from selenium.webdriver.support.ui import Select
from botcity.web import By

def correios_cotacao(bot):
    try:
        logging.info("Iniciando cotacao dos Correios.")

        logging.info("Lendo planilha de saida.")
        planilha_saida = pd.read_excel(ARQUIVO_SAIDA)

        for index, row in planilha_saida.iterrows():
            logging.info(f"Processando linha {index + 1}.")

            cep_destino = str(row[9])
            logging.info(f"Verificando CEP destino: {cep_destino}")

            if verifica_cep_valido(cep_destino) == False:
                logging.warning(f"CEP inválido encontrado na linha {index + 1}.")
                celula_incorreta(planilha_saida, index)
                continue

            if cep_destino == "nan":
                logging.warning(f"CEP destino NaN encontrado na linha {index + 1}.")
                celula_incorreta(planilha_saida, index)
                continue

            tipo_servico = str(row[5])
            logging.info(f"Verificando tipo de serviço: {tipo_servico}")

            if tipo_servico == "nan":
                logging.warning(f"Tipo de serviço NaN na linha {index + 1}. Encerrando browser.")
                celula_incorreta(planilha_saida, index)
                close_browser(bot)
                continue

            logging.info("Extraindo dimensoes do produto.")
            dimensoes = str(row[2])

            if dimensoes == "nan":
                logging.warning(f"Dimensoes NaN na linha {index + 1}. Encerrando browser.")
                celula_incorreta(planilha_saida, index)
                close_browser(bot)
                continue

            dimensoes = dimensoes.split(" x ")
            altura_produto = dimensoes[0].strip()
            largura_produto = dimensoes[1].strip()
            comprimento_produto = dimensoes[2].strip()

            logging.info(f"Dimensoes extraidas: Altura={altura_produto}, Largura={largura_produto}, Comprimento={comprimento_produto}")

            if float(altura_produto) < 0.4:
                logging.warning(f"Altura invalida ({altura_produto}) na linha {index + 1}. Encerrando browser.")
                celula_incorreta(planilha_saida, index)
                close_browser(bot)
                continue

            if int(largura_produto) < 8:
                logging.warning(f"Largura invalida ({largura_produto}) na linha {index + 1}. Encerrando browser.")
                celula_incorreta(planilha_saida, index)
                close_browser(bot)
                continue

            if int(comprimento_produto) <= 13:
                logging.warning(f"Comprimento invalido ({comprimento_produto}) na linha {index + 1}. Encerrando browser.")
                celula_incorreta(planilha_saida, index)
                close_browser(bot)
                continue

            peso_produto = row[3]
            logging.info(f"Verificando peso do produto: {peso_produto}")

            if str(peso_produto) == "nan":
                logging.warning(f"Peso NaN encontrado na linha {index + 1}. Encerrando browser.")
                celula_incorreta(planilha_saida, index)
                close_browser(bot)
                continue

            logging.info("Abrindo página dos Correios.")
            abrir_url(URL_CORREIOS, bot)

            logging.info("Preenchendo o cep de origem e cep de destino.")
            preencher_xpath(CEP_ORIGEM, "//input[@name ='cepOrigem']", bot)
            preencher_xpath(cep_destino, "//input[@name ='cepDestino']", bot)

            logging.info("Selecionando tipo de serviço.")
            select_tipo_servico = Select(bot.find_element("//select[@name ='servico']", By.XPATH))

            if tipo_servico == "PAC":
                select_tipo_servico.select_by_visible_text("PAC")
            elif tipo_servico == "SEDEX":
                select_tipo_servico.select_by_visible_text("SEDEX")
            else:
                logging.error("Tipo de serviço incorreto.")
                raise ValueError("Tipo de serviço incorreto.")
            
            bot.wait(1000)

            logging.info("Selecionando tipo de embalagem.")
            select_embalagem = Select(bot.find_element("//select[@name ='embalagem1']", By.XPATH))
            select_embalagem.select_by_visible_text("Outra Embalagem")

            bot.wait(1000)

            if peso_produto == "0.4":
                peso_produto = float(peso_produto)
            else:
                peso_produto = int(peso_produto)

            logging.info("Preenchendo dimensoes e peso.")
            preencher_xpath(altura_produto, "//input[@name ='Altura']", bot)
            preencher_xpath(largura_produto, "//input[@name ='Largura']", bot)
            preencher_xpath(comprimento_produto, "//input[@name='Comprimento']", bot)

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
    logging.warning(f"Registrando erro na linha {index + 1}.")
    planilha_saida.at[index, planilha_saida.columns[15]] = "N/A"
    planilha_saida.at[index, planilha_saida.columns[16]] = "N/A"

    status = planilha_saida.at[index, planilha_saida.columns[17]]
    planilha_saida.at[index, planilha_saida.columns[17]] = f"{status}, Erro ao realizar a cotação Correios"

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
        logging.info(f"Capturando resultado para linha {index + 1}.")
        abas = bot.driver.window_handles
        bot.driver.switch_to.window(abas[-1])

        bot.wait(500)

        try:
            alert = bot.driver.switch_to.alert
            if alert:
                logging.warning(f"Popup de alerta detectado: {alert.text}")
                alert.accept()
                celula_incorreta(planilha_saida, index)
                return
        except:
            logging.info("Nenhum popup de alerta detectado, continuando...")

        logging.info("Capturando valores de prazo de entrega e custo.")
        entrega_prazo = capturar_xpath("/html[1]/body[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/table[1]/tbody[1]/tr[2]/td[1]", bot)
        valor_total = capturar_cssselector("tfoot td", bot)

        valor_total = valor_total.replace(",", ".")
        entrega_prazo = entrega_prazo.split("+")[1].strip()
        valor_total = valor_total.split(" ")[1].strip()

        logging.info(f"Prazo de entrega capturado: {entrega_prazo}")
        logging.info(f"Valor total capturado: {valor_total}")

        planilha_saida.at[index, planilha_saida.columns[15]] = valor_total
        planilha_saida.at[index, planilha_saida.columns[16]] = entrega_prazo
        return

    except Exception as e:
        # error_exception()
        return False
