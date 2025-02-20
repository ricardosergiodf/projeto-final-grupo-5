import os
import pandas as pd
import requests
import time

# Diretórios dos arquivos
DIRETORIO_EXCEL = r"C:\RPA\projeto-final-grupo-5\resources"
ARQUIVO_ENTRADA = os.path.join(DIRETORIO_EXCEL, "tabela_inicial2.xlsx")
ARQUIVO_SAIDA = os.path.join(DIRETORIO_EXCEL, "dados_saida.xlsx")

# Definição das colunas da planilha de saída
COLUNAS_SAIDA = [
    "CNPJ", "RAZÃO SOCIAL", "NOME FANTASIA", "ENDEREÇO", "CEP",
    "DESCRIÇÃO MATRIZ FILIAL", "TELEFONE + DDD", "E-MAIL",
    "VALOR DO PEDIDO", "DIMENSÕES CAIXA", "PESO DO PRODUTO",
    "TIPO DE SERVIÇO JADLOG", "TIPO DE SERVIÇO CORREIOS",
    "VALOR COTAÇÃO JADLOG", "VALOR COTAÇÃO CORREIOS",
    "PRAZO DE ENTREGA CORREIOS", "Status"
]

def carregar_cnpjs():
    """Lê os CNPJs da planilha inicial e retorna uma lista."""
    try:
        df = pd.read_excel(ARQUIVO_ENTRADA, dtype=str)
        df = df.dropna(how="all")  # Remove linhas onde todas as colunas são NaN
        df.fillna("", inplace=True)  # Substitui NaN por string vazia

        if "CNPJ" not in df.columns:
            raise ValueError("A coluna 'CNPJ' não foi encontrada no arquivo de entrada.")
        return df["CNPJ"].dropna().tolist()
    except Exception as e:
        print(f"Erro ao carregar a planilha inicial: {e}")
        return []
    
def carregar_dados_adicionais():
    """Carrega os dados adicionais (como valor do pedido, dimensões, peso, etc.) da planilha inicial e retorna um dicionário."""
    try:
        df = pd.read_excel(ARQUIVO_ENTRADA, dtype=str)
        df = df.dropna(how="all")  # Remove linhas onde todas as colunas são NaN
        df.fillna("", inplace=True)  # Substitui NaN por string vazia
        
       
        
        # Normalizando as colunas para evitar problemas com caracteres especiais
        df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
        
        # Criar um dicionário com os dados adicionais
        dados_adicionais = df[["CNPJ", "VALOR DO PEDIDO", "DIMENSOES CAIXA (altura x largura x comprimento cm)", 
                               "PESO DO PRODUTO", "TIPO DE SERVICO JADLOG", "TIPO DE SERVICO CORREIOS"]].dropna(subset=["CNPJ"])
        return dados_adicionais.set_index("CNPJ").to_dict(orient="index")
    except Exception as e:
        print(f"Erro ao carregar os dados adicionais: {e}")
        return {}

def consultar_api(cnpj, tentativas=3):
    """Consulta a API para obter os dados do CNPJ."""
   
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    headers = {"User-Agent": "Mozilla/5.0"}
    erro = "Erro ao consultar API"

    for tentativa in range(tentativas):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 429:  # Erro de muitas requisições
                print(f"⚠️ Erro 429 - Aguardando antes de tentar novamente... ({tentativa + 1}/{tentativas})")
                time.sleep(10)  # Espera 10 segundos antes de tentar de novo
                continue  # Tenta novamente

            response.raise_for_status()
            data = response.json()
            

            # Se a API retornar um erro no JSON, capturamos a mensagem
            if "message" in data:
                erro = data["message"]  # Atualiza a variável erro com a mensagem da API
                print(f"Erro ao consultar CNPJ {cnpj}: {erro}")
                return {"CNPJ": cnpj, "Status": erro}
                

            return{
                "CNPJ": cnpj,
                "RAZÃO SOCIAL": data.get("razao_social", ""),
                "SITUACAO_CADASRTAL": data.get("situacao_cadastral", ""),
                "NOME FANTASIA": data.get("nome_fantasia", ""),
                "ENDEREÇO": f'{data.get("logradouro", "")}, {data.get("numero", "")}, {data.get("municipio", "")}',
                "CEP": data.get("cep", ""),
                "DESCRIÇÃO MATRIZ FILIAL": data.get("descricao_identificador_matriz_filial", ""),
                "TELEFONE + DDD": data.get("ddd_telefone_1", ""),
                "E-MAIL": data.get("email", "")if data.get("email") else "N/A" # Se não houver e-mail, exibe "N/A"
            }
        
        except requests.exceptions.RequestException as e:
            erro = str(e)  # Atualiza a variável erro com a mensagem da exceção
            print(f"Erro ao consultar CNPJ {cnpj}: {erro}")
    
    # Se todas as tentativas falharem, retorna um status de erro
    return {"CNPJ": cnpj, "Status": erro}

def preencher_planilha_saida():
    """Consulta os CNPJs e preenche a planilha de saída."""

    MAPEAMENTO_COLUNAS = {
    "DIMENSOES CAIXA (altura x largura x comprimento cm)": "DIMENSÕES CAIXA",
    "TIPO DE SERVICO JADLOG": "TIPO DE SERVIÇO JADLOG",
    "TIPO DE SERVICO CORREIOS": "TIPO DE SERVIÇO CORREIOS"
}


    
    cnpjs = carregar_cnpjs()
    if not cnpjs:
        print("Nenhum CNPJ encontrado na planilha inicial.")
        return
    
    dados_coletados = []
    
    # Carregar os dados adicionais
    dados_adicionais = carregar_dados_adicionais()

    for cnpj in cnpjs:
        print(f"Consultando API para CNPJ: {cnpj}")
        dados = consultar_api(cnpj)
        '''
        print("Chaves disponíveis em dados_adicionais:", list(dados_adicionais.keys()))
        if cnpj in dados_adicionais:  # Verifica se o CNPJ está no dicionário antes de acessar
            valores = dados_adicionais[cnpj]  # Obtém os dados específicos para aquele CNPJ
            print(f"CNPJ: {cnpj}, Dados: {valores}")  # Exibe os valores corretos
            for coluna_entrada, coluna_saida in MAPEAMENTO_COLUNAS.items():
                if coluna_entrada in valores:
                    dados[coluna_saida] = valores[coluna_entrada]
        '''
        # Criar uma lista de campos vazios para o status
        campos_vazios = [campo for campo, valor in dados.items() if not valor]
        print(campos_vazios)

       # Se não houver erro, verificar campos vazios
        if "Status" not in dados or not dados["Status"]:
            campos_vazios = [campo for campo, valor in dados.items() if not valor]
            dados["Status"] = f"Os campos: {", ".join(campos_vazios)} estão vazios." if campos_vazios else ""

        dados_coletados.append(dados)
        time.sleep(3)  # Pausa para evitar bloqueios na API

    # Criar DataFrame e salvar no Excel
    df_saida = pd.DataFrame(dados_coletados, columns=COLUNAS_SAIDA)
    df_saida.to_excel(ARQUIVO_SAIDA, index=False, engine="openpyxl")
    
    print(f"Dados salvos com sucesso em: {ARQUIVO_SAIDA}")