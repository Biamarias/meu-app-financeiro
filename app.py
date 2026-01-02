import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Finanças Bia & Lu", layout="wide")

# --- CONEXÃO COM O GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LOGIN ---
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("🔒 Acesso Restrito")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if (user.lower() in ["bia", "lu"]) and senha == "1234": # Altere sua senha aqui
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
else:
    # --- MENU LATERAL ---
    menu = st.sidebar.radio("Navegação", ["CADASTRAR DESPESAS", "CADASTRAR ENTRADAS", "RELATÓRIO MENSAL", "CONTROLE GERAL"])

    # --- TELA: CADASTRAR DESPESAS ---
    if menu == "CADASTRAR DESPESAS":
        st.header("💸 Lançar Despesa")
        with st.form("form_despesas", clear_on_submit=True):
            data = st.date_input("Data", datetime.now())
            tipo = st.selectbox("Tipo", ["FIXAS", "SAÚDE", "ESTUDOS", "VESTUÁRIO", "ACESSÓRIOS", "DIVERSOS", "LAZER", "PRESENTES", "INVESTIMENTOS"])
            desc = st.text_input("Descrição")
            valor_total = st.number_input("Valor Total", min_value=0.0, step=0.01)
            parcelas = st.number_input("Quantidade de Parcelas", min_value=1, value=1)
            pagamento = st.selectbox("Pagamento", ["CARTÃO CONJUNTA", "CARTÃO BIA", "CARTÃO LU", "DINHEIRO BIA", "DINHEIRO LU"])
            
            valor_parcela = valor_total / parcelas
            st.info(f"Valor da Parcela: R$ {valor_parcela:.2f}")
            
            if st.form_submit_button("Cadastrar"):
                nova_linha = pd.DataFrame([{
                    "Data": data.strftime('%d/%m/%Y'), "Tipo": tipo, "Descricao": desc,
                    "Valor_Total": valor_total, "Parcelas": parcelas, 
                    "Valor_Parcela": valor_parcela, "Pagamento": pagamento
                }])
                # Adiciona na aba 'Despesas' da sua planilha
                existing_data = conn.read(worksheet="Despesas")
                updated_df = pd.concat([existing_data, nova_linha], ignore_index=True)
                conn.update(worksheet="Despesas", data=updated_df)
                st.success("Despesa cadastrada!")

    # --- TELA: CADASTRAR ENTRADAS ---
    elif menu == "CADASTRAR ENTRADAS":
        st.header("💰 Lançar Entrada")
        with st.form("form_entradas", clear_on_submit=True):
            data_e = st.date_input("Data", datetime.now())
            tipo_e = st.selectbox("Tipo", ["Serviço principal", "Trabalho Extra", "Presente"])
            nome_e = st.selectbox("Nome", ["Bianca", "Lucas"])
            desc_e = st.text_input("Descrição")
            valor_e = st.number_input("Valor", min_value=0.0, step=0.01)
            
            if st.form_submit_button("Cadastrar Entrada"):
                nova_entrada = pd.DataFrame([{
                    "Data": data_e.strftime('%d/%m/%Y'), "Tipo": tipo_e, 
                    "Nome": nome_e, "Descricao": desc_e, "Valor": valor_e
                }])
                existing_entradas = conn.read(worksheet="Entradas")
                updated_ent = pd.concat([existing_entradas, nova_entrada], ignore_index=True)
                conn.update(worksheet="Entradas", data=updated_ent)
                st.success(f"Entrada de {nome_e} salva!")

    # --- TELA: RELATÓRIO MENSAL ---
    elif menu == "RELATÓRIO MENSAL":
        st.header("📊 Relatórios")
        # Aqui ele lê a planilha para mostrar o que já foi cadastrado
        df_despesas = conn.read(worksheet="Despesas")
        st.write("### Suas Despesas Lançadas")
        st.dataframe(df_despesas)
