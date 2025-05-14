import streamlit as st
import pandas as pd
import os
from datetime import date
import plotly.express as px
from database import criar_tabela, inserir_transacao, listar_transacoes, deletar_transacao
from database import (
    criar_tabela, inserir_transacao, listar_transacoes,
    deletar_transacao, atualizar_transacao,
    cadastrar_usuario, autenticar_usuario
)

if "usuario_id" not in st.session_state:
    st.session_state.usuario_id = None

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

st.title("💼 App de Gestão Financeira")

if st.session_state.usuario_id is None:
    st.subheader("🔐 Acesso")
    opcao = st.radio("Escolha uma opção", ["Login", "Registrar"])

    with st.form("form_login"):
        username = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar" if opcao == "Login" else "Registrar")

        if submit:
            if opcao == "Login":
                usuario_id = autenticar_usuario(username, senha)
                if usuario_id:
                    st.session_state.usuario_id = usuario_id
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos.")
            else:
                if cadastrar_usuario(username, senha):
                    st.success("Usuário registrado! Faça login.")
                else:
                    st.error("Erro: usuário já existe.")
    st.stop()
else:
    st.sidebar.success("✅ Logado")
    if st.sidebar.button("🚪 Sair"):
        st.session_state.usuario_id = None
        st.rerun()

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
        if tipo and valor > 0 and data:
            # Se categoria ou descrição estiverem em branco, ainda assim salva
            categoria = categoria if categoria.strip() != "" else "Não informado"
            descricao = descricao if descricao.strip() != "" else ""
            
            inserir_transacao(tipo, valor, categoria, str(data), descricao, st.session_state.usuario_id)
            st.success("Transação salva com sucesso!")
        else:
            st.error("Preencha os campos obrigatórios: Tipo, Valor e Data.")

with aba2:
    st.subheader("📋 Transações Registradas")
    dados = listar_transacoes(st.session_state.usuario_id)

    if not dados:
        st.info("Nenhuma transação registrada.")
    else:
        df = pd.DataFrame(dados, columns=["ID", "Tipo", "Valor", "Categoria", "Data", "Descrição"])
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

        # Filtros
        tipo_filtro = st.selectbox("Filtrar por tipo", ["Todos", "Receita", "Despesa"])
        data_inicio = st.date_input("Data início", value=df["Data"].min().date())
        data_fim = st.date_input("Data fim", value=df["Data"].max().date())

        if tipo_filtro != "Todos":
            df = df[df["Tipo"] == tipo_filtro]

        df = df[(df["Data"] >= pd.to_datetime(data_inicio)) & (df["Data"] <= pd.to_datetime(data_fim))]

        st.dataframe(df.sort_values(by="Data", ascending=False), use_container_width=True)

        # Excluir transações
        st.markdown("### ❌ Excluir uma transação")
        transacao_id = st.selectbox("Selecione o ID para excluir", df["ID"])
        if st.button("Excluir"):
            deletar_transacao(transacao_id)
            st.success(f"Transação com ID {transacao_id} excluída com sucesso!")
            st.rerun()  # Recarrega a página para atualizar
               
        # Editar transações
        st.markdown("### ✏️ Editar uma transação")
        id_editar = st.selectbox("Selecione o ID para editar", df["ID"], key="editar_id")

        transacao_editar = df[df["ID"] == id_editar].iloc[0]

        with st.form(key="form_edicao"):
            novo_tipo = st.selectbox("Tipo", ["Receita", "Despesa"], index=0 if transacao_editar["Tipo"] == "Receita" else 1)
            novo_valor = st.number_input("Valor", min_value=0.01, value=transacao_editar["Valor"])
            nova_categoria = st.text_input("Categoria", value=transacao_editar["Categoria"])
            nova_data = st.date_input("Data", value=pd.to_datetime(transacao_editar["Data"]).date())
            nova_descricao = st.text_input("Descrição", value=transacao_editar["Descrição"] if pd.notna(transacao_editar["Descrição"]) else "")
            
            if st.form_submit_button("Salvar Alterações"):
                atualizar_transacao(id_editar, novo_tipo, novo_valor, nova_categoria, str(nova_data), nova_descricao)
                st.success("Transação atualizada com sucesso!")
                st.rerun()

