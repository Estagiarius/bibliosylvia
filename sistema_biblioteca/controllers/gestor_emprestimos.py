import logging
import sqlite3
from datetime import datetime, timedelta

from models.usuario_repo import UsuarioRepository
from models.livro_repo import LivroRepository
from models.emprestimo_repo import EmprestimoRepository

class GestorEmprestimos:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.livro_repo = LivroRepository()
        self.emprestimo_repo = EmprestimoRepository()

    def cadastrar_usuario(self, id_usuario, nome, tipo):
        """Registra um novo usuário no sistema."""
        if not id_usuario or not nome or not tipo:
            raise ValueError("Todos os campos de usuário são obrigatórios.")

        # Verificar se usuário já existe
        if self.usuario_repo.buscar_por_id(id_usuario):
            raise ValueError(f"O usuário com ID {id_usuario} já existe.")

        self.usuario_repo.adicionar(id_usuario, nome, tipo)
        return True

    def cadastrar_livro(self, id_tombo, titulo_curto):
        """Registra um novo livro físico no sistema."""
        if not id_tombo or not titulo_curto:
            raise ValueError("Todos os campos do livro são obrigatórios.")

        # Verificar se livro já existe
        if self.livro_repo.buscar_por_id(id_tombo):
            raise ValueError(f"O livro com o tombo {id_tombo} já existe.")

        self.livro_repo.adicionar(id_tombo, titulo_curto)
        return True

    def registrar_emprestimo(self, id_usuario, id_tombo, dias_emprestimo):
        """
        Registra o empréstimo de um livro.
        Valida se o livro e o usuário existem, e se o livro não está emprestado.
        """
        if not id_usuario or not id_tombo:
            raise ValueError("ID do Usuário e ID do Tombo são obrigatórios.")

        try:
            dias = int(dias_emprestimo)
            if dias <= 0:
                raise ValueError()
        except ValueError:
            raise ValueError("A quantidade de dias deve ser um número inteiro positivo.")

        # 1. Validar existência do Usuário
        usuario = self.usuario_repo.buscar_por_id(id_usuario)
        if not usuario:
            raise ValueError(f"Usuário {id_usuario} não encontrado.")

        # 2. Validar existência do Livro
        livro = self.livro_repo.buscar_por_id(id_tombo)
        if not livro:
            raise ValueError(f"Livro (Tombo: {id_tombo}) não encontrado.")

        # 3. Validar concorrência/status (Se já está emprestado e ativo)
        emprestimo_ativo = self.emprestimo_repo.buscar_emprestimo_ativo_por_tombo(id_tombo)
        if emprestimo_ativo:
            raise ValueError(f"O livro (Tombo: {id_tombo}) já possui um empréstimo ativo e não foi devolvido.")

        # 4. Calcular datas e registrar
        data_atual = datetime.now()
        data_retirada_str = data_atual.strftime('%Y-%m-%d')
        data_devolucao_prevista = data_atual + timedelta(days=dias)
        data_devolucao_prevista_str = data_devolucao_prevista.strftime('%Y-%m-%d')

        self.emprestimo_repo.adicionar(
            id_usuario=id_usuario,
            id_tombo=id_tombo,
            data_retirada=data_retirada_str,
            data_devolucao_prevista=data_devolucao_prevista_str
        )

        # Para a interface, retorna no formato BR
        data_devolucao_prevista_br = data_devolucao_prevista.strftime('%d/%m/%Y')
        return True, data_devolucao_prevista_br

    def obter_emprestimos_ativos(self):
        """Retorna todos os empréstimos ativos."""
        try:
            return self.emprestimo_repo.listar_emprestimos_ativos()
        except Exception as e:
            logging.error(f"Erro no controller ao obter empréstimos ativos: {e}")
            raise RuntimeError("Não foi possível carregar a lista de empréstimos ativos.")

    def registrar_devolucao(self, id_tombo):
        """
        Registra a devolução de um livro.
        Busca se há um empréstimo ativo para o id_tombo e o encerra.
        """
        if not id_tombo:
            raise ValueError("O ID do Tombo é obrigatório.")

        # 1. Validar existência do Livro
        livro = self.livro_repo.buscar_por_id(id_tombo)
        if not livro:
            raise ValueError(f"Livro (Tombo: {id_tombo}) não encontrado.")

        # 2. Buscar empréstimo ativo
        emprestimo_ativo = self.emprestimo_repo.buscar_emprestimo_ativo_por_tombo(id_tombo)
        if not emprestimo_ativo:
            raise ValueError(f"Não há nenhum empréstimo ativo para o livro (Tombo: {id_tombo}).")

        # 3. Registrar devolução factual
        data_atual = datetime.now()
        data_devolucao_real_iso = data_atual.strftime('%Y-%m-%d')
        id_emprestimo = emprestimo_ativo['id_emprestimo']

        sucesso = self.emprestimo_repo.devolver_emprestimo(id_emprestimo, data_devolucao_real_iso)

        if not sucesso:
            raise RuntimeError("Falha desconhecida ao tentar atualizar o empréstimo no banco de dados.")

        data_devolucao_real_br = data_atual.strftime('%d/%m/%Y')
        return True, data_devolucao_real_br
