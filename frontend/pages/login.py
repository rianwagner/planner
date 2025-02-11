import streamlit as st
import requests

def show():
    st.title("📚 Planner Acadêmico")
    st.markdown("---")
    st.subheader("Login")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=200)

    with col2:
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")

        if st.button("Entrar", key="login_button"):
            if username and password:
                response = requests.post(
                    "http://localhost:5000/login",
                    json={"username": username, "password": password}
                )
                if response.status_code == 200:
                    st.session_state.token = response.json().get("access_token")
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")
            else:
                st.warning("Preencha todos os campos!")