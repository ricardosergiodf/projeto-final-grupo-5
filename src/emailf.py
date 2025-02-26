import smtplib
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import *
import pandas as pd
from src.configurar_logs import user_logger

def mandar_email(nome_processo, arquivo_nome, path_arquivo, is_sucesso = True, nome_tarefa = "n/a"):
    try:
        path_arquivo = f"{path_arquivo}/{arquivo_nome}"
        hora_agora = datetime.now().strftime("%d-%m-%Y - %H:%M")
        if is_sucesso:
            assunto = f"RPA {nome_processo} - {hora_agora}"
            corpo_texto = f"O processo RPA {nome_processo} foi executado com sucesso na data: {hora_agora}"
        else:
            assunto = f"Erro - RPA {nome_processo} - {hora_agora}"
            corpo_texto = f"Foi encontrado ERRO durante a execução do processo RPA {nome_processo}, na data {hora_agora}, na tarefa {nome_tarefa}"

        logging.info(f"Enviando email com {arquivo_nome}")
        USUARIO = "osquesobroubot@gmail.com"
        SENHA = "reeb ohur bnig lqgd"
        
        destinatarios = capturar_destinatarios(ARQUIVO_DESTINATARIOS, NOME_COLUNA_DESTINATARIOS)
        servidor = smtplib.SMTP(host="smtp.gmail.com", port=587)
        servidor.starttls()
        servidor.login(USUARIO, SENHA)

        msg = MIMEMultipart()
        msg["From"] = USUARIO
        msg["To"] = destinatarios
        msg["Subject"] = assunto
        msg.attach(MIMEText(corpo_texto, "plain"))

        with open(path_arquivo, "rb") as arquivo:
            dados = arquivo.read()

        tipo_arquivo = arquivo_nome.split('.', 1)[1].strip()
        print(tipo_arquivo)
        anexo = MIMEApplication(dados, _subtype=tipo_arquivo)
        anexo.add_header("Content-Disposition", "attachment", filename=arquivo_nome)
        msg.attach(anexo)

        servidor.send_message(msg)
        servidor.quit()
        user_logger.info(f"Email enviado para: {destinatarios}")
    except Exception as error:
        user_logger.error(f"Erro ao tentar enviar o email: {error}")
        raise Exception('Erro ao tentar enviar o Email')
        

def capturar_destinatarios(path_arquivo, coluna):
    try:
        excel = pd.read_excel(path_arquivo)
        if coluna in excel.columns:
            #Retorna os valores da coluna em uma lista
            lista = excel[coluna].tolist()
            lista = ", ".join(lista)
            print(f"Lista de emails: {lista}")
            return lista
        else:
            raise Exception(f'Erro: a coluna: {coluna} nao foi encontrada na planilha')
    except Exception as error:
        user_logger.error(f"Erro ao tentar ler os destinatarios na planilha {path_arquivo}: {error}")
        raise Exception(f'Erro ao tentar ler os destinatarios na planilha: {path_arquivo}')

