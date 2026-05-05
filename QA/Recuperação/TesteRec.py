import sqlite3
import time
import random
import shutil
import os

# ==============================
# CONFIGURAÇÃO
# ==============================

DB_SISTEMA = "sistema.db"
BACKUP_DB = "backup.db"


# ==============================
#         RECUPERAÇÃO
# ==============================

def criar_banco_sistema():
    conn = sqlite3.connect(DB_SISTEMA)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor TEXT
        )
    """)

    conn.commit()
    conn.close()


def inserir_dado(valor):
    conn = sqlite3.connect(DB_SISTEMA)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO dados (valor) VALUES (?)", (valor,))
    conn.commit()
    conn.close()


def listar_dados():
    conn = sqlite3.connect(DB_SISTEMA)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dados")
    dados = cursor.fetchall()

    print("\n� Dados no sistema:")
    for d in dados:
        print(d)

    conn.close()


def criar_backup():
    if os.path.exists(DB_SISTEMA):
        shutil.copy(DB_SISTEMA, BACKUP_DB)
        print("� Backup criado.")


def restaurar_backup():
    if os.path.exists(BACKUP_DB):
        shutil.copy(BACKUP_DB, DB_SISTEMA)
        print("♻️ Banco restaurado.")


def simular_falha():
    return random.choice([True, False])


def teste_recuperacao():
    print("\n========== TESTE DE RECUPERAÇÃO ==========")

    inicio = time.time()

    try:
        inserir_dado("Dado importante")

        if simular_falha():
            raise Exception("� Falha simulada!")

        print("✅ Operação executada com sucesso.")

    except Exception as e:
        print(e)
        print("� Recuperando sistema...")

        restaurar_backup()

        print("� Sistema em estado seguro.")

    finally:
        tempo = time.time() - inicio
        print(f"⏱️ Tempo de recuperação: {tempo:.2f}s")

        listar_dados()