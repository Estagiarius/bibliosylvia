import customtkinter as ctk
import logging

from controllers.gestor_emprestimos import GestorEmprestimos
from views.tab_emprestimo import TabEmprestimo
from views.tab_devolucao import TabDevolucao
from views.tab_cadastros import TabCadastros
from views.tab_config import TabConfig

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Biblioteca Escolar - Standalone")
        self.geometry("900x600")

        # Configura grid (1 coluna, 1 linha)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Instancia o Gestor de Empréstimos
        self.gestor = GestorEmprestimos()

        # Adiciona o TabView
        self.tab_view = ctk.CTkTabview(self, width=850, height=550)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Adiciona as Abas
        self.tab_view.add("Empréstimo")
        self.tab_view.add("Devolução")
        self.tab_view.add("Cadastros Iniciais")
        self.tab_view.add("Configurações e Backup")

        # Configuração das instâncias dentro das abas
        self._setup_tabs()

    def _setup_tabs(self):
        try:
            # Empréstimo
            tab_emprestimo = TabEmprestimo(master=self.tab_view.tab("Empréstimo"), gestor=self.gestor)
            tab_emprestimo.pack(expand=True, fill="both")

            # Devolução
            tab_devolucao = TabDevolucao(master=self.tab_view.tab("Devolução"), gestor=self.gestor)
            tab_devolucao.pack(expand=True, fill="both")

            # Cadastros
            tab_cadastros = TabCadastros(master=self.tab_view.tab("Cadastros Iniciais"), gestor=self.gestor)
            tab_cadastros.pack(expand=True, fill="both")

            # Config
            tab_config = TabConfig(master=self.tab_view.tab("Configurações e Backup"))
            tab_config.pack(expand=True, fill="both")

            logging.info("Interfaces gráficas carregadas com sucesso.")
        except Exception as e:
            logging.error(f"Erro crítico ao carregar abas: {e}")
            raise RuntimeError("Falha ao inicializar os componentes visuais.")
