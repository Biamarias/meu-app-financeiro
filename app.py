import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Finanças Bia & Lu", page_icon="💰")

# Pegar o link dos Secrets (deve ser o link normal da planilha)
# Ex: https://docs.google.com/spreadsheets/d/ID_DA_PLANILHA/edit
url_base = st.secrets["connections"]["gsheets"]["spreadsheet"]

# Função para converter o link normal em link de dados (CSV)
def get_csv_url(url, sheet_name):
    base = url.split("/edit")[0]
    sheet_name_parsed = urllib.parse.quote(sheet_name)
    return f"{base}/gviz/tq?tqx=out:csv&sheet={sheet_name_parsed}"

# Função para ler dados sem frescura
def ler_dados(aba):
    try:
        csv_url = get_csv_url(url_base, aba)
        return pd.read_csv(csv_url)
    except:
        if aba == "Despesas":
            return pd.DataFrame(columns=["Data", "Tipo", "Descricao", "Valor_Total", "Parcelas", "Valor_Parcela", "Pagamento"])
        return pd.DataFrame(columns=["Data", "Tipo", "Nome", "Descricao", "Valor"])

# --- LOGIN E NAVEGAÇÃO (Igual ao anterior) ---
if "logado" not in st.session_state: st.session_state.logado = False
if "tela" not in st.session_state: st.session_state.tela = "MENU"

if not st.session_state.logado:
    st.title("🔒 Acesso")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("ENTRAR"):
        if user.lower() in ["bia", "lu"] and senha == "1234":
            st.session_state.logado = True
            st.rerun()
else:
    if st.session_state.tela == "MENU":
        st.title("🏠 Menu")
        c1, c2 = st.columns(2)
        if c1.button("➕ DESPESAS", use_container_width=True): st.session_state.tela = "DESPESAS"; st.rerun()
        if c2.button("💰 ENTRADAS", use_container_width=True): st.session_state.tela = "ENTRADAS"; st.rerun()
        if c1.button("📊 RELATÓRIO", use_container_width=True): st.session_state.tela = "RELATORIO"; st.rerun()
    
    if st.session_state.tela != "MENU":
        if st.sidebar.button("⬅️ VOLTAR"): st.session_state.tela = "MENU"; st.rerun()

    if st.session_state.tela == "DESPESAS":
        st.header("💸 Lançar Despesa")
        # O formulário de cadastro continua aqui igual...
        with st.form("f1"):
            # (Campos de entrada aqui)
            if st.form_submit_button("SALVAR"):
                st.info("Para salvar agora com esse método, usaremos uma Google Form ou API simples. Quer que eu configure o link do Form para você?")

    elif st.session_state.tela == "RELATORIO":
        st.header("📊 Seus Lançamentos")
        dados = ler_dados("Despesas")
        st.dataframe(dados)
