import os
import re
import locale
from PyPDF2 import PdfReader
from datetime import datetime

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def extract_info_from_pdf(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    num_pages = len(pdf_reader.pages)
    text = ""

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    date_pattern = r'\b(\d{1,2} de [a-z]+ de \d{4})\b'
    value_pattern = r'R\$ (\d{1,3}\.\d{3}|\d{1,3}),\d{2}'

    date_match = re.search(date_pattern, text, re.IGNORECASE)
    value_match = re.search(value_pattern, text)

    if date_match and value_match:
        corrida_date = date_match.group(1)
        corrida_value = value_match.group(0).replace("R$ ", "").replace(".", "").replace(",", ".")
        
        corrida_date = datetime.strptime(corrida_date, '%d de %B de %Y').strftime('%d-%m-%Y')
        
        return corrida_date, corrida_value
    else:
        return None, None

def rename_pdf_in_folder():
    folder_path = os.getcwd()
    print(f"Verificando arquivos na pasta: {folder_path}")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            print(f"Processando arquivo: {filename}")
            pdf_path = os.path.join(folder_path, filename)
            corrida_date, corrida_value = extract_info_from_pdf(pdf_path)
            
            if corrida_date and corrida_value:
                new_filename = f"{corrida_date}--{corrida_value}.pdf"
                new_path = os.path.join(folder_path, new_filename)
                os.rename(pdf_path, new_path)
                print(f"Arquivo '{filename}' renomeado para: '{new_filename}'")
            else:
                print(f"Informações de data ou valor não encontradas no arquivo '{filename}'.")

rename_pdf_in_folder()