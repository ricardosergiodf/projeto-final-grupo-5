from src.webbot import *
from config import *
import pandas as pd
from src.configurar_logs import user_logger, dev_logger
from src.setup import *

def cotacao_correios(bot):
    for tentativa in range(1, MAXIMOS_TENTATIVAS_ERRO + 1):
        bot = bot_driver_setup()
        user_logger.info(f"Tentativa {tentativa}")
        try:
            user_logger.info("Iniciando cotacao dos Correios.")

            user_logger.info("Lendo planilha de saida.")
            planilha_saida = pd.read_excel(ARQUIVO_SAIDA)

            for index, row in planilha_saida.iterrows():
                user_logger.info(QUEBRA_LOG)
                user_logger.info(f"Processando linha {index + 1}.")
                
                if not verificacoes_gerais(row, index, planilha_saida, bot):
                    continue

                cep_destino = str(row["CEP"])
                tipo_servico = str(row["TIPO DE SERVIÇO CORREIOS"])
                dimensoes = str(row["DIMENSÕES CAIXA"]).split(" x ")
                altura_produto = dimensoes[0].strip()
                largura_produto = dimensoes[1].strip()
                comprimento_produto = dimensoes[2].strip()
                peso_produto = row["PESO DO PRODUTO"]
                
                if "." in str(cep_destino):
                    cep_destino = str(cep_destino).split(".")[0]
                user_logger.info("Abrindo página dos Correios.")
                abrir_url(URL_CORREIOS, bot)

                user_logger.info("Preenchendo o cep de origem e cep de destino.")
                preencher_xpath(CEP_ORIGEM, "//input[@name ='cepOrigem']", bot)
                preencher_xpath(cep_destino, "//input[@name ='cepDestino']", bot)
                
                user_logger.info("Selecionando tipo de serviço.")
                select_tipo_servico = capturar_seletor_xpath("//select[@name ='servico']", bot)

                if tipo_servico == "PAC":
                    selecionar_por_texto("PAC", select_tipo_servico)
                elif tipo_servico == "SEDEX":
                    selecionar_por_texto("SEDEX", select_tipo_servico)
                else:
                    user_logger.error("Tipo de serviço incorreto.")
                    raise ValueError("Tipo de serviço incorreto.")
                
                bot.wait(1000)

                user_logger.info("Selecionando tipo de embalagem.")
                select_embalagem = capturar_seletor_xpath("//select[@name ='embalagem1']", bot)
                selecionar_por_texto("Outra Embalagem", select_embalagem)

                bot.wait(1000)

                if peso_produto == "0.4":
                    peso_produto = float(peso_produto)
                else:
                    peso_produto = int(peso_produto)

                user_logger.info("Preenchendo dimensões e peso.")
                preencher_xpath(altura_produto, "//input[@name ='Altura']", bot)
                preencher_xpath(largura_produto, "//input[@name ='Largura']", bot)
                preencher_xpath(comprimento_produto, "//input[@name='Comprimento']", bot)

                bot.wait(1000)
                
                select_peso = capturar_seletor_xpath("//select[@name ='peso']", bot)
                selecionar_por_texto (str(peso_produto), select_peso)

                user_logger.info("Clicando no botão Calcular.")
                clicar_xpath("//input[@name ='Calcular']", bot)  

                captura_resultado(bot, planilha_saida, index)

                user_logger.info("Salvando planilha atualizada.")
                planilha_saida.to_excel(ARQUIVO_SAIDA, index=False)

                close_browser(bot)

            user_logger.info("Cotação finalizada com sucesso.")
            user_logger.info(QUEBRA_LOG)
            return True

        except Exception as e:
            user_logger.warning(f"Ocorreu um erro durante a cotação Correios na tentativa {tentativa}.")
            dev_logger.error(f'Erro: {e} na tentativa {tentativa}')
        
    raise Exception(f"Máxima de {MAXIMOS_TENTATIVAS_ERRO} tentativas alcançada, finalizando cotação Correios...")


def celula_incorreta(planilha_saida, index):
    user_logger.warning(f"Registrando erro na linha {index + 1}.")

    planilha_saida.at[index, "VALOR COTAÇÃO CORREIOS"] = "-"
    planilha_saida.at[index, "PRAZO DE ENTREGA CORREIOS"] = "-"

    status = planilha_saida.at[index, "Status"]
    if status in ["nan", "N/A", "-", "", " "]:
        planilha_saida.at[index, "Status"] = "Erro ao realizar a cotação Correios"
    else:
        planilha_saida.at[index, "Status"] = f"{status} | Erro ao realizar a cotação Correios"

    user_logger.info("Salvando planilha atualizada.")
    planilha_saida.to_excel(ARQUIVO_SAIDA, index=False)
    
    return


def verifica_cep_valido(cep):
    try:
        cep = str(cep).replace("-", "").split(".")[0]
        return len(cep) == 8 and cep.isdigit()
    except ValueError:
        user_logger.warning("CEP Inválido.")
        return False
    

