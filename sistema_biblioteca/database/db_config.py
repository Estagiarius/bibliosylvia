import sqlite3
import os
import logging

def get_db_path():
    """Retorna o caminho absoluto do arquivo do banco de dados (mesmo diretório do projeto)."""
    # Como o arquivo atual está em /database, queremos pegar o diretório pai onde está main.py
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'dados_escola.db')

def get_connection():
    """Retorna uma nova conexão com o banco de dados."""
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        # Permite acessar colunas por nome
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        raise

def init_db():
    """Cria as tabelas necessárias se elas não existirem."""
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Tabela Usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
                id_usuario TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        ''')

        # Tabela Livros_Fisicos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Livros_Fisicos (
                id_tombo TEXT PRIMARY KEY,
                titulo_curto TEXT NOT NULL
            )
        ''')

        # Tabela Emprestimos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Emprestimos (
                id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario TEXT NOT NULL,
                id_tombo TEXT NOT NULL,
                data_retirada DATE NOT NULL,
                data_devolucao_prevista DATE NOT NULL,
                data_devolucao_real DATE NULL,
                status TEXT NOT NULL CHECK(status IN ('Ativo', 'Devolvido')),
                FOREIGN KEY(id_usuario) REFERENCES Usuarios(id_usuario),
                FOREIGN KEY(id_tombo) REFERENCES Livros_Fisicos(id_tombo)
            )
        ''')

        conn.commit()
        logging.info("Tabelas do banco de dados criadas/verificadas com sucesso.")
    except sqlite3.Error as e:
        logging.error(f"Erro ao inicializar tabelas do banco: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
