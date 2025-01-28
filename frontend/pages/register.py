import streamlit as st
import requests

def show():
    st.title("📚 Planner Acadêmico")
    st.markdown("---")
    st.subheader("Registrar Usuário")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/747/747545.png", width=100)  # Ícone de registro

    with col2:
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        confirm_password = st.text_input("Confirme a Senha", type="password", placeholder="Confirme sua senha")

        if st.button("Registrar", key="register_button"):
            if username and password and confirm_password:
                if password == confirm_password:
                    response = requests.post(
                        "http://localhost:5000/register",
                        json={"username": username, "password": password}
                    )
                    if response.status_code == 201:
                        st.success("Usuário registrado com sucesso! Faça login para continuar.")
                    elif response.status_code == 409:
                        st.error("Usuário já existe. Tente um nome de usuário diferente.")
                    else:
                        st.error("Erro ao registrar o usuário. Tente novamente.")
                else:
                    st.warning("As senhas não coincidem!")
            else:
                st.warning("Preencha todos os campos!")

if __name__ == "__main__":
    show()
