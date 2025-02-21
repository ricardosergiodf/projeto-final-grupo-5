import os
import pandas as pd
import requests
import time

# Diretórios dos arquivos
DIRETORIO_EXCEL = r"C:\RPA\projeto-final-grupo-5\resources"
ARQUIVO_ENTRADA = os.path.join(DIRETORIO_EXCEL, "tabela_inicial2.xlsx")
FORMATO_DATA = time.strftime("%d-%m-%Y_%H-%M-%S")
ARQUIVO_SAIDA = os.path.join(DIRETORIO_EXCEL, f"cnpjs_{FORMATO_DATA}.xlsx")

# Definição das colunas da planilha de saída
COLUNAS_SAIDA = [
    "CNPJ", "RAZÃO SOCIAL", "NOME FANTASIA", "ENDEREÇO", "CEP",
    "DESCRIÇÃO MATRIZ FILIAL", "TELEFONE + DDD", "E-MAIL",
    "VALOR DO PEDIDO", "DIMENSÕES CAIXA", "PESO DO PRODUTO",
    "TIPO DE SERVIÇO JADLOG", "TIPO DE SERVIÇO CORREIOS",
    "VALOR COTAÇÃO JADLOG", "VALOR COTAÇÃO CORREIOS",
    "PRAZO DE ENTREGA CORREIOS", "Status"
]

def consultar_api(cnpj, tentativas=3):
    """Consulta a API para obter os dados do CNPJ."""
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    headers = {"User-Agent": "Mozilla/5.0"}
    erro = "Erro ao consultar API"

    for tentativa in range(tentativas):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 429:  # Erro de muitas requisições
                print(f"Erro 429 - Aguardando antes de tentar novamente... ({tentativa + 1}/{tentativas})")
                time.sleep(10)
                continue

            response.raise_for_status()
            data = response.json()

            if "message" in data:
                erro = data["message"]
                print(f"Erro ao consultar CNPJ {cnpj}: {erro}")
                return {"CNPJ": cnpj, "Status": erro}

            return {
                "CNPJ": cnpj,
                "RAZÃO SOCIAL": data.get("razao_social", ""),
                "NOME FANTASIA": data.get("nome_fantasia", ""),
                "ENDEREÇO": f'{data.get("logradouro", "")}, {data.get("numero", "")}, {data.get("municipio", "")}',
                "CEP": data.get("cep", ""),
                "DESCRIÇÃO MATRIZ FILIAL": data.get("descricao_identificador_matriz_filial", ""),
                "TELEFONE + DDD": data.get("ddd_telefone_1", ""),
                "E-MAIL": data.get("email", "") if data.get("email") else "N/A"
            }
        
        except requests.exceptions.RequestException as e:
            erro = str(e)
            print(f"Erro ao consultar CNPJ {cnpj}: {erro}")
    
    return {"CNPJ": cnpj, "Status": erro}

def consultar_e_preencher_api(df_saida):
    """Consulta a API para preencher os dados faltantes na tabela de saída."""
    try:
        for index, row in df_saida.iterrows():
            cnpj = row["CNPJ"]
            if not isinstance(cnpj, str) or not cnpj.isnumeric():
                print(f"CNPJ inválido na linha {index + 1}: {cnpj}")
                continue

            print(f"Consultando API para CNPJ: {cnpj}...")
            dados_api = consultar_api(cnpj)

            # Preenche os dados faltantes na linha
            for key, value in dados_api.items():
                if key in df_saida.columns and not row[key]:  # Preenche se estiver vazio
                    df_saida.at[index, key] = value

        return df_saida
    
    except Exception as e:
        print(f"Erro ao consultar e preencher API: {e}")

def preencher_com_dados_existentes():
    """Preenche a tabela de saída com os dados da planilha de entrada."""
    try:
        # Lendo os dados de entrada
        df_entrada = pd.read_excel(ARQUIVO_ENTRADA, dtype=str, engine="openpyxl")
        df_saida = df_entrada.copy()

        # Criando colunas ausentes
        for coluna in COLUNAS_SAIDA:
            if coluna not in df_saida.columns:
                df_saida[coluna] = ""

        return df_saida
    except Exception as e:
        print(f"Erro ao preencher com dados existentes: {e}")


def verificar_campos_vazios(df_saida):
    """Verifica campos vazios e define um status com os campos vazios para cada linha, preenchendo com 'N/A' quando necessário."""

    campos_vazios = {"Status", "DIMENSÕES CAIXA", "VALOR COTAÇÃO JADLOG", "VALOR COTAÇÃO CORREIOS", "PRAZO DE ENTREGA CORREIOS"}
    status_list = []
    try:
        for index, row in df_saida.iterrows():
            campos_faltando = []
            
            for col in df_saida.columns:
                if col not in campos_vazios and (pd.isna(row[col]) or str(row[col]).strip() == "" or row[col] == "N/A"):
                    df_saida.at[index, col] = "N/A"
                    campos_faltando.append(col)

            status_list.append("Completo" if not campos_faltando else f"Faltando: {', '.join(campos_faltando)}")
    except Exception as e:
        print(f"Erro ao verificar campos vazios: {e}")

    df_saida["Status"] = status_list
    return df_saida


def preencher_tabela_saida():
    """Executa todo o fluxo: preenche com dados existentes, consulta API e verifica status."""
    try:
        print("Preenchendo tabela com dados existentes...")
        df_saida = preencher_com_dados_existentes()

        print("Consultando API para preencher campos vazios...")
        df_saida = consultar_e_preencher_api(df_saida)

        print("Verificando campos vazios e definindo status...")
        df_saida = verificar_campos_vazios(df_saida)

        # Salvando a planilha
        df_saida.to_excel(ARQUIVO_SAIDA, index=False, engine="openpyxl")
        print(f"Tabela de saída gerada com sucesso: {ARQUIVO_SAIDA}")
    
    except Exception as e:
        print(f"Erro ao preencher tabela de saída: {e}")


# Executar a função
preencher_tabela_saida()

