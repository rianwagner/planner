import streamlit as st
import requests

def show():
    st.title("📚 Matérias")
    st.markdown("---")

    if 'token' not in st.session_state:
        st.error("Você precisa estar logado para acessar esta página.")
        return

    token = st.session_state.token
    headers = {"Authorization": f"Bearer {token}"}

    # Lista de matérias
    st.subheader("Lista de Matérias")
    response = requests.get("http://localhost:5000/materias", headers=headers)
    if response.status_code == 200:
        materias = response.json()
        if materias:
            for materia in materias:
                with st.container():
                    st.markdown(f"""
                    **📖 {materia['nome']}**  
                    ID: {materia['id']}
                    """)
                    st.markdown("---")
        else:
            st.info("Nenhuma matéria cadastrada.")
    else:
        st.error("Erro ao carregar matérias.")

    # Adicionar nova matéria
    st.subheader("Adicionar Matéria")
    with st.form(key="add_materia_form"):
        nome = st.text_input("Nome da Matéria", placeholder="Digite o nome da matéria")
        submit_button = st.form_submit_button("Adicionar Matéria")

        if submit_button:
            if nome:
                response = requests.post(
                    "http://localhost:5000/materias",
                    json={"nome": nome},
                    headers=headers
                )
                if response.status_code == 201:
                    st.success("Matéria adicionada com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao adicionar matéria.")
            else:
                st.warning("Preencha o nome da matéria!")