import json
import csv
import os

# =========================================================
# CONFIGURAÇÕES
# =========================================================
INPUT_FILE = 'Translation/Universe_for_Sale_PTBR_Workfile.csv' # Seu arquivo CSV traduzido
SOURCE_FOLDER = 'Source'  # JSONs originais (para carregar a estrutura)
OUTPUT_FOLDER = 'Output'  # Onde os JSONs traduzidos serão salvos
# =========================================================

def load_translations():
    """Carrega o CSV de tradução para um dicionário de busca rápida."""
    
    translations = {}
    try:
        # Abre o CSV (usando vírgula como delimitador)
        with open(INPUT_FILE, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                # Usa File_ID como chave e a tradução como valor
                # Ele só armazena se houver texto traduzido para evitar strings vazias
                translated_text = row.get('Translation_PTBR', '').strip()
                if translated_text:
                    translations[row['File_ID']] = translated_text
        return translations
    except FileNotFoundError:
        print(f"Erro: Arquivo CSV não encontrado em {INPUT_FILE}. Verifique o caminho.")
        return None

def recursive_replace(data, path, translations, filename):
    """Função recursiva para encontrar strings originais e substituí-las pela tradução."""
    
    # 1. Checa se o item atual é uma string de texto
    if isinstance(data, str) and data.strip():
        # Gera o ID de busca
        unique_id = f"{filename}_{path}"
        
        # Procura a tradução
        translated_text = translations.get(unique_id)
        
        # 2. Se a tradução existir, retorna a tradução.
        if translated_text:
            return translated_text
        # Caso contrário, mantém o texto original (data).
        return data
    
    # 3. Itera em Estruturas Aninhadas (Dicionários e Listas)
    elif isinstance(data, dict):
        new_data = data.copy()
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            new_data[key] = recursive_replace(value, new_path, translations, filename)
        return new_data
    
    elif isinstance(data, list):
        new_data = []
        for index, item in enumerate(data):
            new_path = f"{path}[{index}]"
            new_data.append(recursive_replace(item, new_path, translations, filename))
        return new_data
        
    return data # Retorna o item se não for str, dict ou list

def build_translated_jsons():
    """Coordena o processo de construção dos JSONs."""
    
    translations = load_translations()
    if translations is None:
        return

    print("Iniciando a reconstrução dos JSONs traduzidos...")
    # Garante que a pasta 'Output' existe
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    for filename in os.listdir(SOURCE_FOLDER):
        if filename.endswith('.json'):
            source_filepath = os.path.join(SOURCE_FOLDER, filename)
            output_filepath = os.path.join(OUTPUT_FOLDER, filename)
            
            try:
                # 1. Carrega a estrutura JSON original (do Source)
                with open(source_filepath, 'r', encoding='utf-8') as f:
                    original_data = json.load(f)
            except Exception as e:
                print(f"Erro ao carregar {filename}: {e}")
                continue
            
            # 2. Substitui as strings recursivamente
            translated_data = recursive_replace(original_data, "", translations, filename)
            
            # 3. Salva o novo JSON traduzido na pasta 'Output'
            with open(output_filepath, 'w', encoding='utf-8') as f:
                # Usa indent=None para manter o JSON compacto, como o original
                json.dump(translated_data, f, ensure_ascii=False)
            
            print(f"  [SUCESSO] Reconstruído: {filename}")
    
    print("\nProcesso de reversão concluído. JSONs traduzidos estão na pasta 'Output/'.")

if __name__ == "__main__":
    build_translated_jsons()