import streamlit as st
import requests

def show():
    st.title("📝 Provas")
    st.markdown("---")

    if 'token' not in st.session_state:
        st.error("Você precisa estar logado para acessar esta página.")
        return

    token = st.session_state.token
    headers = {"Authorization": f"Bearer {token}"}

    # Lista de provas
    st.subheader("Lista de Provas")
    response = requests.get("http://localhost:5000/provas", headers=headers)
    if response.status_code == 200:
        provas = response.json()
        if provas:
            for prova in provas:
                with st.container():
                    st.markdown(f"""
                    **📖 {prova['titulo']}**  
                    Descrição: {prova['descricao']}  
                    Data: {prova['data']}  
                    Matéria ID: {prova['materia_id']}
                    """)
                    st.markdown("---")
        else:
            st.info("Nenhuma prova cadastrada.")
    else:
        st.error("Erro ao carregar provas.")

    # Adicionar nova prova
    st.subheader("Adicionar Prova")
    with st.form(key="add_prova_form"):
        titulo = st.text_input("Título da Prova", placeholder="Digite o título da prova")
        descricao = st.text_area("Descrição da Prova", placeholder="Digite a descrição da prova")
        data_prova = st.date_input("Data da Prova")
        materia_id = st.number_input("ID da Matéria", min_value=1, placeholder="Digite o ID da matéria")
        submit_button = st.form_submit_button("Adicionar Prova")

        if submit_button:
            if titulo and descricao and data_prova and materia_id:
                response = requests.post(
                    "http://localhost:5000/provas",
                    json={
                        "titulo": titulo,
                        "descricao": descricao,
                        "data": str(data_prova),  # Converte a data para string
                        "materia_id": materia_id
                    },
                    headers=headers
                )
                if response.status_code == 201:
                    st.success("Prova adicionada com sucesso!")
                    st.rerun()  # Recarrega a página para atualizar a lista
                else:
                    st.error("Erro ao adicionar prova.")
            else:
                st.warning("Preencha todos os campos!")