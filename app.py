import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Finanças Casal", layout="centered")

# Simulação de Login simples (Para segurança real, usaríamos o st.secrets)
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if (user == "Bia" or user == "Lu") and password == "suasenha123":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")
        return False
    return True

if check_password():
    st.title("💰 Lançamento de Despesas")

    # Formulário de Cadastro
    with st.form("form_despesa", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            data = st.date_input("Data", datetime.now())
            tipo = st.selectbox("Tipo", ["FIXAS", "SAÚDE", "ESTUDOS", "VESTUÁRIO", "ACESSÓRIOS", "DIVERSOS", "LAZER", "PRESENTES", "INVESTIMENTOS"])
            descricao = st.text_input("Descrição")
            
        with col2:
            valor_total = st.number_input("Valor Total (R$)", min_value=0.0, step=0.01)
            parcelas = st.number_input("Qtd de Parcelas", min_value=1, value=1)
            pagamento = st.selectbox("Pagamento", ["CARTÃO CONJUNTA", "CARTÃO BIA", "CARTÃO LU", "DINHEIRO BIA", "DINHEIRO LU"])

        # Cálculo automático
        valor_parcela = valor_total / parcelas
        st.info(f"Valor da Parcela: R$ {valor_parcela:,.2f}")

        submit = st.form_submit_button("Cadastrar Despesa")

        if submit:
            # Aqui entrará a conexão com o banco de dados (ex: Google Sheets ou Supabase)
            st.success(f"Lançamento de '{descricao}' realizado com sucesso!")
