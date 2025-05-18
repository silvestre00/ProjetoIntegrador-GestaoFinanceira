# Senac EAD - Projeto Integrador
## Desenvolvimento de Sistemas Orientado a Dispositivos Móveis e Baseados na Web

### Integrantes:
• Silvestre Alves de Almeida Neto  
• Vinicius da Silva Ferreira  
• Bruno Bezerra Almeida  
• Charles Mamor Iwamoto Filho  
• Fernanda Mayara Severino

# 💼 Sistema Web de Controle Financeiro Pessoal

## Descrição:
É um sistema web desenvolvido com foco em **educação financeira** e **gestão prática das finanças pessoais**. Com uma interface simples, moderna e responsiva, o sistema permite aos usuários:

## Visualização do Website
![image_alt](https://github.com/silvestre00/ProjetoIntegrador-GestaoFinanceira/blob/25ad81a3bc463bdffd422b6b19923f8e1a0ea07b/interface.png)

---
- ✅ Registrar **receitas e despesas** de forma rápida  
- 🏷️ **Categorizar** seus gastos  
- 📊 Visualizar **relatórios dinâmicos e gráficos interativos**  
- ✏️ Editar ou excluir transações já registradas  
- 🔐 Contar com um sistema de **autenticação de usuários** (login e cadastro)  
- 📅 Aplicar **filtros por data, tipo e categoria** para facilitar a análise  

## 🎯 Objetivo do Projeto

Este projeto tem como objetivo desenvolver um **website para controle financeiro pessoal**, com interface intuitiva e acessível.

A solução permite:

- Registro simplificado de receitas e despesas  
- Categorização de gastos  
- Geração de relatórios dinâmicos e gráficos analíticos  
- Filtros interativos por período, tipo e categoria  
- Apoio à organização financeira pessoal, desde a **saída de dívidas até o planejamento de investimentos**  

---

## 🛠️ Tecnologias Utilizadas

- **[Python](https://www.python.org/)** – Lógica de backend  
- **[Streamlit](https://streamlit.io/)** – Framework para construção do front-end web  
- **[SQLite3](https://www.sqlite.org/index.html)** – Banco de dados local para persistência  
- **[Plotly](https://plotly.com/python/)** – Visualização de gráficos interativos  
- **[Pandas](https://pandas.pydata.org/)** – Manipulação e análise de dados  

---

## 🔐 Funcionalidades

### Autenticação de Usuário

- Cadastro com nome de usuário e senha  
- Login com verificação de credenciais (criptografia com `hashlib`)  

### Dashboard de Controle Financeiro

- Registro de transações com tipo (Receita/Despesa), valor, data, categoria e descrição  
- Visualização das transações em tabela interativa  
- Edição e exclusão de transações  

### Relatórios e Gráficos

- Gráficos de pizza para **distribuição por categoria**  
- Gráficos de linha para **evolução mensal de receitas, despesas e saldo**  
- Métricas agregadas (total de receitas, despesas e saldo)  
- Filtros por tipo, categoria e intervalo de datas  

---

## 🗂️ Estrutura do Projeto

- `app.py`: Interface e lógica principal com Streamlit  
- `dados_financeiros.db`: Banco de dados local (gerado automaticamente)  
- `database.py`: Lógica de conexão, autenticação e manipulação de dados SQLite  
- `requirements.txt`: Dependências do projeto  
- `transacoes.csv`: Registro auxiliar das transações (não essencial)  
- `README.md`: Documentação do projeto  

---

## 🚀 Como Executar o Projeto

1. **Clone o repositório:**

```bash
git clone https://github.com/silvestre00/ProjetoIntegrador-GestaoFinanceira.git
cd ProjetoIntegrador-GestaoFinanceira

2. **Instale as dependências:**

```bash
pip install streamlit pandas plotly

3.**Execute o projeto com o Streamlit:**
streamlit run app.py

O navegador será aberto com o endereço:
http://localhost:8501


## 🌐 Acesso ao Projeto

Você pode acessar a aplicação web do projeto de gestão financeira diretamente neste link:

[👉 Projeto Integrador - Gestão Financeira](https://projetointegrador-gestaofinanceira-4v7ppyxqbhxiqzpdopc7eg.streamlit.app/)

Sinta-se à vontade para testar todas as funcionalidades, registrar transações, visualizar relatórios e explorar o sistema!

