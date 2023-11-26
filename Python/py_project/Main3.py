from docx import Document
import pandas as pd
import os


def extract_tables_from_docx(file_path):
    doc = Document(file_path)
    tables = []

    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text)
            table_data.append(row_data)
        tables.append(table_data)

    return tables


# Spécifiez le chemin du dossier contenant les fichiers DOCX
docx_folder_path = './Les fichiers'
existing_excel_path = 'output3.xlsx'


# Liste tous les fichiers dans le dossier avec l'extension .docx
docx_files = [f for f in os.listdir(docx_folder_path) if f.endswith('.docx')]

# Boucle à travers chaque fichier DOCX
for docx_file in docx_files:
    # Construisez le chemin complet du fichier DOCX
    file_path = os.path.join(docx_folder_path, docx_file)
    
    # Extrait les tables du fichier DOCX
    tables = extract_tables_from_docx(file_path)

    # Chargez le fichier Excel existant dans un DataFrame
    existing_df = pd.read_excel(existing_excel_path)

    # Parcourez chaque table extraite
    for table_data in tables:
        header = table_data[0]  # Supposant que la première ligne contient les en-têtes de colonnes
        table_df = pd.DataFrame(table_data[1:], columns=header)
        
        # Ajoutez de nouvelles lignes au DataFrame existant
        existing_df = pd.concat([existing_df, table_df], ignore_index=True, sort=False)

    # Enregistrez le DataFrame mis à jour dans le même fichier Excel
    existing_df.to_excel(existing_excel_path, index=False)

    print(f'Nouvelles données ajoutées à {existing_excel_path} à partir de {file_path}.')
    
    
    