from src.webbot import *
from config import *
import pandas as pd
from src.configurar_logs import user_logger, dev_logger
from src.setup import *

def cotacao_correios(bot):
    """
    Realiza a cotação de preços e prazos de entrega no site dos Correios com base nos dados fornecidos
    em uma planilha de entrada. Os resultados são salvos na planilha.
    """
    for tentativa in range(1, MAXIMOS_TENTATIVAS_ERRO + 1):
        # Reinstancia o bot caso haja problemas anteriores
        bot = bot_driver_setup()
        user_logger.info(f"Tentativa {tentativa}")
        try:
            user_logger.info("Iniciando cotação dos Correios.")

            user_logger.info("Lendo planilha de saida.")
            planilha_saida = pd.read_excel(ARQUIVO_SAIDA)

            for index, row in planilha_saida.iterrows():
                user_logger.info(QUEBRA_LOG)
                user_logger.info(f"Processando linha {index + 1}.")
                
                # Verifica condições gerais antes de prosseguir com a cotação
                if not verificacoes_gerais(row, index, planilha_saida, bot):
                    continue

                # Extração de informações relevantes da planilha
                cep_destino = str(row["CEP"])
                tipo_servico = str(row["TIPO DE SERVIÇO CORREIOS"])
                dimensoes = str(row["DIMENSÕES CAIXA"]).split(" x ")
                altura_produto = dimensoes[0].strip()
                largura_produto = dimensoes[1].strip()
                comprimento_produto = dimensoes[2].strip()
                peso_produto = row["PESO DO PRODUTO"]
                
                # Remove o ponto decimal do CEP, se houver
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

                user_logger.info("Selecionando tipo de embalagem.")
                select_embalagem = capturar_seletor_xpath("//select[@name ='embalagem1']", bot)
                selecionar_por_texto("Outra Embalagem", select_embalagem)

                # Conversão do peso do produto para o tipo correto
                if peso_produto == "0.4":
                    peso_produto = float(peso_produto)
                else:
                    peso_produto = int(peso_produto)

                user_logger.info("Preenchendo dimensões e peso.")
                preencher_xpath(altura_produto, "//input[@name ='Altura']", bot)
                preencher_xpath(largura_produto, "//input[@name ='Largura']", bot)
                preencher_xpath(comprimento_produto, "//input[@name='Comprimento']", bot)
                
                select_peso = capturar_seletor_xpath("//select[@name ='peso']", bot)
                selecionar_por_texto (str(peso_produto), select_peso)

                user_logger.info("Clicando no botão Calcular.")
                clicar_xpath("//input[@name ='Calcular']", bot)  

                # Captura o resultado da cotação e salva na planilha
                captura_resultado(bot, planilha_saida, index)

                user_logger.info("Salvando planilha atualizada.")
                planilha_saida.to_excel(ARQUIVO_SAIDA, index=False)

                # Fecha o navegador após o processamento
                close_browser(bot)

            user_logger.info("Cotação finalizada com sucesso.")
            user_logger.info(QUEBRA_LOG)
            return True

        except Exception as e:
            # Registra erros durante as tentativas
            user_logger.warning(f"Ocorreu um erro durante a cotação Correios na tentativa {tentativa}.")
            dev_logger.error(f'Erro: {e} na tentativa {tentativa}')

    # Se todas as tentativas falharem, levanta uma exceção
    raise Exception(f"Máxima de {MAXIMOS_TENTATIVAS_ERRO} tentativas alcançada, finalizando cotação Correios...")


def celula_incorreta(planilha_saida, index):
    """
    Registra erro na linha especificada da planilha, substituindo os valores de cotação e atualização do status.
    """
    user_logger.warning(f"Registrando erro na linha {index + 1}.")

    planilha_saida.at[index, "VALOR COTAÇÃO CORREIOS"] = "-"
    planilha_saida.at[index, "PRAZO DE ENTREGA CORREIOS"] = "-"

    status = planilha_saida.at[index, "Status"]
    if status in ["nan", "N/A", "-", " "]:
        planilha_saida.at[index, "Status"] = "Erro ao realizar a cotação Correios"
    else:
        planilha_saida.at[index, "Status"] = f"{status} | Erro ao realizar a cotação Correios"

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
    Captura os resultados de cotação no site dos Correios e atualiza a planilha.
    """
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

        # Troca a vírgula por ponto, para melhor manipulação dos dados e evitar erros (padronização dos dados)
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
        """
        Erro geralmente causado por muitas requisições no site dos correios, o ip acaba sendo bloqueado temporariamente
        Solução: Esperar um tempo para que o ip seja desbloqueado e o bot tente executar o processo novamente
        """
        time.sleep(60)
        close_browser(bot)
        raise Exception("Erro ao capturar o resultado da cotação")



def verifica_dimensoes(tipo_servico, comprimento_produto, largura_produto, altura_produto, index):
    """
    Verifica se as dimensões do produto estão dentro dos padrões aceitos pelos Correios.
    """
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
    """
    Realiza verificações gerais nos dados antes de prosseguir com a cotação,
    se for verificado algum erro, já é preenchido o erro da cotação na planilha de saída.
    """
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
    
    # Divide a variável de dimensões em 3 variáveis: altura, largura e comprimento para manipulação correta dos dados
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
