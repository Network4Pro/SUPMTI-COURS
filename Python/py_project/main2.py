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

# Replace 'your_file.docx' with the path to your DOCX file
file_path = 'test.docx'
tables = extract_tables_from_docx(file_path)

# Load the existing Excel file into a DataFrame
existing_excel_path = 'output3.xlsx'
existing_df = pd.read_excel(existing_excel_path)

for table_data in tables:
    header = table_data[0]  # Assuming the first row contains column headers
    table_df = pd.DataFrame(table_data[1:], columns=header)
    
    # Append new rows to the existing DataFrame
    existing_df = pd.concat([existing_df, table_df], ignore_index=True, sort=False)

# Save the updated DataFrame back to the same Excel file
existing_df.to_excel(existing_excel_path, index=False)

print(f'New data added to {existing_excel_path}.')
