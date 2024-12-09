import openai

# gopenai.api_key = ""

def resposta_pergunta(prompt, contexto):
    mensagem = [
        {"role": "system", "content": "Você é um especialista em normas de segurança industrial."},
        {"role": "user", "content": f"Contexto: {contexto}\n\nPergunta: {prompt}"}
    ]
    resposta = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = mensagem,
        temperature = 0.7,
        max_tokens = 200
    )
    return resposta.choices[0].message['content'].strip()