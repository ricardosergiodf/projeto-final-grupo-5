from src.webbot import *
from config import *
import pandas as pd
from src.configurar_logs import user_logger, dev_logger
from src.setup import *

def cotacao_jadlog(bot):
    """
    Realiza a cotação de preços no site do JadLog com base nos dados fornecidos
    em uma planilha de entrada. Os resultados são salvos na planilha.
    """
    for tentativa in range(1, MAXIMOS_TENTATIVAS_ERRO + 1):
        # Reinstancia o bot caso haja problemas anteriores
        bot = bot_driver_setup()
        user_logger.info(f"Tentativa {tentativa}")
        try:
            user_logger.info("Iniciando cotação JadLog.")

            user_logger.info("Lendo planilha de saída.")
            planilha_saida = pd.read_excel(ARQUIVO_SAIDA)

            for index, row in planilha_saida.iterrows():
                user_logger.info(QUEBRA_LOG)
                user_logger.info(f"Processando linha {index + 1}.")

                cep_destino = str(row["CEP"])
                tipo_servico = str(row["TIPO DE SERVIÇO JADLOG"])
                valor_pedido = str(row["VALOR DO PEDIDO"])

                # Processa as dimensões da caixa, se disponíveis
                try:
                    # Divide a variável de dimensões em 3 variáveis: altura, largura e comprimento para manipulação correta dos dados
                    dimensoes = str(row["DIMENSÕES CAIXA"]).split(" x ")
                    altura_produto = dimensoes[0].strip()
                    largura_produto = dimensoes[1].strip()
                    comprimento_produto = dimensoes[2].strip()
                except:
                    dimensoes = ""

                # Obtém o peso do produto
                peso_produto = row["PESO DO PRODUTO"]

                # Realiza verificações gerais e pula a iteração se necessário
                if not verificacoes_gerais(row, index, planilha_saida, bot):
                    continue

                user_logger.info("Abrindo a página do Jadlog.")
                abrir_url(URL_JADLOG, bot)

                # Remove ponto do CEP, caso exista
                if "." in str(cep_destino):
                    cep_destino = str(cep_destino).split(".")[0]

                user_logger.info("Preenchendo o cep de origem e cep de destino.")
                clear_preencher(CEP_ORIGEM, "//input[@id='origem']", bot)
                clear_preencher(cep_destino, "//input[@id='destino']", bot)

                user_logger.info("Selecionando tipo de serviço/modalidade.")
                select_tipo_servico = capturar_seletor_xpath("//select[@id='modalidade']", bot)

                if tipo_servico == "JADLOG Econômico":
                    selecionar_por_valor("5", select_tipo_servico)
                elif tipo_servico == "JADLOG Expresso":
                    selecionar_por_valor("0", select_tipo_servico)
                else:
                    user_logger.error("Tipo de serviço incorreto.")
                    raise ValueError("Tipo de serviço incorreto.")

                # Marca a opção "Frete a pagar"
                user_logger.info("Clicando no 'Sim' em 'Frete a pagar'.")
                clicar_xpath("//input[@id='selectFrete:0']", bot)

                try:
                    # Preenche os campos de peso e valor da mercadoria
                    user_logger.info("Preenchendo o peso do produto.")
                    clear_preencher(str(peso_produto).replace(".", ","), "//input[@id='peso']", bot)

                    user_logger.info("Preenchendo o valor da mercadoria.")
                    clear_preencher(str(valor_pedido).replace(".", ","), "//input[@id='valor_mercadoria']", bot)
                except Exception as e:
                    print(e)

                # Preenche as dimensões, caso estejam disponíveis
                if dimensoes != "":
                    user_logger.info("Preenchendo a largura do produto.")
                    clear_preencher(str(largura_produto).replace(".", ","), "//input[@id='valLargura']", bot)

                    user_logger.info("Preenchendo a altura do produto.")
                    clear_preencher(str(altura_produto).replace(".", ","), "//input[@id='valAltura']", bot)

                    user_logger.info("Preenchendo o comprimento do produto.")
                    clear_preencher(str(comprimento_produto).replace(".", ","), "//input[@id='valComprimento']", bot)

                user_logger.info("Clicando em 'Simular'.")
                clicar_xpath("//input[@value='Simular']", bot)

                # Captura o resultado da cotação e salva na planilha
                captura_resultado(bot, planilha_saida, index)

            # Fecha o navegador após o processamento
            close_browser(bot)
            user_logger.info(QUEBRA_LOG)
            return True
        except Exception as e:
            # Registra erros durante as tentativas
            user_logger.warning(f"Ocorreu um erro durante a cotação Jadlog na tentativa {tentativa}.")
            dev_logger.error(f'Erro: {e} na tentativa {tentativa}')

    # Se todas as tentativas falharem, levanta uma exceção
    raise Exception(f"Máxima de {MAXIMOS_TENTATIVAS_ERRO} tentativas alcançada, finalizando cotação Jadlog...")

    
