import streamlit as st
import requests
from datetime import datetime

def show():
    st.title("📝 Provas")
    st.markdown("---")

    if 'token' not in st.session_state:
        st.error("Você precisa estar logado para acessar esta página.")
        return

    token = st.session_state.token
    headers = {"Authorization": f"Bearer {token}"}

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
                    
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        if st.button("✏️ Editar", key=f"editar_{prova['id']}"):
                            st.session_state.editando_prova_id = prova['id']
                            st.session_state.edit_titulo = prova['titulo']
                            st.session_state.edit_descricao = prova['descricao']
                            st.session_state.edit_data = prova['data']
                            st.session_state.edit_materia_id = prova['materia_id']

                    with col2:
                        if st.button("🗑️ Excluir", key=f"excluir_{prova['id']}"):
                            response = requests.delete(
                                f"http://localhost:5000/provas/{prova['id']}",
                                headers=headers
                            )
                            if response.status_code == 200:
                                st.success("Prova excluída!")
                                st.rerun()
                            else:
                                st.error("Erro ao excluir prova.")
                    st.markdown("---")
                    
        else:
            st.warning("Nenhuma prova encontrada.")
    else:
        st.error("Erro ao carregar provas.")
    
    if 'editando_prova_id' in st.session_state:
        st.subheader("Editar Prova")
        with st.form(key="edit_prova_form"):
            edit_titulo = st.text_input("Título", value=st.session_state.edit_titulo)
            edit_descricao = st.text_area("Descrição", value=st.session_state.edit_descricao)
            edit_data = st.date_input("Data", value=datetime.fromisoformat(st.session_state.edit_data))
            edit_materia_id = st.number_input("ID Matéria", value=st.session_state.edit_materia_id, min_value=1)
            
            if st.form_submit_button("Salvar Alterações"):
                response = requests.put(
                    f"http://localhost:5000/provas/{st.session_state.editando_prova_id}",
                    json={
                        "titulo": edit_titulo,
                        "descricao": edit_descricao,
                        "data": edit_data.isoformat(),
                        "materia_id": edit_materia_id
                    },
                    headers = {"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 200:
                    st.success("Prova atualizada!")
                    del st.session_state.editando_prova_id
                    st.rerun()
                else:
                    st.error("Erro ao atualizar.")
    
    st.subheader("Adicionar Prova")
    with st.form(key="add_prova_form"):
        titulo = st.text_input("Título da Prova", placeholder="Digite o título")
        descricao = st.text_area("Descrição da Prova", placeholder="Digite a descrição")
        data = st.date_input("Data da Prova")
        if data:
            data_str = data.strftime("%Y-%m-%d")
        materia_id = st.number_input("ID da Matéria", min_value=1, placeholder="Digite o ID da matéria")
        submit_button = st.form_submit_button("Adicionar Prova")

        if submit_button:
            if titulo and descricao and materia_id:
                response = requests.post(
                    "http://localhost:5000/provas",
                    json={"titulo": titulo, "descricao": descricao, "data": data_str, "materia_id": materia_id},
                    headers=headers
                )
                if response.status_code == 201:
                    st.success("Prova adicionada com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao adicionar prova.")
            else:
                st.warning("Preencha todos os campos!")
