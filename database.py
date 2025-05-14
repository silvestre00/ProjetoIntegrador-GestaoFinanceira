import sqlite3
import hashlib

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario(username, senha):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", (username, hash_senha(senha)))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def autenticar_usuario(username, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE username = ? AND senha = ?", (username, hash_senha(senha)))
    usuario = cursor.fetchone()
    conn.close()
    return usuario[0] if usuario else None

DB = 'dados_financeiros.db'

def conectar():
    return sqlite3.connect(DB)

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    # Tabela de transações com vínculo ao usuário
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL,
            descricao TEXT,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    conn.commit()
    conn.close()


def inserir_transacao(tipo, valor, categoria, data, descricao, usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transacoes (tipo, valor, categoria, data, descricao, usuario_id) VALUES (?, ?, ?, ?, ?, ?)",
        (tipo, valor, categoria, data, descricao, usuario_id)
    )
    conn.commit()
    conn.close()


def listar_transacoes(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, tipo, valor, categoria, data, descricao FROM transacoes WHERE usuario_id = ?", (usuario_id,))
    dados = cursor.fetchall()
    conn.close()
    return dados


def deletar_transacao(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id,))
    conn.commit()
    conn.close()


def atualizar_transacao(id, tipo, valor, categoria, data, descricao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transacoes
        SET tipo = ?, valor = ?, categoria = ?, data = ?, descricao = ?
        WHERE id = ?
    """, (tipo, valor, categoria, data, descricao, id))
    conn.commit()
    conn.close()


