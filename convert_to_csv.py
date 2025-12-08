import json
import csv
import os

# =========================================================
# CONFIGURAÇÕES (Não precisa de ajustes, as pastas já estão definidas)
# =========================================================
JSON_FOLDER = 'Source'  # Pasta onde estão os JSONs originais
OUTPUT_FILE = 'Translation/Universe_for_Sale_PTBR_Workfile.csv' # Arquivo de saída para a tradução
# =========================================================

def recursive_find_strings(data, path, all_strings, filename):
    """Função recursiva para encontrar strings em estruturas aninhadas."""
    
    if isinstance(data, str) and data.strip():
        # Encontramos uma string válida (não vazia)
        # O 'path' serve como um ID único para rastrear a posição no JSON original
        unique_id = f"{filename}_{path}"
        all_strings.append({
            'File_ID': unique_id,
            'Original_File': filename,
            'Original_Text': data,
            'Translation_PTBR': ''
        })
    
    elif isinstance(data, dict):
        # Se for um dicionário (como "data": { ... }), itera pelas chaves
        for key, value in data.items():
            # A chave 'data' é o ponto de partida que vimos na imagem
            if key == 'data' or path: 
                new_path = f"{path}.{key}" if path else key
                recursive_find_strings(value, new_path, all_strings, filename)
    
    elif isinstance(data, list):
        # Se for uma lista (array), itera pelos índices
        for index, item in enumerate(data):
            new_path = f"{path}[{index}]"
            recursive_find_strings(item, new_path, all_strings, filename)

def extract_and_flatten_json():
    """Processa todos os JSONs para CSV."""
    
    all_strings = []
    
    for filename in os.listdir(JSON_FOLDER):
        if filename.endswith('.json'):
            filepath = os.path.join(JSON_FOLDER, filename)
            
            print(f"Processando arquivo: {filename}")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Erro ao ler {filename}: {e}")
                continue

            # Inicia a busca recursiva a partir da raiz do arquivo
            recursive_find_strings(data, "", all_strings, filename)

    # Grava tudo no arquivo CSV
    if all_strings:
        print(f"\nTotal de strings encontradas: {len(all_strings)}")
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            # Usando vírgula como delimitador (mais universal que o ponto e vírgula)
            fieldnames = ['File_ID', 'Original_File', 'Original_Text', 'Translation_PTBR']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',') 
            
            writer.writeheader()
            writer.writerows(all_strings)
            
        print(f"Sucesso! O arquivo de tradução foi criado em: {OUTPUT_FILE}")
    else:
        print("Aviso: Nenhuma string foi extraída. Verifique se seus JSONs contêm texto.")

if __name__ == "__main__":
    extract_and_flatten_json()