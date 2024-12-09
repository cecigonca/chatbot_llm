from gpt4all import GPT4All
import os

caminho_modelo = "./models/gpt4all-lora-quantized.bin"

if not os.path.exists(caminho_modelo):
    raise FileNotFoundError("Modelo não encontrado em {caminho_modelo}.")

def resposta_pergunta(prompt, contexto):
    modelo = GPT4All(model_name="gpt4all-lora-quantized", model_path=caminho_modelo)
    mensagem = f"Você é um especialista em normas de segurança industrial. \n\nContexto: {contexto}\n\npergunta: {prompt}"
    resposta = modelo.generate(mensagem)
    return resposta.strip()