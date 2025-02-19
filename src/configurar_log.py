import logging
from datetime import datetime

def configurar_logger():
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
        print(f"Erro ao configurar o logger.")
        raise
