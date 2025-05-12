import sqlite3

DB = 'dados_financeiros.db'

def conectar():
    return sqlite3.connect(DB)

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT,
            data TEXT NOT NULL,
            descricao TEXT
        )
    """)
    conn.commit()
    conn.close()

def inserir_transacao(tipo, valor, categoria, data, descricao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transacoes (tipo, valor, categoria, data, descricao)
        VALUES (?, ?, ?, ?, ?)
    """, (tipo, valor, categoria, data, descricao))
    conn.commit()
    conn.close()

def listar_transacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes")
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_transacao(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
