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
                    
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        if st.button("✏️ Editar", key=f"editar_{materia['id']}"):
                            st.session_state.editando_materia_id = materia['id']
                            st.session_state.edit_nome = materia['nome']

                    with col2:
                        if st.button("🗑️ Excluir", key=f"excluir_{materia['id']}"):
                            response = requests.delete(
                                f"http://localhost:5000/materias/{materia['id']}",
                                headers=headers
                            )
                            if response.status_code == 200:
                                st.success("Matéria excluída!")
                                st.rerun()
                            else:
                                st.error("Erro ao excluir matéria.")
        else:
            st.info("Nenhuma matéria cadastrada.")
    else:
        st.error("Erro ao carregar matérias.")

    # Formulário de edição
    if 'editando_materia_id' in st.session_state:
        st.subheader("Editar Matéria")
        with st.form(key="edit_materia_form"):
            edit_nome = st.text_input("Nome", value=st.session_state.edit_nome)
            
            if st.form_submit_button("Salvar Alterações"):
                response = requests.put(
                    f"http://localhost:5000/materias/{st.session_state.editando_materia_id}",
                    json={
                        "nome": edit_nome
                    },
                    headers = {"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 200:
                    st.success("Matéria atualizada com sucesso!")
                    del st.session_state.editando_materia_id
                    st.rerun()
                else:
                    st.error("Erro ao atualizar matéria.")
    
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
