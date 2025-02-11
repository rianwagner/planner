import streamlit as st
from pages import login, materias, trabalhos, provas

st.sidebar.title("Menu")
if 'token' not in st.session_state:
    login.show()
else:
    page = st.sidebar.radio("Escolha uma opção:", ["Matérias", "Trabalhos", "Provas"])

    if page == "Matérias":
        materias.show()
    elif page == "Trabalhos":
        trabalhos.show()
    elif page == "Provas":
        provas.show()