import streamlit as st
from src.chatbot import resposta_pergunta
from src.pdf import carregar_pdf

def interface_chatbot(prompt):
    return "Resposta do chatbot: " + prompt

def rodar_interface():
    st.title("Chatbot Normas de Segurança")
    caminho_pdf = "./docs/normas_seguranca.pdf"
    contexto = carregar_pdf(caminho_pdf)
    prompt = st.text_input("Envie uma mensagem para o Chatbot")
    if st.button("Enviar"):
        if prompt.strip():
            resposta = resposta_pergunta(prompt, contexto)
            st.success(resposta)
        else:
            st.error("Pergunta inválida! Por favor, digite uma pergunta válida.")