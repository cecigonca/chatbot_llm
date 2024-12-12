# import streamlit as st
# from src.chatbot import resposta_pergunta
# from src.pdf import carregar_pdf

# def rodar_interface():
#     st.title("Chatbot Normas de Segurança")
#     url_pdf = "https://www.ku.edu.bh/wp-content/uploads/2016/09/Engineering-workshop-health-and-safety-guidelines-catalog.pdf"
#     with st.spinner("Carregando arquivo de contexto..."):
#         contexto = carregar_pdf(url_pdf)
    
#     if "Erro" in contexto:
#         st.warning(contexto)
#     else:
#         st.text("O arquivo de contexto; 'Workshop rules and safety considerations' foi carregado.")
    
#     prompt = st.chat_input("Envie uma mensagem para o Chatbot")
#     if st.button("Enviar"):
#         if prompt.strip():
#             resposta = resposta_pergunta(prompt, contexto)
#             with st.chat_message("Usuário:"):
#                 st.markdown(prompt)
#             with st.chat_message("Chatbot"):
#                 st.write(resposta)
#         else:
#             st.error("Pergunta inválida! Por favor, digite uma pergunta válida.")

import streamlit as st
from src.chatbot import resposta_pergunta
from src.pdf import carregar_pdf

def rodar_interface():
    st.title("Chatbot Normas de Segurança")
    url_pdf = "https://www.ku.edu.bh/wp-content/uploads/2016/09/Engineering-workshop-health-and-safety-guidelines-catalog.pdf"
    with st.spinner("Carregando arquivo de contexto..."):
        contexto = carregar_pdf(url_pdf)
    
    if "Erro" in contexto:
        st.warning(contexto)
    else:
        st.text("O arquivo de contexto 'Workshop rules and safety considerations' foi carregado.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Área de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do usuário
    prompt = st.chat_input("Você:")

    # Processar a mensagem quando o usuário pressionar Enter
    if prompt:
        with st.chat_message("Usuário"):
            st.write(prompt)
        with st.chat_message("Chatbot"):
            with st.spinner("Processando sua pergunta..."):
                resposta = resposta_pergunta(prompt, contexto)
                st.write(resposta)

        # Adicionar a conversa ao histórico
        st.session_state.messages.append({"role": "Usuário", "content": prompt})
        st.session_state.messages.append({"role": "Chatbot", "content": resposta})

