import pyautogui
from botcity.maestro import *
from config import *
from src.configurar_logs import user_logger
import os
import time

def capturar_tela():
    try:
        # Define o diretório de prints
        path_prints = os.path.join(PATH_LOGS, "Prints")

        # Gera um nome único para o arquivo
        nome_arquivo = time.strftime("%d-%m-%Y_%H-%M-%S.png")
        arquivo_print = os.path.join(path_prints, nome_arquivo)

        # Salva o screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(arquivo_print)
        user_logger.info(f"Screenshot salvo com sucesso em {arquivo_print}!")

        return arquivo_print  # Retorna o caminho do print salvo

    except Exception as error:
        user_logger.error(f"Erro ao salvar o screenshot: {error}")
        raise Exception("Erro ao salvar o screenshot")
    
def maestro_finalizar_sucesso():
    #Manda uma resposta para o osquestrador de que a tarefa foi finalizada com sucesso
    execution = maestro.get_execution()
    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Processo finalizado com sucesso",
        total_items=1,
        processed_items=1,
        failed_items=0
    )