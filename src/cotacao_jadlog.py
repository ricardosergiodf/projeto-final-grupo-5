from src.webbot import *
from config import *
import pandas as pd
from src.configurar_logs import user_logger
from botcity.web import By

def cotacao_jadlog(bot):
    try:
        user_logger.info("Iniciando cotacao JadLog.")

        user_logger.info("Lendo planilha de saida.")
        planilha_saida = pd.read_excel(ARQUIVO_SAIDA)

        for index, row in  planilha_saida.iterrows():
            user_logger.info(f"Processando linha {index + 1}.")

            cep_destino = str(row["CEP"])
            tipo_servico = str(row["TIPO DE SERVIÇO JADLOG"])
            valor_pedido = str(row["VALOR DO PEDIDO"])
            try:
                dimensoes = str(row["DIMENSÕES CAIXA"]).split(" x ")
                altura_produto = dimensoes[0].strip()
                largura_produto = dimensoes[1].strip()
                comprimento_produto = dimensoes[2].strip()
            except:
                dimensoes = ""
            
            peso_produto = row["PESO DO PRODUTO"]

            if not verificacoes_gerais(row, index, planilha_saida, bot):
                continue

            user_logger.info("Abrindo a página do Jadlog.")
            abrir_url(URL_JADLOG, bot)

            if "." in str(cep_destino):
                cep_destino = str(cep_destino).split(".")[0]

            user_logger.info("Preenchendo o cep de origem e cep de destino.")
            preencher_xpath(CEP_ORIGEM, "//input[@id='origem']", bot)
            preencher_xpath(cep_destino, "//input[@id='destino']", bot)

            user_logger.info("Selecionando tipo de serviço/modalidade.")
            select_tipo_servico = capturar_seletor_xpath("//select[@id='modalidade']", bot)

            if tipo_servico == "JADLOG Econômico":
                selecionar_por_valor("5", select_tipo_servico)
            elif tipo_servico == "JADLOG Expresso":
                selecionar_por_valor("0", select_tipo_servico)
            else:
                user_logger.error("Tipo de serviço incorreto.")
                raise ValueError("Tipo de serviço incorreto.")

            user_logger.info("Clicando no 'Sim' em 'Frete a pagar'.")
            clicar_xpath("//input[@id='selectFrete:0']", bot)

            
            try:
                user_logger.info("Preenchendo o peso do produto.")
                clear_preencher(str(peso_produto).replace(".", ","), "//input[@id='peso']", bot)

                user_logger.info("Preenchendo o valor da mercadoria.")
                clear_preencher(str(valor_pedido).replace(".", ","), "//input[@id='valor_mercadoria']", bot)
            except Exception as e:
                print(e)

            if dimensoes != "":
                user_logger.info("Preenchendo a largura do produto.")
                clear_preencher(str(largura_produto).replace(".", ","), "//input[@id='valLargura']", bot)

                user_logger.info("Preenchendo a altura do produto.")
                clear_preencher(str(altura_produto).replace(".", ","), "//input[@id='valAltura']", bot)

                user_logger.info("Preenchendo o comprimento do produto.")
                clear_preencher(str(comprimento_produto).replace(".", ","), "//input[@id='valComprimento']", bot)

            user_logger.info("Clicando em 'Simular'.")
            clicar_xpath("//input[@value='Simular']", bot)

            captura_resultado(bot, planilha_saida, index)

            close_browser(bot)
        user_logger.info(QUEBRA_LOG)
        return True
    except Exception:
        # error_exception()
        return False
    
def celula_incorreta(planilha_saida, index):
    user_logger.warning(f"Registrando erro na linha {index + 1}.")
    planilha_saida.at[index, "VALOR COTAÇÃO JADLOG"] = "-"

    status = planilha_saida.at[index, "Status"]
    planilha_saida.at[index, "Status"] = f"{status} | Erro ao realizar a cotação Jadlog"

    user_logger.info("Salvando planilha atualizada.")
    planilha_saida.to_excel(ARQUIVO_SAIDA, index=False)

    return


def verifica_cep_valido(cep):
    try:
        cep = str(cep).replace("-", "").split(".")[0]
        return len(cep) == 8 and cep.isdigit()
    except ValueError:
        user_logger.warning("CEP Inválido.")
        # error_exception()
        return False
    

def captura_resultado(bot, planilha_saida, index):
    bot.wait(500)
    
    user_logger.info("Capturando custo do frete Jadlog.")
    valor_total = capturar_xpath("/html[1]/body[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[4]/div[1]/div[1]/div[2]/div[2]/span[1]", bot)

    if valor_total in "Localidade nao atende FRAP":
        user_logger.warning("Localidade não atendidade pelo Jadlog.")
        celula_incorreta(planilha_saida, index)
        return

    valor_total = valor_total.replace(",", ".")
    valor_total = valor_total.split(" ")[1].strip()

    user_logger.info(f"Valor total capturado: {valor_total}")

    planilha_saida.at[index, "VALOR COTAÇÃO JADLOG"] = valor_total
    return


def verificacoes_gerais(row, index, planilha_saida, bot):
    cep_destino = str(row["CEP"])
    user_logger.info(f"Verificando CEP destino: {cep_destino}")

    if not verifica_cep_valido(cep_destino) or cep_destino in ["nan", "-"]:
        user_logger.warning(f"CEP inválido encontrado na linha {index + 1}.")
        celula_incorreta(planilha_saida, index)
        return False

    tipo_servico = str(row["TIPO DE SERVIÇO JADLOG"])
    user_logger.info(f"Verificando tipo de serviço: {tipo_servico}")
    
    if tipo_servico in ["nan", "-"]:
        user_logger.warning(f"Tipo de serviço inválido na linha {index + 1}. Encerrando browser.")
        celula_incorreta(planilha_saida, index)
        close_browser(bot)
        return False
    
    dimensoes = str(row["DIMENSÕES CAIXA"])
    user_logger.info("Verificando dimensões do produto.")  # na cotação jadlog, as dimensões podem ser 0 ou ""
    
    try:
        dimensoes = dimensoes.split(" x ")
        altura_produto = dimensoes[0].strip()
        largura_produto = dimensoes[1].strip()
        comprimento_produto = dimensoes[2].strip()
        
        user_logger.info(f"Dimensões extraídas: Altura={altura_produto}, Largura={largura_produto}, Comprimento={comprimento_produto}")
    except:
        user_logger.info(f"Dimensões nulas extraídas.")
    
    peso_produto = row["PESO DO PRODUTO"]
    user_logger.info(f"Verificando peso do produto: {peso_produto}")
    
    if str(peso_produto) in ["nan", "-"]:
        user_logger.warning(f"Peso inválido encontrado na linha {index + 1}. Encerrando browser.")
        celula_incorreta(planilha_saida, index)
        close_browser(bot)
        return False
    
    if float(peso_produto) < 1:
        user_logger.warning(f"Peso inválido encontrado na linha {index + 1}. Encerrando browser.")
        celula_incorreta(planilha_saida, index)
        close_browser(bot)
        return False
    
    return True
