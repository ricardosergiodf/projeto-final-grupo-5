import pandas as pd
import requests
import time
from config import *
from src.configurar_logs import user_logger, dev_logger

def consultar_api(cnpj):
    """Consulta a API para obter os dados do CNPJ."""
    
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    headers = {"User-Agent": "Mozilla/5.0"}
    erro = "Erro ao consultar API"
    data = [""]
    
    for tentativa in range(MAXIMOS_TENTATIVAS_ERRO):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"RESPONSE: {response.status_code}")
            
            if response.status_code == 429:  # Erro de muitas requisições
                user_logger.error(f"Erro 429 - Aguardando antes de tentar novamente... ({tentativa + 1}/{MAXIMOS_TENTATIVAS_ERRO})")
                time.sleep(5)
                continue

            if response.status_code in [400, 404]:  # CNPJ inválido ou não encontrado
                user_logger.error(f"Erro {response.status_code} - Cadastro Inativo")
                return {"CNPJ": cnpj, "Status": "Cadastro Inativo"}

            response.raise_for_status()
            data = response.json()

            if "Erro" in data:
                user_logger.error(f"Erro ao consultar CNPJ {cnpj}: {response.status_code}")
                return {"CNPJ": cnpj, "Status": erro}

            return {
                "CNPJ": cnpj,
                "RAZÃO SOCIAL": data.get("razao_social", ""),
                "NOME FANTASIA": data.get("nome_fantasia", ""),
                "ENDEREÇO": f'{data.get("logradouro", "")}, {data.get("numero", "")}, {data.get("municipio", "")}',
                "CEP": data.get("cep", ""),
                "DESCRIÇÃO MATRIZ FILIAL": data.get("descricao_identificador_matriz_filial", ""),
                "TELEFONE + DDD": data.get("ddd_telefone_1", ""),
                "E-MAIL": data.get("email", "") if data.get("email") else "-",
            }

        except requests.exceptions.RequestException as e:
            user_logger.error(f"Erro ao consultar CNPJ {cnpj}: {erro}")

        
    return {"CNPJ": cnpj, "Status": erro}

def consultar_e_preencher_api(df_saida):
    """Consulta a API para preencher os dados faltantes na tabela de saída."""
    
    try:
        for index, row in df_saida.iterrows():
            cnpj = row["CNPJ"]
            if not isinstance(cnpj, str) or not cnpj.isnumeric():
                print(f"CNPJ inválido na linha {index + 1}: {cnpj}")
                continue
            
            user_logger.info(f"Consultando API para CNPJ: {cnpj}...")
            dados_api = consultar_api(cnpj)
            user_logger.info(f"Consulta realizada com sucesso")

            # Preenche os dados faltantes na linha
            user_logger.info(f"Preenchendo dados faltantes na linha {index + 1}")
            for key, value in dados_api.items():
                #if key in df_saida.columns and not row[key]:  # Preenche se estiver vazio
                if key == "Status" or not row[key]:  
                    df_saida.at[index, key] = value
                

        return df_saida
    
    except Exception as e:
        print(f"Erro ao consultar e preencher API: {e}")

def verificar_campos_vazios(df_saida):
    """Verifica campos vazios e define um status com os campos vazios para cada linha, preenchendo com '-' quando necessário."""

    campos_vazios = {"Status", "VALOR COTAÇÃO JADLOG", "VALOR COTAÇÃO CORREIOS", "PRAZO DE ENTREGA CORREIOS"} 
    status_list = []
    try:
        user_logger.info("Verificando campos vazios e definindo status.")
        for index, row in df_saida.iterrows():
            campos_faltando = []
            
            for col in df_saida.columns:
                if col not in campos_vazios and (pd.isna(row[col]) or str(row[col]).strip() == "" or row[col] == "-"):
                    df_saida.at[index, col] = "-"
                    if col != "TELEFONE + DDD" and col != "E-MAIL" and col != "DIMENSÕES CAIXA" and col != "NOME FANTASIA":
                        campos_faltando.append(col)

            # Atualiza o campo "Status" apenas se não for "Cadastro Inativo"
            if row["Status"] != "Cadastro Inativo":
                status_list.append(f"Faltando: {', '.join(campos_faltando)}" if campos_faltando else " ")
            else:
                status_list.append("Cadastro Inativo")  # Mantém o status inalterado
            
    except Exception as e:
        print(f"Erro ao verificar campos vazios: {e}")

    df_saida["Status"] = status_list
    return df_saida
       

def processar_brasil_api(df_saida):
    """Executa todo o fluxo: preenche com dados existentes, consulta API e verifica status."""
    try:
        print("Consultando API para preencher campos vazios...")
        df_saida = consultar_e_preencher_api(df_saida)

        print("Verificando campos vazios e definindo status...")
        df_saida = verificar_campos_vazios(df_saida)

        # Salvando a planilha com dados atualizados
        df_saida.to_excel(ARQUIVO_SAIDA, index=False, engine="openpyxl")
        print(f"Tabela de saída gerada com sucesso: {ARQUIVO_SAIDA}")
    
    except Exception as e:
        print(f"Erro ao preencher tabela de saída: {e}")

  
