import logging
from database.db_config import get_connection

class UsuarioRepository:
    def adicionar(self, nome, tipo):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Usuarios (nome, tipo)
                VALUES (?, ?)
            ''', (nome, tipo))
            conn.commit()
            id_gerado = cursor.lastrowid
            logging.info(f"Usuário {id_gerado} ({nome}) inserido com sucesso no banco de dados.")
            return id_gerado
        except Exception as e:
            logging.error(f"Erro ao inserir usuário {nome}: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def listar_todos(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id_usuario, nome, tipo FROM Usuarios ORDER BY nome ASC')
            usuarios = cursor.fetchall()
            return [dict(row) for row in usuarios]
        except Exception as e:
            logging.error(f"Erro ao listar todos os usuários: {e}")
            raise
        finally:
            conn.close()

    def buscar_por_id(self, id_usuario):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Usuarios WHERE id_usuario = ?', (id_usuario,))
            usuario = cursor.fetchone()
            return dict(usuario) if usuario else None
        except Exception as e:
            logging.error(f"Erro ao buscar usuário {id_usuario}: {e}")
            raise
        finally:
            conn.close()
