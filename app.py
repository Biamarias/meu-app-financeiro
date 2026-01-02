import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Gestão Financeira Bia & Lu", layout="wide")

# --- MENU LATERAL ---
st.sidebar.title("Navegação")
menu = st.sidebar.radio("Ir para:", ["CADASTRAR DESPESAS", "CADASTRAR ENTRADAS", "RELATÓRIO MENSAL", "CONTROLE GERAL"])

# --- FUNÇÃO DE LOGIN (Simples para uso próprio) ---
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("Acesso Restrito")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if (user.lower() in ["bia", "lu"]) and senha == "1234": # Escolha sua senha
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
else:
    # --- TELA: CADASTRAR DESPESAS ---
    if menu == "CADASTRAR DESPESAS":
        st.title("💸 Cadastrar Despesas")
        with st.form("form_despesa", clear_on_submit=True):
            data = st.date_input("Data", datetime.now())
            tipo = st.selectbox("Tipo", ["FIXAS", "SAÚDE", "ESTUDOS", "VESTUÁRIO", "ACESSÓRIOS", "DIVERSOS", "LAZER", "PRESENTES", "INVESTIMENTOS"])
            desc = st.text_input("Descrição")
            valor = st.number_input("Valor Total", min_value=0.0)
            parc = st.number_input("Qtd Parcelas", min_value=1, value=1)
            pagamento = st.selectbox("Pagamento", ["CARTÃO CONJUNTA", "CARTÃO BIA", "CARTÃO LU", "DINHEIRO BIA", "DINHEIRO LU"])
            
            valor_parc = valor / parc
            st.write(f"Valor da Parcela: R$ {valor_parc:.2f}")
            
            if st.form_submit_button("Cadastrar"):
                st.success("Despesa salva com sucesso!") # Aqui conectaremos a gravação depois

    # --- TELA: CADASTRAR ENTRADAS ---
    elif menu == "CADASTRAR ENTRADAS":
        st.title("💰 Cadastrar Entradas")
        with st.form("form_entrada", clear_on_submit=True):
            data_e = st.date_input("Data", datetime.now())
            tipo_e = st.selectbox("Tipo", ["Serviço principal", "Trabalho Extra", "Presente"])
            nome_e = st.selectbox("Nome", ["Bianca", "Lucas"])
            desc_e = st.text_input("Descrição")
            valor_e = st.number_input("Valor", min_value=0.0)
            
            if st.form_submit_button("Cadastrar Entrada"):
                st.success("Entrada salva!")

    # --- TELA: RELATÓRIO MENSAL ---
    elif menu == "RELATÓRIO MENSAL":
        st.title("📊 Relatório Mensal")
        mes_ref = st.selectbox("Selecione o Mês", ["JANEIRO/2026", "FEVEREIRO/2026", "MARÇO/2026"]) # Isso será automático depois
        
        # Simulação da visualização da sua imagem
        st.subheader(f"Resumo de {mes_ref}")
        col1, col2 = st.columns(2)
        col1.metric("Total Despesas", "R$ 8.940,58")
        col2.metric("Total Entradas", "R$ 10.500,00")
        
        st.markdown("---")
        st.write("### Detalhamento (Igual à sua foto)")
        # Aqui o código vai filtrar a planilha e mostrar a tabela formatada

    # --- TELA: CONTROLE GERAL ---
    elif menu == "CONTROLE GERAL":
        st.title("📈 Controle Geral")
        st.write("Visão anual e gráficos de gastos por categoria.")
