import os
import fitz  # PyMuPDF
from docx import Document as DocxDocument

# Caminho para as pastas de dados
pdf_dir = "data/pdf"
word_dir = "data/word"

# Função para ler todos os arquivos PDF da pasta especificada
def read_pdf_files(directory):
    all_texts = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text("text")
            all_texts.append(text)
    return all_texts

# Função para ler todos os arquivos Word da pasta especificada
def read_word_files(directory):
    all_texts = []
    for filename in os.listdir(directory):
        if filename.endswith(".docx"):
            filepath = os.path.join(directory, filename)
            doc = DocxDocument(filepath)
            text = " ".join([para.text for para in doc.paragraphs])
            all_texts.append(text)
    return all_texts
