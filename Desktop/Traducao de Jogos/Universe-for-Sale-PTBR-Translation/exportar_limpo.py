import json
import pandas as pd
import re
import os
import unicodedata

# Força o script a olhar para a pasta onde ele está
os.chdir(os.path.dirname(os.path.abspath(__file__)))

arquivo_csv = 'TRABALHO_BASE_ESPANHOL.csv' 
arquivos_saida = {
    'dlg_choose_es.json': 'dlg_choose_eng.json',
    'dlg_dialoghi_es.json': 'dlg_dialoghi_eng.json'
}

def limpar_acentos_total(texto):
    if not isinstance(texto, str) or texto == 'nan': return ""
    # Remove acentos e converte para maiúsculas (padrão seguro para o jogo)
    nfkd = unicodedata.normalize('NFKD', texto)
    texto = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return texto.upper().replace('Ç', 'C').replace('Ñ', 'N')

def injetar_texto(data, file_id, novo_texto):
    try:
        indices = [int(i) for i in re.findall(r'\[(\d+)\]', str(file_id))]
        temp = data['data']
        for i in range(len(indices) - 1):
            temp = temp[indices[i]]
        temp[indices[-1]] = novo_texto
    except:
        pass

# EXECUÇÃO MAIS ROBUSTA
if os.path.exists(arquivo_csv):
    print(f"🚀 Lendo {arquivo_csv}...")
    try:
        # O 'sep=None' faz o Pandas descobrir sozinho se é vírgula ou ponto e vírgula
        df = pd.read_csv(arquivo_csv, sep=None, engine='python', encoding='utf-8-sig', on_bad_lines='skip')
        
        for original, novo_nome in arquivos_saida.items():
            if os.path.exists(original):
                print(f"Gerando {novo_nome}...")
                with open(original, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # Procura as colunas corretas independente do nome
                col_id = 'File_ID'
                col_texto = 'Traducao_PTBR' if 'Traducao_PTBR' in df.columns else df.columns[-1]
                
                for _, row in df[df[col_id].str.contains(original, na=False)].iterrows():
                    texto_limpo = limpar_acentos_total(str(row[col_texto]))
                    injetar_texto(json_data, row[col_id], texto_limpo)

                with open(novo_nome, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=True)
        
        print("\n✅ CONCLUÍDO! Arquivos gerados sem acentos.")
    except Exception as e:
        print(f"❌ Erro ao ler a planilha: {e}")
else:
    print(f"❌ Erro: {arquivo_csv} não encontrado.")