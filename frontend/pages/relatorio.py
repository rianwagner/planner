import streamlit as st
import requests
from datetime import datetime, timedelta

def show():
    st.title("📊 Relatório de Provas e Trabalhos")
    st.markdown("---")

    if 'token' not in st.session_state:
        st.error("Você precisa estar logado para acessar esta página.")
        return

    token = st.session_state.token
    headers = {"Authorization": f"Bearer {token}"}

    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input("Data Início", 
                                   value=datetime.now().date(),
                                   min_value=datetime.now().date() - timedelta(days=365*2))
    with col2:
        data_fim = st.date_input("Data Fim", 
                                value=datetime.now().date() + timedelta(days=180),
                                min_value=data_inicio)

    if st.button("Gerar Relatório"):
        params = {
            'data_inicio': data_inicio.strftime("%Y-%m-%d"),
            'data_fim': data_fim.strftime("%Y-%m-%d")
        }
        
        response = requests.get("http://localhost:5000/api/relatorio", 
                              headers=headers,
                              params=params)
        
        if response.status_code == 200:
            dados = response.json()

            if 'relatorio' in dados:
                for materia in dados['relatorio']:
                    with st.expander(f"📚 {materia['materia_nome']}"):
                        # Seção de Provas
                        if 'provas' in materia and materia['provas']:
                            st.subheader("📝 Provas")
                            for prova in materia['provas']:
                                st.markdown(f"""
                                **{prova['titulo']}**  
                                Data: {prova['data']}  
                                {prova['descricao']}
                                """)
                                st.markdown("---")
                        else:
                            st.info("Nenhuma prova encontrada para o período selecionado.")
                        
                        if 'trabalhos' in materia and materia['trabalhos']:
                            st.subheader("📘 Trabalhos")
                            for trabalho in materia['trabalhos']:
                                st.markdown(f"""
                                **{trabalho['titulo']}**  
                                Data de Entrega: {trabalho['data']}  
                                {trabalho['descricao']}
                                """)
                                st.markdown("---")
                        else:
                            st.info("Nenhum trabalho encontrado para o período selecionado.")
            else:
                st.error("Erro ao carregar o relatório. Estrutura de dados inválida.")
        else:
            st.error("Erro ao gerar relatório. Tente novamente.")