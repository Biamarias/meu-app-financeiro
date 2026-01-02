import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Finanças Bia & Lu", page_icon="💰", layout="centered")

# 2. ESTILIZAÇÃO CSS
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    div.stButton > button {
        background-color: #99ff33; color: black; font-weight: bold;
        height: 5em; border-radius: 15px; border: 2px solid #7ecc29; margin-bottom: 10px;
    }
    .stSidebar .stButton > button { background-color: #f0f2f6; height: 3em; color: #31333F; }
    </style>
    """, unsafe_allow_html=True)

# 3. CONEXÃO COM O GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNÇÃO AUXILIAR PARA LER DADOS COM SEGURANÇA ---
def ler_dados(aba):
    try:
        # Tenta ler a aba específica
        return conn.read(worksheet=aba, ttl=0)
    except Exception as e:
        # Se der erro (como o HTTPError), retorna um DataFrame vazio com as colunas certas
        if aba == "Despesas":
            return pd.DataFrame(columns=["Data", "Tipo", "Descricao", "Valor_Total", "Parcelas", "Valor_Parcela", "Pagamento"])
        else:
            return pd.DataFrame(columns=["Data", "Tipo", "Nome", "Descricao", "Valor"])

# 4. CONTROLE DE ESTADO
if "logado" not in st.session_state:
    st.session_state.logado = False
if "tela" not in st.session_state:
    st.session_state.tela = "MENU"

# --- FLUXO DE ACESSO ---
if not st.session_state.logado:
    st.title("🔒 Acesso Restrito")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("ENTRAR"):
        if (user.lower() in ["bia", "lu"]) and senha == "1234":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
else:
    # Menu Principal
    if st.session_state.tela == "MENU":
        st.title("🏠 Menu Principal")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ CADASTRAR\nDESPESAS", use_container_width=True):
                st.session_state.tela = "DESPESAS"; st.rerun()
            if st.button("📊 RELATÓRIO\nMENSAL", use_container_width=True):
                st.session_state.tela = "RELATORIO"; st.rerun()
        with col2:
            if st.button("💰 CADASTRAR\nENTRADAS", use_container_width=True):
                st.session_state.tela = "ENTRADAS"; st.rerun()
            if st.button("📈 CONTROLE\nGERAL", use_container_width=True):
                st.session_state.tela = "CONTROLE"; st.rerun()

    if st.session_state.tela != "MENU":
        if st.sidebar.button("⬅️ VOLTAR AO MENU"):
            st.session_state.tela = "MENU"; st.rerun()

    # --- TELA: DESPESAS ---
    if st.session_state.tela == "DESPESAS":
        st.header("💸 Lançar Despesa")
        with st.form("form_despesas", clear_on_submit=True):
            data = st.date_input("Data", datetime.now())
            tipo = st.selectbox("Tipo", ["FIXAS", "SAÚDE", "ESTUDOS", "VESTUÁRIO", "ACESSÓRIOS", "DIVERSOS", "LAZER", "PRESENTES", "INVESTIMENTOS"])
            desc = st.text_input("Descrição")
            valor_total = st.number_input("Valor Total", min_value=0.0, step=0.01)
            parc = st.number_input("Qtd Parcelas", min_value=1, value=1)
            pag = st.selectbox("Pagamento", ["CARTÃO CONJUNTA", "CARTÃO BIA", "CARTÃO LU", "DINHEIRO BIA", "DINHEIRO LU"])
            v_parc = valor_total / parc
            st.info(f"Valor da Parcela: R$ {v_parc:.2f}")

            if st.form_submit_button("SALVAR DESPESA"):
                nova_d = pd.DataFrame([{
                    "Data": data.strftime('%d/%m/%Y'), "Tipo": tipo, "Descricao": desc,
                    "Valor_Total": valor_total, "Parcelas": parc, "Valor_Parcela": v_parc, "Pagamento": pag
                }])
                df_atual = ler_dados("Despesas") # Usa a função de leitura segura
                df_final = pd.concat([df_atual, nova_d], ignore_index=True)
                conn.update(worksheet="Despesas", data=df_final)
                st.success("Lançado com sucesso!")

    # --- TELA: ENTRADAS ---
    elif st.session_state.tela == "ENTRADAS":
        st.header("💰 Lançar Entrada")
        with st.form("form_entradas", clear_on_submit=True):
            data_e = st.date_input("Data", datetime.now())
            tipo_e = st.selectbox("Tipo", ["Serviço principal", "Trabalho Extra", "Presente"])
            nome_e = st.selectbox("Quem recebeu?", ["Bianca", "Lucas"])
            desc_e = st.text_input("Descrição")
            valor_e = st.number_input("Valor", min_value=0.0, step=0.01)

            if st.form_submit_button("SALVAR ENTRADA"):
                nova_e = pd.DataFrame([{
                    "Data": data_e.strftime('%d/%m/%Y'), "Tipo": tipo_e, "Nome": nome_e, "Descricao": desc_e, "Valor": valor_e
                }])
                df_e_atual = ler_dados("Entradas") # Usa a função de leitura segura
                df_e_final = pd.concat([df_e_atual, nova_e], ignore_index=True)
                conn.update(worksheet="Entradas", data=df_e_final)
                st.success("Entrada registrada!")

    # --- TELA: RELATÓRIO ---
    elif st.session_state.tela == "RELATORIO":
        st.header("📊 Relatório Mensal")
        df_ver = ler_dados("Despesas")
        st.dataframe(df_ver)