with aba3:
    st.subheader("📊 Relatórios e Gráficos")
    dados = listar_transacoes(st.session_state.usuario_id)

    if not dados:
        st.info("Nenhuma transação registrada.")
    else:
        df = pd.DataFrame(dados, columns=["ID", "Tipo", "Valor", "Categoria", "Data", "Descrição"])
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

        # 🎛️ Filtros Dinâmicos
        st.sidebar.markdown("### 🎯 Filtros do Dashboard")
        tipos = st.sidebar.multiselect("Tipo", options=df["Tipo"].unique(), default=df["Tipo"].unique())
        categorias = st.sidebar.multiselect("Categoria", options=df["Categoria"].dropna().unique(), default=df["Categoria"].dropna().unique())
        data_min = df["Data"].min().date()
        data_max = df["Data"].max().date()
        data_inicio = st.sidebar.date_input("De", value=data_min, min_value=data_min, max_value=data_max)
        data_fim = st.sidebar.date_input("Até", value=data_max, min_value=data_min, max_value=data_max)

        # 🎯 Aplicar filtros
        df_filtrado = df[
            (df["Tipo"].isin(tipos)) &
            (df["Categoria"].isin(categorias)) &
            (df["Data"] >= pd.to_datetime(data_inicio)) &
            (df["Data"] <= pd.to_datetime(data_fim))
        ]

        # 🔎 Verifica se houve algum erro na conversão
        if df_filtrado["Data"].isnull().any():
            st.warning("Algumas datas são inválidas e foram ignoradas nos gráficos.")

        # 🎯 Divide em receitas e despesas
        receitas = df_filtrado[df_filtrado["Tipo"] == "Receita"]
        despesas = df_filtrado[df_filtrado["Tipo"] == "Despesa"]

        # 💡 Exibe métricas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Receitas", f"R$ {receitas['Valor'].sum():.2f}")
        with col2:
            st.metric("Total de Despesas", f"R$ {despesas['Valor'].sum():.2f}")

        # 📊 Gráfico de despesas por categoria
        st.markdown("### 🧾 Gastos por Categoria")
        if not despesas.empty:
            categoria_gastos = despesas.groupby("Categoria")["Valor"].sum()
            st.bar_chart(categoria_gastos)

            # 📊 Gráfico de despesas por categoria (Pizza)
        st.markdown("### 🧾 Distribuição de Despesas por Categoria")
        if not despesas.empty:
            categoria_gastos = despesas.groupby("Categoria")["Valor"].sum().reset_index()
            fig = px.pie(
                categoria_gastos,
                names="Categoria",
                values="Valor",
                title="Despesas por Categoria",
                color_discrete_sequence=px.colors.sequential.Reds
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)


        else:
            st.info("Nenhuma despesa encontrada no período selecionado.")

        # 📊 Gráfico de receitas por categoria (Pizza)
        st.markdown("### 💡 Distribuição de Receitas por Categoria")
        if not receitas.empty:
            categoria_receitas = receitas.groupby("Categoria")["Valor"].sum().reset_index()
            fig = px.pie(
                categoria_receitas,
                names="Categoria",
                values="Valor",
                title="Receitas por Categoria",
                color_discrete_sequence=px.colors.sequential.Blues
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma despesa encontrada no período selecionado.")

            
        # 📈 Gráfico de receita mensal
        st.markdown("### 📈 Receita Mensal")
        df_validas = df_filtrado.dropna(subset=["Data"])
        df_validas["AnoMes"] = df_validas["Data"].dt.to_period("M").astype(str)
        receita_mensal = df_validas[df_validas["Tipo"] == "Receita"].groupby("AnoMes")["Valor"].sum()
        st.line_chart(receita_mensal)

        # 📊 Gráfico de saldo mensal
        st.markdown("### 💰 Saldo Mensal")
        saldo_mensal = (
            df_validas
            .groupby(["AnoMes", "Tipo"])["Valor"]
            .sum()
            .unstack(fill_value=0)
            .assign(Saldo=lambda x: x.get("Receita", 0) - x.get("Despesa", 0))
        )
        fig = px.line(
            saldo_mensal.reset_index(),
            x="AnoMes",
            y=["Receita", "Despesa", "Saldo"],
            title="Evolução Mensal: Receita, Despesa e Saldo"
            )
        st.plotly_chart(fig, use_container_width=True)








