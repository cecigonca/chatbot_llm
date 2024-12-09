import streamlit as st

def interface_chatbot(prompt):
    return "Resposta do chatbot: " + prompt

def rodar_interface():
    st.title("Chatbot Normas de Segurança")
    prompt = st.text_input("Envie uma mensagem para o Chatbot")
    if st.button("Enviar"):
        if prompt.strip():
            resposta = interface_chatbot(prompt)
            st.success(resposta)
        else:
            st.error("Pergunta inválida! Por favor, digite uma pergunta válida.")
            