import requests
import io
import pdfplumber
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from llama_index.llms import Gemini
from llama_index.core import Settings
import os

# Certifique-se de que os dados necessários do NLTK estejam baixados
nltk.download("punkt")

class RAG:
    def __init__(self, pdf_url):
        self.pdf_url = pdf_url
        self.contexto = None
        self.index = None

        # Inicializar e carregar o PDF
        self._carregar_e_indexar_pdf()

    def _carregar_pdf(self):
        """
        Carrega o conteúdo do PDF a partir de uma URL.
        """
        try:
            resposta = requests.get(self.pdf_url)
            arquivo_pdf = io.BytesIO(resposta.content)

            # Abrir e extrair texto do PDF
            with pdfplumber.open(arquivo_pdf) as pdf:
                texto = ""
                for page in pdf.pages:
                    texto += page.extract_text()

            return texto.strip() if texto else "Erro: O PDF está vazio ou não pode ser lido."
        except requests.exceptions.RequestException as e:
            return f"Erro ao baixar o PDF: {e}"
        except Exception as e:
            return f"Erro ao processar o PDF: {e}"

    def _tokenizar_contexto(self, texto):
        """
        Divide o texto em sentenças usando o NLTK.
        """
        return sent_tokenize(texto)

    def _carregar_e_indexar_pdf(self):
        """
        Carrega o PDF e cria o índice usando LlamaIndex.
        """
        # Carregar o texto do PDF
        self.contexto = self._carregar_pdf()
        if "Erro" not in self.contexto:
            # Tokenizar o contexto em sentenças
            sentencas = self._tokenizar_contexto(self.contexto)
            
            # Criar documentos para LlamaIndex
            documentos = [Document(text=sentenca) for sentenca in sentencas]

            # Configurar o modelo LLM para uso no índice
            llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))
            service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

            # Criar o índice
            self.index = VectorStoreIndex.from_documents(documentos, service_context=service_context)
        else:
            raise Exception(self.contexto)

    def buscar_contexto(self, pergunta, top_k=3):
        """
        Busca as sentenças mais relevantes para a pergunta no índice.
        """
        if not self.index:
            raise Exception("O índice não foi inicializado corretamente.")

        # Consultar o índice
        resposta = self.index.query(pergunta, similarity_top_k=top_k)
        return resposta.response
