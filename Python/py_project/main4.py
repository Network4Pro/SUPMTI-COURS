import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from aspose.words import Document

path_folder = ""
path_file_excel = ""

# Fonction pour choisir un dossier
def choose_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        global path_folder
        path_folder = folder_selected
    else:
        path_folder = None

# Fonction pour choisir un fichier Excel
def open_file_excel():
    excel_output_path = filedialog.askopenfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    global path_file_excel
    path_file_excel = excel_output_path

# Fonction pour extraire les tables d'un fichier Word (.doc)
def extract_tables_from_doc(file_path):
    try:
        doc = Document(file_path)
        tables = []

        for section in doc.sections:
            for body_node in section.get_child_nodes():
                if body_node.node_type == 7:  # Node type 7 corresponds to 'Body'
                    for table_node in body_node.get_child_nodes():
                        if table_node.node_type == 9:  # Node type 9 corresponds to 'Table'
                            table_data = []
                            for row_node in table_node.get_child_nodes():
                                if row_node.node_type == 10:  # Node type 10 corresponds to 'Row'
                                    row_data = [cell.to_string().strip() for cell in row_node.get_child_nodes()]
                                    table_data.append(row_data)
                            tables.append(table_data)

        return tables

    except Exception as e:
        print(f"An error occurred while extracting tables: {e}")
        return None




# Fonction pour sauvegarder les résultats
def save_results():
    # Vérifier si les chemins sont définis
    if not path_folder or not path_file_excel:
        print("Veuillez sélectionner un dossier et un fichier Excel.")
        return

    # Liste tous les fichiers dans le dossier avec l'extension .doc
    doc_files = [f for f in os.listdir(path_folder) if f.endswith('.doc')]

    # Boucle à travers chaque fichier .doc
    for doc_file in doc_files:
        # Construire le chemin complet du fichier .doc
        file_path = os.path.join(path_folder, doc_file)

        # Extraire les tables du fichier .doc
        tables = extract_tables_from_doc(file_path)

        if tables is not None:
            # Charger le fichier Excel existant dans un DataFrame
            existing_df = pd.read_excel(path_file_excel)

            # Parcourir chaque table extraite
            for table_data in tables:
                header = table_data[0]
                table_df = pd.DataFrame(table_data[1:], columns=header)

                # Ajouter de nouvelles lignes au DataFrame existant
                existing_df = pd.concat([existing_df, table_df], ignore_index=True, sort=False)

            # Enregistrer le DataFrame mis à jour dans le même fichier Excel
            existing_df.to_excel(path_file_excel, index=False)

            print(f'Nouvelles données ajoutées à {path_file_excel} à partir de {file_path}.')

# Interface utilisateur Tkinter
root = tk.Tk()
root.title("Extraction de tables depuis des fichiers Word (.doc)")

# Set the size of the window (width x height)
root.geometry("500x600")

btn_choose_folder = tk.Button(root, text="Choisir un dossier", command=choose_folder)
btn_choose_folder.pack(pady=10)

btn_open_file_excel = tk.Button(root, text="Ouvrir un fichier Excel", command=open_file_excel)
btn_open_file_excel.pack(pady=10)

btn_save_results = tk.Button(root, text="Sauvegarder les résultats", command=save_results)
btn_save_results.pack(pady=10)

root.mainloop()