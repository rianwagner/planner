import streamlit as st
from pages import login, relatorio, materias, trabalhos, provas

def logout():
    del st.session_state['token']
    st.success("Você foi desconectado!")
    st.rerun()

if 'token' not in st.session_state:
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
