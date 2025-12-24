import json
import pandas as pd
import re
import os
import unicodedata

# Garante que o script rode na pasta raiz do projeto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

arquivo_csv = 'TRABALHO_BASE_ESPANHOL.csv' 

# Configurado para atualizar os arquivos de ESPANHOL diretamente em Translation/
arquivos_saida = {
    'Translation/dlg_choose_es.json': 'Translation/dlg_choose_es.json',
    'Translation/dlg_dialoghi_es.json': 'Translation/dlg_dialoghi_es.json'
}

def remover_acentos_e_maiusculas(texto):
    if not isinstance(texto, str):
        return texto
    # Remove acentos para compatibilidade com o motor do jogo
    nfkd_form = unicodedata.normalize('NFKD', texto)
    texto_sem_acento = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    # Converte para MAIÚSCULAS
    return texto_sem_acento.upper()

def injetar_texto(data, file_id, novo_texto):
    try:
        indices = [int(i) for i in re.findall(r'\[(\d+)\]', str(file_id))]
        temp = data['data']
        for i in range(len(indices) - 1):
            temp = temp[indices[i]]
        # Aplica a limpeza antes de salvar no JSON
        temp[indices[-1]] = remover_acentos_e_maiusculas(novo_texto)
    except:
        pass

if os.path.exists(arquivo_csv):
    print(f"🚀 Iniciando exportação LIMPA (Sem acentos/MAIÚSCULAS) para o ESPANHOL...")
    try:
        df = pd.read_csv(arquivo_csv, sep=None, engine='python', encoding='utf-8-sig')
        col_id = 'File_ID'
        col_traducao = 'Traducao_PTBR' 
        
        for original, novo_nome in arquivos_saida.items():
            if os.path.exists(original):
                with open(original, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                nome_simples = os.path.basename(original)
                mascara = df[col_id].str.contains(nome_simples, na=False)
                dados_filtrados = df[mascara]
                
                for _, row in dados_filtrados.iterrows():
                    texto = str(row[col_traducao])
                    if texto != 'nan' and texto.strip() != "":
                        injetar_texto(json_data, row[col_id], texto)

                with open(novo_nome, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent='\t')
                print(f"✅ Arquivo LIMPO atualizado: {novo_nome}")
            else:
                print(f"⚠️ Arquivo base '{original}' não encontrado na pasta Translation/.")
                
    except Exception as e:
        print(f"❌ Erro crítico no processamento: {e}")
else:
    print(f"❌ Erro: Planilha '{arquivo_csv}' não encontrada na raiz.")