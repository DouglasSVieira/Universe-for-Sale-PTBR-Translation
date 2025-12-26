import json
import pandas as pd
import re
import os
import unicodedata

# Garante que o script rode na pasta raiz
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Planilha exclusiva para dados de sistema
arquivo_csv = 'TRABALHO_DATA.csv'

# Arquivos que este script vai atualizar
arquivos_saida = {
    'Translation/data.json': 'Translation/data.json',
    'Translation/data_fix.json': 'Translation/data_fix.json'
}

def remover_acentos_e_maiusculas(texto):
    if not isinstance(texto, str): return texto
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).upper()

def injetar_texto(data, file_id, novo_texto):
    try:
        # Lógica para IDs complexos como ['scenes'][0]['text']
        chaves = re.findall(r"\[(?:'([^']+)'|(\d+))\]", file_id)
        temp = data
        for i in range(len(chaves) - 1):
            chave = chaves[i][0] if chaves[i][0] else int(chaves[i][1])
            temp = temp[chave]
        
        ultima_chave = chaves[-1][0] if chaves[-1][0] else int(chaves[-1][1])
        temp[ultima_chave] = remover_acentos_e_maiusculas(novo_texto)
    except Exception as e:
        print(f"⚠️ Erro ao injetar no ID {file_id}: {e}")

if os.path.exists(arquivo_csv):
    print(f"🚀 Iniciando exportação de DADOS ({arquivo_csv})...")
    try:
        df = pd.read_csv(arquivo_csv, encoding='utf-8-sig')
        
        for original, novo_nome in arquivos_saida.items():
            if os.path.exists(original):
                with open(original, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                nome_simples = os.path.basename(original)
                # Filtra apenas as linhas que pertencem a este arquivo JSON
                mascara = df['File_ID'].str.contains(nome_simples, na=False)
                dados_filtrados = df[mascara]
                
                contador = 0
                for _, row in dados_filtrados.iterrows():
                    texto = str(row['Traducao_PTBR'])
                    if texto != 'nan' and texto.strip() != "":
                        injetar_texto(json_data, row['File_ID'], texto)
                        contador += 1

                with open(novo_nome, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent='\t')
                print(f"✅ Arquivo atualizado: {novo_nome} ({contador} linhas)")
            else:
                print(f"⚠️ Arquivo base '{original}' não encontrado.")
                
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
else:
    print(f"❌ Erro: Planilha '{arquivo_csv}' não encontrada.")