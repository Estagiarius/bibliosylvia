import logging
from database.db_config import get_connection

class UsuarioRepository:
    def adicionar(self, id_usuario, nome, tipo):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Usuarios (id_usuario, nome, tipo)
                VALUES (?, ?, ?)
            ''', (id_usuario, nome, tipo))
            conn.commit()
            logging.info(f"Usuário {id_usuario} ({nome}) inserido com sucesso no banco de dados.")
        except Exception as e:
            logging.error(f"Erro ao inserir usuário {id_usuario}: {e}")
            conn.rollback()
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
