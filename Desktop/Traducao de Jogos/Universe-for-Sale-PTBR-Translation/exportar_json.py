import json
import pandas as pd
import re
import os

# Garante que o script rode na pasta raiz do projeto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

arquivo_csv = 'TRABALHO_BASE_ESPANHOL.csv' 

# Configurado para atualizar os arquivos de ESPANHOL diretamente
arquivos_saida = {
    'Translation/dlg_choose_es.json': 'Translation/dlg_choose_es.json',
    'Translation/dlg_dialoghi_es.json': 'Translation/dlg_dialoghi_es.json'
}

def injetar_texto(data, file_id, novo_texto):
    try:
        indices = [int(i) for i in re.findall(r'\[(\d+)\]', str(file_id))]
        temp = data['data']
        for i in range(len(indices) - 1):
            temp = temp[indices[i]]
        temp[indices[-1]] = novo_texto
    except:
        pass

if os.path.exists(arquivo_csv):
    print(f"🚀 Exportando tradução para os arquivos de idioma ESPANHOL...")
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
                print(f"✅ Atualizado: {novo_nome} ({len(dados_filtrados)} linhas)")
            else:
                print(f"⚠️ Arquivo base '{original}' não encontrado.")
                
    except Exception as e:
        print(f"❌ Erro ao processar a planilha: {e}")
else:
    print(f"❌ Erro: Planilha '{arquivo_csv}' não encontrada.")