import os
import logging

def criar_diretorios():
    rpa_path = r"C:\RPA"
    falhas_path = f"{rpa_path}\Falhas"
    logs_path = f"{rpa_path}\Logs"
    processados_path = f"{rpa_path}\Processados"
    processar_path = f"{rpa_path}\Processar"
    
    try:
        if not os.path.exists(rpa_path):
            logging.info("Diretorio nao encontrado... -> Cria diretorio RPA.")
            os.makedirs(rpa_path)

        if not os.path.exists(falhas_path):
            logging.info("Diretorio nao encontrado... -> Cria diretorio de Falhas.")
            os.makedirs(falhas_path)

        if not os.path.exists(logs_path):
            logging.info("Diretorio nao encontrado... -> Cria diretorio de Logs.")
            os.makedirs(logs_path)

        if not os.path.exists(processados_path):
            logging.info("Diretorio nao encontrado... -> Cria diretorio de Processados.")
            os.makedirs(processados_path)

        if not os.path.exists(processar_path):
            logging.info("Diretorio nao encontrado... -> Cria diretorio de Processar.")
            os.makedirs(processar_path)
        
        return True
    
    except Exception:
        # chama função de erro que também já faz o log do erro
        return False
    