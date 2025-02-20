import logging
from datetime import datetime
from botcity.maestro import MaestroSDK

maestro = MaestroSDK() 

def configurar_log():
    try:
        # Define o nome do arquivo de log com base na data e horário
        log_filename = datetime.now().strftime("log_%Y-%m-%d_%H-%M-%S.txt")

        # Configura o logger
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            handlers=[logging.StreamHandler(), logging.FileHandler(log_filename, mode="a")]
        )

    except Exception as e:
        logging.error(f"Erro ao configurar o logger.")
        raise

def enviar_log_maestro(message):
    try: 
        logging.info(message)
        maestro.new_log_entry(activity_label="DEFAULT", values={"Message": message}) 

    except Exception as e:
        logging.error(f"Erro ao configurar log maestro.")
        raise 