def celula_incorreta(planilha_saida, index):
    """
    Registra erro na linha especificada da planilha, substituindo os valores de cotação e atualização do status.
    """
    user_logger.warning(f"Registrando erro na linha {index + 1}.")
    planilha_saida.at[index, "VALOR COTAÇÃO JADLOG"] = "-"

    status = planilha_saida.at[index, "Status"]
    if status in ["nan", "N/A", "-", " "]:
        planilha_saida.at[index, "Status"] = "Erro ao realizar a cotação Jadlog"
    else:
        planilha_saida.at[index, "Status"] = f"{status} | Erro ao realizar a cotação Jadlog"

    user_logger.info("Salvando planilha atualizada.")
    planilha_saida.to_excel(ARQUIVO_SAIDA, index=False)

    return


def verifica_cep_valido(cep):
    """
    Verifica se o CEP informado é válido.
    """
    try:
        cep = str(cep).replace("-", "").split(".")[0]
        return len(cep) == 8 and cep.isdigit()
    except ValueError:
        user_logger.warning("CEP Inválido.")
        return False
    

def captura_resultado(bot, planilha_saida, index):
    """
    Captura os resultados de cotação no site JadLog e atualiza a planilha.
    """
    bot.wait(500)
    
    user_logger.info("Capturando custo do frete Jadlog.")
    valor_total = capturar_xpath("/html[1]/body[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[4]/div[1]/div[1]/div[2]/div[2]/span[1]", bot)

    if valor_total in "Localidade nao atende FRAP":
        user_logger.warning("Localidade não atendidade pelo Jadlog.")
        celula_incorreta(planilha_saida, index)
        return

    # Troca a vírgula por ponto, para melhor manipulação dos dados e evitar erros (padronização dos dados)
    valor_total = valor_total.replace(",", ".")
    valor_total = valor_total.split(" ")[1].strip()

    user_logger.info(f"Valor total capturado: {valor_total}")

    planilha_saida.at[index, "VALOR COTAÇÃO JADLOG"] = valor_total
    return


def verificacoes_gerais(row, index, planilha_saida, bot):
    """
    Realiza verificações gerais nos dados antes de prosseguir com a cotação,
    se for verificado algum erro, já é preenchido o erro da cotação na planilha de saída.
    """
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
        # Divide a variável de dimensões em 3 variáveis: altura, largura e comprimento para manipulação correta dos dados
        dimensoes = dimensoes.split(" x ")
        altura_produto = dimensoes[0].strip()
        largura_produto = dimensoes[1].strip()
        comprimento_produto = dimensoes[2].strip()
        
        user_logger.info(f"Dimensões extraídas: Altura={altura_produto}, Largura={largura_produto}, Comprimento={comprimento_produto}")
    except:
        user_logger.info(f"Dimensões nulas extraídas.")
    
    peso_produto = row["PESO DO PRODUTO"]
    user_logger.info(f"Verificando peso do produto: {peso_produto}")
    
    if pd.isna(peso_produto) or peso_produto in ["nan", "-", None]:
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