def captura_resultado(bot, planilha_saida, index):
    try:
        user_logger.info(f"Capturando resultado para linha {index + 1}.")
        abas = bot.driver.window_handles
        bot.driver.switch_to.window(abas[-1])

        bot.wait(500)

        try:
            alert = bot.driver.switch_to.alert
            if alert:
                user_logger.warning(f"Popup de alerta detectado: {alert.text}")
                alert.accept()
                celula_incorreta(planilha_saida, index)
                return
        except:
            user_logger.info("Nenhum popup de alerta detectado, continuando...")

        user_logger.info("Capturando valores de prazo de entrega e custo.")
        entrega_prazo = capturar_xpath("/html[1]/body[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/table[1]/tbody[1]/tr[2]/td[1]", bot)
        valor_total = capturar_cssselector("tfoot td", bot)

        valor_total = valor_total.replace(",", ".")
        entrega_prazo = entrega_prazo.split("+")[1].strip()
        valor_total = valor_total.split(" ")[1].strip()

        user_logger.info(f"Prazo de entrega capturado: {entrega_prazo}")
        user_logger.info(f"Valor total capturado: {valor_total}")

        planilha_saida.at[index, "VALOR COTAÇÃO CORREIOS"] = valor_total
        planilha_saida.at[index, "PRAZO DE ENTREGA CORREIOS"] = entrega_prazo
        return

    except Exception as e:
        user_logger.warning("Erro ao capturar o resultado da cotação.")
        return False


def verifica_dimensoes(tipo_servico, comprimento_produto, largura_produto, altura_produto, index):
    soma_dimensoes = comprimento_produto + largura_produto + altura_produto

    if soma_dimensoes < 21.4 or soma_dimensoes > 200:
        user_logger.warning(f"Soma das dimensoes invalida ({soma_dimensoes}) na linha {index + 1}. Encerrando browser.")
        return False
    
    if altura_produto < 0.4 or altura_produto > 100:
        user_logger.warning(f"Altura invalida ({altura_produto}) na linha {index + 1}. Encerrando browser.")
        return False

    if tipo_servico == "SEDEX":
        if comprimento_produto < 11 or comprimento_produto > 100:
            user_logger.warning(f"Comprimento invalido ({comprimento_produto}) na linha {index + 1}. Encerrando browser.")
            return False

        if largura_produto < 6 or largura_produto > 100:
            user_logger.warning(f"Largura invalida ({largura_produto}) na linha {index + 1}. Encerrando browser.")
            return False
        
        return True
        
    if tipo_servico == "PAC":
        if comprimento_produto < 13 or comprimento_produto > 100:
            user_logger.warning(f"Comprimento invalido ({comprimento_produto}) na linha {index + 1}. Encerrando browser.")
            return False
        
        if largura_produto < 8 or largura_produto > 100:
            user_logger.warning(f"Largura invalida ({largura_produto}) na linha {index + 1}. Encerrando browser.")
            return False
        
        return True
    
    
def verificacoes_gerais(row, index, planilha_saida, bot):
    cep_destino = str(row["CEP"])
    user_logger.info(f"Verificando CEP destino: {cep_destino}")

    if not verifica_cep_valido(cep_destino) or cep_destino in ["nan", "N/A", "-"]:
        user_logger.warning(f"CEP inválido encontrado na linha {index + 1}.")
        celula_incorreta(planilha_saida, index)
        return False

    tipo_servico = str(row["TIPO DE SERVIÇO CORREIOS"])
    user_logger.info(f"Verificando tipo de serviço: {tipo_servico}")
    
    if tipo_servico in ["nan", "N/A", "-"]:
        user_logger.warning(f"Tipo de serviço inválido na linha {index + 1}. Encerrando browser.")
        celula_incorreta(planilha_saida, index)
        close_browser(bot)
        return False
    
    dimensoes = str(row["DIMENSÕES CAIXA"])
    user_logger.info("Verificando dimensões do produto.")
    
    if dimensoes in ["nan", "N/A", "-"]:
        user_logger.warning(f"Dimensões inválidas na linha {index + 1}. Encerrando browser.")
        celula_incorreta(planilha_saida, index)
        close_browser(bot)
        return False
    
    dimensoes = dimensoes.split(" x ")
    altura_produto = dimensoes[0].strip()
    largura_produto = dimensoes[1].strip()
    comprimento_produto = dimensoes[2].strip()
    
    user_logger.info(f"Dimensões extraídas: Altura={altura_produto}, Largura={largura_produto}, Comprimento={comprimento_produto}")
    
    if not verifica_dimensoes(tipo_servico, float(comprimento_produto), float(largura_produto), float(altura_produto), index):
        user_logger.warning(f"Regras de dimensões incorretas na linha {index + 1}. Encerrando browser.")
        celula_incorreta(planilha_saida, index)
        close_browser(bot)
        return False
    
    peso_produto = row["PESO DO PRODUTO"]
    user_logger.info(f"Verificando peso do produto: {peso_produto}")
    
    if str(peso_produto) in ["nan", "N/A", "-"]:
        user_logger.warning(f"Peso inválido encontrado na linha {index + 1}. Encerrando browser.")
        celula_incorreta(planilha_saida, index)
        close_browser(bot)
        return False
    
    return True
