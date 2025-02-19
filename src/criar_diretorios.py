import os
import logging
from config import *

def criar_diretorios():
    try:
        if not os.path.exists(PATH_RPA):
            os.makedirs(PATH_RPA)

        if not os.path.exists(PATH_FALHAS):
            os.makedirs(PATH_FALHAS)

        if not os.path.exists(PATH_LOGS):
            os.makedirs(PATH_LOGS)

        if not os.path.exists(PATH_DEVLOGS):
            os.makedirs(PATH_DEVLOGS)

        if not os.path.exists(PATH_PROCESSADOS):
            os.makedirs(PATH_PROCESSADOS)

        if not os.path.exists(PATH_PROCESSAR):
            os.makedirs(PATH_PROCESSAR)

        if not os.path.exists(PATH_PRINTS):
            os.makedirs(PATH_PRINTS)
        
        return True
    
    except Exception:
        # chama função de erro que também já faz o log do erro
        return False
    