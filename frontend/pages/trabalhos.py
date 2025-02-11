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

    st.subheader("Lista de Trabalhos")
    response = requests.get("http://localhost:5000/trabalhos", headers=headers)
    if response.status_code == 200:
        trabalhos = response.json()
        if trabalhos:
            for trabalho in trabalhos:
                with st.container():
                    st.markdown(f"""
                    **📖 {trabalho['titulo']}**  
                    Descrição: {trabalho['descricao']}  
                    Data: {trabalho['data_entrega']}  
                    Matéria ID: {trabalho['materia_id']}
                    """)
                    st.markdown("---")
        else:
            st.info("Nenhuma prova cadastrada.")
    else:
        st.error("Erro ao carregar provas.")

    # Formulário para adicionar trabalho
    st.subheader("Adicionar Trabalho")
    with st.form(key="add_trabalho_form"):
        titulo = st.text_input("Título do Trabalho", placeholder="Digite o título")
        descricao = st.text_area("Descrição do Trabalho", placeholder="Digite a descrição")
        data_entrega = st.date_input("Data de Entrega")
        if data_entrega:
            data_entrega_str = data_entrega.strftime("%Y-%m-%d")
        materia_id = st.number_input("ID da Matéria", min_value=1, placeholder="Digite o ID da matéria")
        submit_button = st.form_submit_button("Adicionar Trabalho")

        if submit_button:
            if titulo and descricao and materia_id:
                response = requests.post(
                    "http://localhost:5000/trabalhos",
                    json={"titulo": titulo, "descricao": descricao, "data_entrega": data_entrega_str, "materia_id": materia_id},
                    headers=headers
                )
                if response.status_code == 201:
                    st.success("Trabalho adicionado com sucesso!")
                else:
                    st.error("Erro ao adicionar trabalho.")
            else:
                st.warning("Preencha todos os campos!")