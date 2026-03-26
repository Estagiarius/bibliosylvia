import logging
from database.db_config import get_connection

class LivroRepository:
    def adicionar(self, id_tombo, titulo_curto):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Livros_Fisicos (id_tombo, titulo_curto)
                VALUES (?, ?)
            ''', (id_tombo, titulo_curto))
            conn.commit()
            logging.info(f"Livro físico {id_tombo} ({titulo_curto}) inserido com sucesso no banco de dados.")
        except Exception as e:
            logging.error(f"Erro ao inserir livro {id_tombo}: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def buscar_por_id(self, id_tombo):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Livros_Fisicos WHERE id_tombo = ?', (id_tombo,))
            livro = cursor.fetchone()
            return dict(livro) if livro else None
        except Exception as e:
            logging.error(f"Erro ao buscar livro {id_tombo}: {e}")
            raise
        finally:
            conn.close()
