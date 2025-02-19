import os
import logging

def criar_diretorios():
    PATH_RPA = r"C:\RPA"
    PATH_FALHAS = f"{PATH_RPA}\Falhas"
    PATH_LOGS = f"{PATH_RPA}\Logs"
    PATH_PROCESSADOS = f"{PATH_RPA}\Processados"
    PATH_PROCESSAR = f"{PATH_RPA}\Processar"
    
    try:
        if not os.path.exists(PATH_RPA):
            logging.info("Diretorio nao encontrado... -> Cria diretorio RPA.")
            os.makedirs(PATH_RPA)

        if not os.path.exists(PATH_FALHAS):
            logging.info("Diretorio nao encontrado... -> Cria diretorio de Falhas.")
            os.makedirs(PATH_FALHAS)

        if not os.path.exists(PATH_LOGS):
            logging.info("Diretorio nao encontrado... -> Cria diretorio de Logs.")
            os.makedirs(PATH_LOGS)

        if not os.path.exists(PATH_PROCESSADOS):
            logging.info("Diretorio nao encontrado... -> Cria diretorio de Processados.")
            os.makedirs(PATH_PROCESSADOS)

        if not os.path.exists(PATH_PROCESSAR):
            logging.info("Diretorio nao encontrado... -> Cria diretorio de Processar.")
            os.makedirs(PATH_PROCESSAR)
        
        return True
    
    except Exception:
        # chama função de erro que também já faz o log do erro
        return False
