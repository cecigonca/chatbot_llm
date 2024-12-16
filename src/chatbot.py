import os
import google.generativeai as genai
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.gemini import Gemini

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def criar_llama_index():
    llm = Gemini(model= "models/gemini-1.5-pro")
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    documents = SimpleDirectoryReader(input_files=["data/normas_seguranca.pdf"]).load_data()
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model) # Criar o índice vetorial

    Settings.llm = llm
    Settings.embed_model = embed_model
    return index

def resposta_pergunta(llama_index, prompt):
    try:
        # query_engine para recuperar mais trechos
        query_engine = llama_index.as_query_engine(
            response_mode="no_text",
            similarity_top_k=8  # Recuperar até 8 trechos para aumentar o contexto disponível
        )
        response = query_engine.query(prompt)

        # trechos relevantes
        relevant_texts = [node.node.text for node in response.source_nodes]

        if not relevant_texts:
            return "Nenhum contexto encontrado no índice."

        contexto = "\n\n".join(set(relevant_texts[:5]))

        SISTEMA_PROMPT = (
            "Você é um especialista em normas de segurança industrial. "
            "Responda a todas as perguntas em português, mesmo que elas sejam feitas em outro idioma. "
            "Se não houver informações suficientes no contexto, diga que não há dados suficientes.\n\n"
        )

        prompt_unificado = f"{SISTEMA_PROMPT}CONTEXTO:\n{contexto}\n\nPERGUNTA: {prompt}\nRESPOSTA:"

        model = genai.GenerativeModel("gemini-1.5-pro")
        resposta_llm = model.generate_content(prompt_unificado)

        return resposta_llm.text.strip()

    except Exception as e:
        return f"Erro ao gerar a resposta: {e}"
