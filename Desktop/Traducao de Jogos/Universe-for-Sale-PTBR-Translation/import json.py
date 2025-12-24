import json
import pandas as pd
import os

# Certifique-se de que os nomes dos arquivos estão exatamente assim na pasta
arquivos_es = ['dlg_choose_es.json', 'dlg_dialoghi_es.json']
nome_saida = 'TRABALHO_BASE_ESPANHOL.csv'

def extrair_dados(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        dados_json = json.load(f)
    
    lista_final = []
    
    def recursivo(obj, caminho_id):
        if isinstance(obj, str):
            # Filtra apenas diálogos reais (ignora códigos técnicos)
            if len(obj) > 1 and not obj.startswith("dlg_"):
                lista_final.append({
                    'File_ID': f"{os.path.basename(caminho)} {caminho_id}",
                    'Texto_Espanhol': obj.replace('\n', ' ').replace('\r', ' '),
                    'Traducao_PTBR': '' # Espaço para você traduzir
                })
        elif isinstance(obj, dict):
            for k, v in obj.items():
                recursivo(v, f"{caminho_id}['{k}']" if caminho_id else k)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                recursivo(item, f"{caminho_id}[{i}]")

    # Começa a extração pela chave 'data' do Construct 3
    recursivo(dados_json.get('data', {}), 'data')
    return lista_final

todos_dados = []
for arq in arquivos_es:
    if os.path.exists(arq):
        print(f"Lendo {arq}...")
        todos_dados.extend(extrair_dados(arq))
    else:
        print(f"⚠️ Atenção: Arquivo '{arq}' não encontrado na pasta!")

if todos_dados:
    df = pd.DataFrame(todos_dados)
    # Salva com PONTO E VÍRGULA (;) para o Excel abrir as colunas perfeitamente
    df.to_csv(nome_saida, sep=';', index=False, encoding='utf-8-sig')
    print(f"\n✅ SUCESSO! Planilha '{nome_saida}' gerada com {len(df)} linhas.")
    print("Agora você pode abrir no Excel e começar a traduzir.")
else:
    print("\n❌ Nenhuma linha extraída. Verifique se os arquivos JSON estão na pasta.")