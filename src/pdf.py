import pdfplumber
import requests
import io

def carregar_pdf(caminho_ou_url):
    try:
        caminho_ou_url.startswith("http")
        resposta = requests.get(caminho_ou_url)
        arquivo_pdf = io.BytesIO(resposta.content)


        # Abrir e extrair texto do PDF
        with pdfplumber.open(arquivo_pdf) as pdf:
            texto = ""
            for page in pdf.pages:
                texto += page.extract_text()
        
        return texto.strip() if texto else "Erro: O PDF está vazio ou não pode ser lido."
    except requests.exceptions.RequestException as e:
        return f"Erro ao baixar o PDF: {e}"
    except FileNotFoundError:
        return "Erro: Arquivo PDF não encontrado."
    except Exception as e:
        return f"Erro ao processar o PDF: {e}"
    
    