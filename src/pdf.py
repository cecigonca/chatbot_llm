import PyPDF2

def carregar_pdf(caminho_pdf):
    try:
        with open(caminho_pdf, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            texto = ""
            for page in reader.pages:
                texto += page.extract_text()
        return texto
    except FileNotFoundError:
        return "Erro: Arquivo PDF não encontrado."
    except Exception as e:
        return f"Erro ao carregar o PDF: {e}"