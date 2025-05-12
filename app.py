import streamlit as st
import pandas as pd
import os
from datetime import date
from database import criar_tabela, inserir_transacao, listar_transacoes

criar_tabela()

ARQUIVO = 'transacoes.csv'

def salvar_transacao(tipo, valor, categoria, data, descricao):
    nova = pd.DataFrame([[tipo, valor, categoria, data, descricao]], 
                        columns=["Tipo", "Valor", "Categoria", "Data", "Descrição"])
    if os.path.exists(ARQUIVO):
        df = pd.read_csv(ARQUIVO)
        df = pd.concat([df, nova], ignore_index=True)
    else:
        df = nova
    df.to_csv(ARQUIVO, index=False)

def carregar_dados():
    if os.path.exists(ARQUIVO):
        return pd.read_csv(ARQUIVO)
    return pd.DataFrame(columns=["Tipo", "Valor", "Categoria", "Data", "Descrição"])

st.title("💰 Aplicativo de Gestão Financeira")

# Criação das abas
aba1, aba2, aba3 = st.tabs(["➕ Registrar", "📋 Transações", "📊 Relatórios"])
with aba1:
    st.subheader("Registrar Nova Transação")
    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
    valor = st.number_input("Valor", min_value=0.01)
    categoria = st.text_input("Categoria")
    data = st.date_input("Data", value=date.today())
    descricao = st.text_input("Descrição")

    if st.button("Salvar"):
        inserir_transacao(tipo, valor, categoria, str(data), descricao)
        st.success("Transação salva com sucesso!")


with aba2:
    st.subheader("Transações Registradas")
    dados = listar_transacoes()
    if not dados:
        st.info("Nenhuma transação registrada.")
    else:
        df = pd.DataFrame(dados, columns=["ID", "Tipo", "Valor", "Categoria", "Data", "Descrição"])
        st.dataframe(df.sort_values(by="Data", ascending=False))


with aba3:
    st.subheader("Gráficos e Relatórios")
    df = carregar_dados()

    if df.empty:
        st.info("Nenhuma transação para exibir.")
    else:
        despesas = df[df["Tipo"] == "Despesa"]
        receitas = df[df["Tipo"] == "Receita"]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Receitas", f"R$ {receitas['Valor'].sum():.2f}")
        with col2:
            st.metric("Total de Despesas", f"R$ {despesas['Valor'].sum():.2f}")

        st.markdown("### Gastos por Categoria")
        if not despesas.empty:
            grafico = despesas.groupby("Categoria")["Valor"].sum()
            st.bar_chart(grafico)

        st.markdown("### Receita Mensal")
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
        df["AnoMes"] = df["Data"].dt.to_period("M").astype(str)
        receita_mensal = df[df["Tipo"] == "Receita"].groupby("AnoMes")["Valor"].sum()
        st.line_chart(receita_mensal)
