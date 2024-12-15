
import streamlit as st
from src.chatbot import resposta_pergunta
from src.pdf import carregar_pdf


def rodar_interface():
    # Título e introdução
    st.title("Chatbot Normas de Segurança")
    st.markdown(
        """
        Bem-vindo ao Chatbot de Normas de Segurança Industrial! 
        Este assistente foi projetado para responder suas perguntas sobre normas de segurança em ambientes industriais 
        com base no documento "Workshop Rules and Safety Considerations".
        """
    )

    # Carregamento do contexto (PDF)
    url_pdf = "https://www.ku.edu.bh/wp-content/uploads/2016/09/Engineering-workshop-health-and-safety-guidelines-catalog.pdf"
    st.sidebar.header("Configurações")
    if "contexto" not in st.session_state:
        with st.spinner("Carregando documento de contexto..."):
            contexto = carregar_pdf(url_pdf)
            if "Erro" in contexto:
                st.session_state.contexto = None
                st.sidebar.error("Erro ao carregar o documento.")
            else:
                st.session_state.contexto = contexto

    # Verificação de carregamento do contexto
    if st.session_state.contexto:
        st.sidebar.success("Documento de contexto carregado com sucesso!")
        with st.expander("Visualizar Contexto do PDF"):
            st.text_area("Conteúdo do PDF", st.session_state.contexto, height=300)
    else:
        st.error("Não foi possível carregar o documento de contexto. Verifique o log para mais detalhes.")
        return

    # Histórico de mensagens na sessão
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibição do histórico de mensagens
    st.subheader("Chat")
    for message in st.session_state.messages:
        if message["role"] == "Usuário":
            with st.chat_message("Usuário"):
                st.markdown(f"**Você:** {message['content']}")
        elif message["role"] == "Chatbot":
            with st.chat_message("Chatbot"):
                st.markdown(f"**Chatbot:** {message['content']}")

    # Entrada de mensagem do usuário
    prompt = st.chat_input("Digite sua pergunta aqui...")
    if prompt:
        with st.chat_message("Usuário"):
            st.markdown(f"**Você:** {prompt}")

        # Processar a resposta
        with st.chat_message("Chatbot"):
            with st.spinner("Processando sua pergunta..."):
                resposta = resposta_pergunta(prompt, st.session_state.contexto)
                if not resposta or "Erro" in resposta:
                    st.error("Ocorreu um erro ao gerar a resposta. Tente novamente.")
                else:
                    st.markdown(f"**Chatbot:** {resposta}")

        # Atualizar o histórico de mensagens
        st.session_state.messages.append({"role": "Usuário", "content": prompt})
        st.session_state.messages.append({"role": "Chatbot", "content": resposta})

    # Botões adicionais no rodapé
    st.sidebar.subheader("Ações")
    if st.sidebar.button("Limpar Chat"):
        st.session_state.messages = []
        st.sidebar.success("Chat limpo com sucesso!")
    if st.sidebar.button("Baixar Histórico"):
        if st.session_state.messages:
            st.sidebar.download_button(
                "Baixar como JSON",
                data=str(st.session_state.messages),
                file_name="historico_chat.json",
                mime="application/json"
            )
        else:
            st.sidebar.warning("Nenhuma conversa para baixar ainda!")

