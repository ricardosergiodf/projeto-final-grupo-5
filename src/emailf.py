import smtplib
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import *
import pandas as pd
from src.configurar_logs import user_logger

def mandar_email(nome_processo, path_arquivo, is_sucesso = True, nome_tarefa = "n/a"):
    """
    Envia um email com mensagens predefinidas (erro ou sucesso) e um anexo passado por argumento

    Args:
        nome_processo (str): Nome do processo RPA
        path_arquivo (str): Path do arquivo a ser anexado
        is_sucesso (bool): Indica se a execução foi bem-sucedida. Default é True.
        nome_tarefa (str): Nome da tarefa onde ocorreu o erro, se houver. Default é "n/a".

    """

    try:
        arquivo_nome = os.path.basename(path_arquivo)
        user_logger.info(f"Enviando email com o arquivo: {arquivo_nome}")
        hora_agora = datetime.now().strftime("%d-%m-%Y - %H:%M")

        #Define o mesagem e o assunto do email baseado se é sucesso ou erro
        if is_sucesso:
            assunto = f"RPA {nome_processo} - {hora_agora}"
            corpo_texto = f"O processo RPA {nome_processo} foi executado com sucesso na data: {hora_agora}"
        else:
            assunto = f"Erro - RPA {nome_processo} - {hora_agora}"
            corpo_texto = f"Foi encontrado ERRO durante a execução do processo RPA {nome_processo}, na data {hora_agora}, na tarefa {nome_tarefa}"
        
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

        extensao_arquivo = arquivo_nome.split('.', 1)[1].strip()
        anexo = MIMEApplication(dados, _subtype=extensao_arquivo)
        anexo.add_header("Content-Disposition", "attachment", filename=arquivo_nome)
        msg.attach(anexo)

        servidor.send_message(msg)
        servidor.quit()
        user_logger.info(f"Email enviado para: {destinatarios}")
        #Coloca nos resultados do osquestrador o arquivo
        maestro.post_artifact(
            task_id=execution.task_id,
            artifact_name=arquivo_nome,
            filepath=path_arquivo
        )
    except Exception as error:
        user_logger.error(f"Erro ao tentar enviar o email: {error}")
        raise Exception('falha ao tentar enviar o Email')
        

def capturar_destinatarios(path_arquivo, coluna):
    #Captura os emails na planilha emails.xlsx que serao utilizado como destinarios
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

