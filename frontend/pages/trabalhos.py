import streamlit as st
import requests
from datetime import datetime

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
                    
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        if st.button("✏️ Editar", key=f"editar_{trabalho['id']}"):
                            st.session_state.editando_trabalho_id = trabalho['id']
                            st.session_state.edit_titulo = trabalho['titulo']
                            st.session_state.edit_descricao = trabalho['descricao']
                            st.session_state.edit_data_entrega = trabalho['data_entrega']
                            st.session_state.edit_materia_id = trabalho['materia_id']

                    with col2:
                        if st.button("🗑️ Excluir", key=f"excluir_{trabalho['id']}"):
                            response = requests.delete(
                                f"http://localhost:5000/trabalhos/{trabalho['id']}",
                                headers=headers
                            )
                            if response.status_code == 200:
                                st.success("Trabalho excluído!")
                                st.rerun()
                            else:
                                st.error("Erro ao excluir trabalho.")
                    
        else:
            st.warning("Nenhum trabalho encontrado.")
    else:
        st.error("Erro ao carregar trabalhos.")
    
    # Formulário de edição
    if 'editando_trabalho_id' in st.session_state:
        st.subheader("Editar Trabalho")
        with st.form(key="edit_trabalho_form"):
            edit_titulo = st.text_input("Título", value=st.session_state.edit_titulo)
            edit_descricao = st.text_area("Descrição", value=st.session_state.edit_descricao)
            edit_data_entrega = st.date_input("Data de Entrega", value=datetime.fromisoformat(st.session_state.edit_data_entrega))
            edit_materia_id = st.number_input("ID Matéria", value=st.session_state.edit_materia_id, min_value=1)
            
            if st.form_submit_button("Salvar Alterações"):
                response = requests.put(
                    f"http://localhost:5000/trabalhos/{st.session_state.editando_trabalho_id}",
                    json={
                        "titulo": edit_titulo,
                        "descricao": edit_descricao,
                        "data_entrega": edit_data_entrega.isoformat(),
                        "materia_id": edit_materia_id
                    },
                    headers = {"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 200:
                    st.success("Trabalho atualizado!")
                    del st.session_state.editando_trabalho_id
                    st.rerun()
                else:
                    st.error("Erro ao atualizar.")
    
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
