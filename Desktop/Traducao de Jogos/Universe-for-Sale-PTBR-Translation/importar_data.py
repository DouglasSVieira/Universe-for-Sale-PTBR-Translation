import json
import pandas as pd
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Caminhos para os arquivos na pasta Translation
arquivos_data = [
    'Translation/data.json',
    'Translation/data_fix.json'
]

planilha_data = 'TRABALHO_DATA.csv'

def extrair_recursivo(objeto, prefixo, lista_destino):
    """Varre qualquer estrutura de JSON em busca de textos"""
    if isinstance(objeto, dict):
        for chave, valor in objeto.items():
            # Cria um caminho legível para o File_ID
            novo_prefixo = f"{prefixo}['{chave}']"
            extrair_recursivo(valor, novo_prefixo, lista_destino)
    elif isinstance(objeto, list):
        for i, valor in enumerate(objeto):
            novo_prefixo = f"{prefixo}[{i}]"
            extrair_recursivo(valor, novo_prefixo, lista_destino)
    elif isinstance(objeto, str):
        texto = objeto.strip()
        # Filtro: Ignora textos muito curtos, números puros ou caminhos de arquivo
        if len(texto) > 2 and not texto.endswith(('.png', '.ogg', '.json')) and not texto.replace('.','').isdigit():
            lista_destino.append({
                'File_ID': prefixo,
                'Texto_Original_ES': objeto,
                'Traducao_PTBR': ''
            })

def executar_importacao():
    dados_totais = []
    for nome_arquivo in arquivos_data:
        if os.path.exists(nome_arquivo):
            print(f"📦 Varrendo profundamente: {nome_arquivo}...")
            try:
                with open(nome_arquivo, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                nome_base = os.path.basename(nome_arquivo)
                extrair_recursivo(json_data, nome_base, dados_totais)
            except Exception as e:
                print(f"❌ Erro ao ler {nome_arquivo}: {e}")
        else:
            print(f"⚠️ Arquivo não encontrado: {nome_arquivo}")

    if dados_totais:
        df = pd.DataFrame(dados_totais)
        df.to_csv(planilha_data, index=False, encoding='utf-8-sig')
        print(f"✅ Sucesso! {len(dados_totais)} linhas encontradas em {planilha_data}")
    else:
        print("❌ Nenhum texto traduzível foi encontrado nos arquivos.")

if __name__ == "__main__":
    executar_importacao()