import streamlit as st
import requests

def show():
    st.title("📝 Trabalhos")
    st.markdown("---")

    if 'token' not in st.session_state:
        st.error("Você precisa estar logado para acessar esta página.")
        return

    token = st.session_state.token
    headers = {"Authorization": f"Bearer {token}"}

    # Formulário para adicionar trabalho
    st.subheader("Adicionar Trabalho")
    with st.form(key="add_trabalho_form"):
        titulo = st.text_input("Título do Trabalho", placeholder="Digite o título")
        descricao = st.text_area("Descrição do Trabalho", placeholder="Digite a descrição")
        data_entrega = st.date_input("Data de Entrega")
        materia_id = st.number_input("ID da Matéria", min_value=1, placeholder="Digite o ID da matéria")
        submit_button = st.form_submit_button("Adicionar Trabalho")

        if submit_button:
            if titulo and descricao and materia_id:
                response = requests.post(
                    "http://localhost:5000/trabalhos",
                    json={"titulo": titulo, "descricao": descricao, "data_entrega": data_entrega, "materia_id": materia_id},
                    headers=headers
                )
                if response.status_code == 201:
                    st.success("Trabalho adicionado com sucesso!")
                else:
                    st.error("Erro ao adicionar trabalho.")
            else:
                st.warning("Preencha todos os campos!")