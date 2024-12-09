import google.generativeai as genai
import os

genai.api_key = os.getenv("GEMINI_API_KEY")

def resposta_pergunta(prompt, contexto):
    try:
        prompt_unificado = (
            "Você é um especialista em normas de segurança industrial.\n"
            f"Contexto: {contexto}\n\n"
            f"Pergunta: {prompt}"
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        resposta = model.generate_content(prompt_unificado)   
        
        return resposta.text.strip()
    except Exception as e:
        return f"Erro ao gerar a resposta: {e}"