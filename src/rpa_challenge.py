from config import *
import pandas as pd
from src.configurar_logs import user_logger
from src.setup import *
from src.webbot import *

def preencher_rpa_challenge():
    """
    Executa o preenchimento automatizado do RPA Challenge utilizando dados de um arquivo Excel.

    Args:
        Nenhum argumento é necessário para a execução.

    Exceções:
        Exception: Caso o botão 'Start' ou 'Submit' não seja encontrado.

    """
    tarefa_atual = "Preencher RPA Challenge"
    tentativas_navegador = 0
    
    while tentativas_navegador < MAX_TRY_ERRORS:
        bot = bot_driver_setup()
        try:
            user_logger.info(QUEBRA_LOG)
            user_logger.info("Iniciando o RPA Challenge.")
            abrir_url(URL_RPA_CHALLENGE, bot)

            user_logger.info("Abrindo o Excel com os dados em segundo plano.")
            # Carrega os dados do Excel como strings
            df = pd.read_excel(ARQUIVO_SAIDA, dtype=str)  

            total_linhas = len(df)
            print(df)
            
            # Verifica a existência do botão 'Start'
            start_btn = encontrar_elemento_xpath("//button[contains(text(), 'Start')]", bot)
            if start_btn:
                start_btn.click()
                user_logger.info("Botão 'Start' clicado com sucesso.")
            else:
                user_logger.error("Botão 'Start' não encontrado. Finalizando.")
                raise Exception("Botão 'Start' não encontrado.")

            # Contadores
            tentativa_atual = 1  # Número da tentativa atual
            linha_atual = 2  # Índice da linha do Excel
            indice_linha = 0  # Índice real das linhas do DataFrame
            total_preenchidos = 0  # Contador de formulários preenchidos

            while indice_linha < total_linhas:
                # Processa 10 registros por vez
                for _ in range(10):  
                    if indice_linha >= total_linhas:
                        break

                    # Obtém a linha atual do DataFrame
                    row = df.iloc[indice_linha]  
                    
                    # Mapeia os campos do formulário com os dados do Excel
                    fields = [
                        ("First Name", row['RAZÃO SOCIAL']),
                        ("Last Name", row['Status']),
                        ("Company Name", row['NOME FANTASIA']),
                        ("Role in Company", row['DESCRIÇÃO MATRIZ FILIAL']),
                        ("Address", row['ENDEREÇO']),
                        ("Email", row['E-MAIL']),
                        ("Phone Number", row['TELEFONE + DDD'])
                    ]

                    # Preenche os campos do formulário
                    for label, value in fields:
                        preencher_xpath(value, f"//div[label[text()='{label}']]/input", bot)
                    
                    user_logger.info(f"{tentativa_atual}ª Tentativa: Preenchendo os campos de entrada com a linha {linha_atual}.")

                    # Verifica a existência do botão 'Submit'
                    submit_btn = encontrar_elemento_xpath("//input[@type='submit']", bot)
                    if submit_btn:
                        submit_btn.click()
                        user_logger.info("Botão 'Submit' clicado com sucesso.")
                    else:
                        user_logger.error("Botão 'Submit' não encontrado. Finalizando.")
                        raise Exception("Botão 'Submit' não encontrado.")

                    tentativa_atual += 1
                    linha_atual += 1
                    indice_linha += 1
                    total_preenchidos += 1

                if indice_linha >= total_linhas:
                    user_logger.info("RPA Challenge concluído com sucesso. Finalizando...")
                    break  # Sai do loop

                user_logger.info("Limite de 10 registros atingido. Reiniciando o desafio.")
                
                # No caso de haver mais de 10 registros, clica no botão 'Reset' para reiniciar o desafio
                clicar_xpath("//button[contains(text(), 'Reset')]", bot)

                # Novamente verifica a existência do botão 'Start'
                start_btn = encontrar_elemento_xpath("//button[contains(text(), 'Start')]", bot)
                if start_btn:
                    start_btn.click()
                    user_logger.info("Botão 'Start' clicado com sucesso.")
                else:
                    user_logger.error("Botão 'Start' não encontrado. Finalizando.")
                    raise Exception("Botão 'Start' não encontrado.")
        
            # Fecha o navegador ao final do processo
            close_browser(bot)  
            break

        except Exception as e:
            # Incrementa a contagem de tentativas
            tentativas_navegador += 1  
            # Lança um erro com a primeira linha da exceção
            raise Exception(f"{str(e).splitlines()[0]}.")  
            
        finally:
            user_logger.info("Finalizando o navegador.")
            user_logger.info(QUEBRA_LOG)
