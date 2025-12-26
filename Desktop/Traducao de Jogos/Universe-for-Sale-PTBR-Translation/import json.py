import json
import pandas as pd
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

arquivos_para_importar = [
    'Translation/dlg_choose_es.json',
    'Translation/dlg_dialoghi_es.json',
    'Translation/data.json',
    'Translation/data_fix.json'
]

planilha_nome = 'TRABALHO_BASE_ESPANHOL.csv'

def eh_lixo_tecnico(texto):
    """Identifica se a string é apenas código (ex: 'anim_idle', '0.5', 'true')"""
    if not isinstance(texto, str) or len(texto.strip()) < 2:
        return True
    # Ignora se for apenas números e pontos (coordenadas)
    if re.match(r'^[0-9\.\-\, ]+$', texto):
        return True
    # Ignora nomes internos de objetos comuns no motor
    if texto.startswith(('obj_', 'spr_', 'bg_', 'snd_', 'vid_', 'layer_')):
        return True
    return False

def executar_importacao_final():
    # 1. Tenta resgatar o que você já traduziu
    df_antigo = pd.DataFrame()
    if os.path.exists(planilha_nome):
        print(f"📖 Recuperando traduções de {planilha_nome}...")
        df_antigo = pd.read_csv(planilha_nome, encoding='utf-8-sig')
        # Remove duplicatas e linhas vazias para um merge limpo
        df_antigo = df_antigo[['File_ID', 'Traducao_PTBR']].dropna(subset=['Traducao_PTBR'])
        df_antigo = df_antigo.drop_duplicates(subset=['File_ID'])

    # 2. Varre os arquivos em busca de textos reais
    dados_jsons = []
    for nome_arquivo in arquivos_para_importar:
        if os.path.exists(nome_arquivo):
            print(f"📦 Extraindo diálogos de: {nome_arquivo}...")
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            if 'data' in json_data:
                for i, bloco in enumerate(json_data['data']):
                    if isinstance(bloco, list):
                        for j, texto in enumerate(bloco):
                            # Se for texto e não for código puro, nós queremos
                            if isinstance(texto, str) and not eh_lixo_tecnico(texto):
                                file_id = f"{os.path.basename(nome_arquivo)}[{i}][{j}]"
                                dados_jsons.append({
                                    'File_ID': file_id,
                                    'Texto_Original_ES': texto
                                })

    # 3. Une os dados novos com o seu trabalho anterior
    if dados_jsons:
        df_novo = pd.DataFrame(dados_jsons)
        if not df_antigo.empty:
            # O Merge 'left' garante que o Texto_Original_ES novo receba a Traducao_PTBR antiga
            df_final = pd.merge(df_novo, df_antigo, on='File_ID', how='left').fillna("")
        else:
            df_final = df_novo
            df_final['Traducao_PTBR'] = ""

        df_final.to_csv(planilha_nome, index=False, encoding='utf-8-sig')
        print(f"✅ Sucesso! Planilha reconstruída com {len(df_final)} linhas.")
        print(f"📌 Busque por 'echar un vistazo' — ela deve estar no final da lista.")
    else:
        print("❌ Nenhum texto foi detectado. Verifique se os arquivos estão na pasta Translation/.")

if __name__ == "__main__":
    executar_importacao_final()