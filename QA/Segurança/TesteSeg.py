import sqlite3
import time
import random
import shutil
import os

# ==============================
# CONFIGURAÇÃO
# ==============================

DB_SISTEMA = "sistema.db"
DB_USUARIOS = "usuarios.db"
BACKUP_DB = "backup.db"

# ==============================
# FUNÇÃO DE INPUT SEGURO
# ==============================

def safe_input(mensagem, valor_padrao):
    """
    Tenta ler input do usuário.
    Se o ambiente não permitir, usa valor padrão.
    """
    try:
        valor = input(mensagem)
        if valor.strip() == "":
            return valor_padrao
        return valor
    except Exception:
        print(f"(Sem input disponível, usando padrão: {valor_padrao})")
        return valor_padrao

# ==============================
#          SEGURANÇA
# ==============================

def criar_banco_usuarios():
    conn = sqlite3.connect(DB_USUARIOS)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            senha TEXT
        )
    """)

    conn.commit()
    conn.close()


def cadastrar_usuario(username, senha):
    conn = sqlite3.connect(DB_USUARIOS)
    cursor = conn.cursor()

    # Verifica se usuário já existe
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    existente = cursor.fetchone()

    if existente:
        print(f"⚠️ Usuário '{username}' já existe. Não será criado novamente.")
    else:
        cursor.execute(
            "INSERT INTO usuarios (username, senha) VALUES (?, ?)",
            (username, senha)
        )
        conn.commit()
        print(f"✅ Usuário '{username}' criado com sucesso.")

    conn.close()


def autenticar(username, senha):
    conn = sqlite3.connect(DB_USUARIOS)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ? AND senha = ?",
        (username, senha)
    )

    user = cursor.fetchone()
    conn.close()

    return user is not None


def listar_usuarios():
    conn = sqlite3.connect(DB_USUARIOS)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    print("\n� Usuários cadastrados:")
    for u in usuarios:
        print(u)

    conn.close()


def teste_seguranca():
    print("\n========== TESTE DE SEGURANÇA ==========")

    criar_banco_usuarios()

    # Criando usuários base
    cadastrar_usuario(safe_input("Digite o usuário: ", "admin"), safe_input("Digite a senha: ", "admin"))

    listar_usuarios()

    print("\n➡️ Teste de login interativo")

    # INPUT (com fallback automático)
    user = safe_input("Digite o usuário: ", "admin")
    senha = safe_input("Digite o usuário: ", "admin")

    if autenticar(user, senha):
        print(f"✅ Acesso permitido: {user}")
    else:
        print(f"❌ Acesso negado: {user}")


# ==============================
# EXECUÇÃO
# ==============================

if __name__ == "__main__":
    print("� INICIANDO SISTEMA DE TESTES")

    criar_banco_sistema()
    inserir_dado("Dado inicial")
    criar_backup()

    teste_recuperacao()
    teste_seguranca()

    print("\n✅ TESTES FINALIZADOS")