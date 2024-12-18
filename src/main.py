import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.chatbot import criar_llama_index, resposta_pergunta

def gerar_resposta_com_streaming(resposta_completa, delay=0.05):
    for caractere in resposta_completa:
        yield caractere  # Retorna um caractere por vez
        time.sleep(delay)  # Atraso para efeito de digitação

def rodar_interface():
    st.title("Chatbot Normas de Segurança")

    # Carregar índice LlamaIndex apenas uma vez
    if "llama_index" not in st.session_state:
        with st.spinner("Carregando documento e criando índice..."):
            st.session_state.llama_index = criar_llama_index()
        st.success("Documento e índice carregados com sucesso!")
    if st.session_state.llama_index is None:
        st.error("Não foi possível criar o índice.")
        return

    with st.expander("Visualizar PDF de contexto"):
        doc_ids = list(st.session_state.llama_index.docstore.docs.keys())
        if doc_ids:
            doc0 = st.session_state.llama_index.docstore.docs[doc_ids[0]]
            conteudo = doc0.get_text()
            st.text(f"{conteudo[:1000]}")
        else:
            st.warning("Nenhum documento encontrado no índice!")

    # Histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        if msg["role"] == "Usuário":
            with st.chat_message("Usuário"):
                st.markdown(f"**Você:** {msg['content']}")
        else:
            with st.chat_message("Chatbot"):
                st.markdown(f"**Chatbot:** {msg['content']}")

    # Captura e resposta de pergunta
    prompt = st.chat_input("Digite sua pergunta aqui...")
    if prompt:
        with st.chat_message("Usuário"):
            st.markdown(f"**Você:** {prompt}")

        with st.chat_message("Chatbot"):
            with st.spinner("Processando sua pergunta..."):
                resposta = resposta_pergunta(st.session_state.llama_index, prompt)
                if not resposta or resposta.startswith("Erro"):
                    st.error("Ocorreu um erro ao gerar a resposta. Tente novamente.")
                else:
                    response_placeholder = st.empty()
                    streamed_response = ""
                    for token in gerar_resposta_com_streaming(resposta, delay=0.01):
                        streamed_response += token
                        # Atualizar a resposta no placeholder
                        response_placeholder.write(f"**Chatbot:** {streamed_response}")

        st.session_state.messages.append({"role": "Usuário", "content": prompt})
        st.session_state.messages.append({"role": "Chatbot", "content": resposta})

if __name__ == "__main__":
    rodar_interface()