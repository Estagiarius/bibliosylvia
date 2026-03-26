import logging
from database.db_config import get_connection

class EmprestimoRepository:
    def adicionar(self, id_usuario, id_tombo, data_retirada, data_devolucao_prevista):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Emprestimos
                (id_usuario, id_tombo, data_retirada, data_devolucao_prevista, status)
                VALUES (?, ?, ?, ?, 'Ativo')
            ''', (id_usuario, id_tombo, data_retirada, data_devolucao_prevista))
            conn.commit()
            logging.info(f"Empréstimo do livro {id_tombo} para usuário {id_usuario} registrado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao registrar empréstimo: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def buscar_emprestimo_ativo_por_tombo(self, id_tombo):
        """Retorna o empréstimo ativo associado ao id_tombo, se houver."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Emprestimos
                WHERE id_tombo = ? AND status = 'Ativo'
            ''', (id_tombo,))
            emprestimo = cursor.fetchone()
            return dict(emprestimo) if emprestimo else None
        except Exception as e:
            logging.error(f"Erro ao buscar empréstimo ativo para o tombo {id_tombo}: {e}")
            raise
        finally:
            conn.close()

    def listar_emprestimos_ativos(self):
        """Retorna uma lista de todos os empréstimos ativos, fazendo JOIN com Usuarios e Livros_Fisicos."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT
                    e.id_emprestimo,
                    e.id_tombo,
                    l.titulo_curto,
                    e.id_usuario,
                    u.nome as nome_usuario,
                    e.data_retirada,
                    e.data_devolucao_prevista
                FROM Emprestimos e
                JOIN Livros_Fisicos l ON e.id_tombo = l.id_tombo
                JOIN Usuarios u ON e.id_usuario = u.id_usuario
                WHERE e.status = 'Ativo'
                ORDER BY e.data_devolucao_prevista ASC
            ''')
            emprestimos = cursor.fetchall()
            return [dict(row) for row in emprestimos]
        except Exception as e:
            logging.error(f"Erro ao listar empréstimos ativos: {e}")
            raise
        finally:
            conn.close()

    def devolver_emprestimo(self, id_emprestimo, data_devolucao_real):
        """Atualiza o empréstimo definindo a data de devolução real e alterando status para Devolvido."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Emprestimos
                SET data_devolucao_real = ?, status = 'Devolvido'
                WHERE id_emprestimo = ?
            ''', (data_devolucao_real, id_emprestimo))
            conn.commit()

            if cursor.rowcount == 0:
                logging.warning(f"Tentativa de devolver empréstimo {id_emprestimo} que não existe ou não foi atualizado.")
                return False

            logging.info(f"Empréstimo {id_emprestimo} atualizado para 'Devolvido' em {data_devolucao_real}.")
            return True
        except Exception as e:
            logging.error(f"Erro ao devolver o empréstimo {id_emprestimo}: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
