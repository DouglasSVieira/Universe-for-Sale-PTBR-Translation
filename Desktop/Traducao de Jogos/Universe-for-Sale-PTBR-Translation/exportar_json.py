import json
import pandas as pd
import re
import os

# Garante que o script rode na pasta onde ele está salvo
os.chdir(os.path.dirname(os.path.abspath(__file__)))

arquivo_csv = 'TRABALHO_BASE_ESPANHOL.csv' 
arquivos_saida = {
    'dlg_choose_es.json': 'dlg_choose_eng.json',
    'dlg_dialoghi_es.json': 'dlg_dialoghi_eng.json'
}

def injetar_texto(data, file_id, novo_texto):
    try:
        # Extrai índices como [1][72][0]
        indices = [int(i) for i in re.findall(r'\[(\d+)\]', str(file_id))]
        temp = data['data']
        for i in range(len(indices) - 1):
            temp = temp[indices[i]]
        temp[indices[-1]] = novo_texto
    except:
        pass

if os.path.exists(arquivo_csv):
    print(f"🚀 Iniciando exportação de {arquivo_csv}...")
    try:
        # Tenta ler com ';' (Excel) ou ',' (Google Sheets)
        df = pd.read_csv(arquivo_csv, sep=None, engine='python', encoding='utf-8-sig')
        
        # Identifica as colunas (ajuste se você mudou os nomes no Google Sheets)
        col_id = 'File_ID'
        col_traducao = 'Traducao_PTBR' # Verifique se este é o nome exato na sua planilha
        
        for original, novo_nome in arquivos_saida.items():
            if os.path.exists(original):
                with open(original, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # Filtra apenas as linhas deste arquivo
                mascara = df[col_id].str.contains(original, na=False)
                dados_filtrados = df[mascara]
                
                for _, row in dados_filtrados.iterrows():
                    texto = str(row[col_traducao])
                    if texto != 'nan' and texto.strip() != "":
                        injetar_texto(json_data, row[col_id], texto)

                # Salva o arquivo final
                with open(novo_nome, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent='\t')
                print(f"✅ Arquivo gerado: {novo_nome} ({len(dados_filtrados)} linhas)")
            else:
                print(f"⚠️ Arquivo base '{original}' não encontrado para conversão.")
                
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
else:
    print(f"❌ Erro: Planilha '{arquivo_csv}' não encontrada.")