import streamlit as st
from pages import login, register, relatorio, materias, trabalhos, provas

def logout():
    for key in ['token', 'show_register']:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Você foi desconectado!")
    st.rerun()

if 'show_register' not in st.session_state:
    st.session_state.show_register = False

if 'token' not in st.session_state:
    if st.session_state.show_register:
        register.show()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Faça login!", type="secondary"):
            st.session_state.show_register = False
            st.rerun()
    else:
        login.show()
else:
    if st.button("🚪 Sair"):
        logout()

    st.markdown("""
        <style>
            .stSelectbox, .stRadio {
                background-color: #f0f4f8;
                padding: 10px;
                border-radius: 8px;
            }
            .stSelectbox label {
                font-size: 16px;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    menu = st.selectbox("Escolha uma página:", ["Relatório", "Trabalhos", "Provas", "Matérias"])

    if menu == "Relatório":
        relatorio.show()
    elif menu == "Trabalhos":
        trabalhos.show()
    elif menu == "Provas":
        provas.show()
    elif menu == "Matérias":
        materias.show()