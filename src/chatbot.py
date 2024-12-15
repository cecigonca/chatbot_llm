import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("GEMINI_API_KEY")) 
genai.api_key = os.getenv("GEMINI_API_KEY")

def resposta_pergunta(prompt, contexto):
    try:
        prompt_unificado = (
            "Você é um especialista em normas de segurança industrial. Responda de forma clara e objetiva, com base exclusivamente no contexto fornecido. Não invente informações.\n"
            f"Contexto: {contexto}\n\n"
            f"Pergunta: {prompt}"
        )
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        resposta = model.generate_content(prompt_unificado)   
        
        return resposta.text.strip()
    except Exception as e:
        return f"Erro ao gerar a resposta: {e}"