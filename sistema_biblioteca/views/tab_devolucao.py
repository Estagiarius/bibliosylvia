import customtkinter as ctk
import logging
from datetime import datetime

class TabDevolucao(ctk.CTkFrame):
    def __init__(self, master, gestor):
        super().__init__(master)
        self.gestor = gestor

        # Título e Atualizar
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(pady=10, padx=20, fill="x")

        self.label_titulo = ctk.CTkLabel(self.frame_top, text="Gerenciar Devoluções", font=("Arial", 20, "bold"))
        self.label_titulo.pack(side="left")

        self.btn_atualizar = ctk.CTkButton(self.frame_top, text="Atualizar Lista", width=120, command=self.carregar_lista)
        self.btn_atualizar.pack(side="right")

        # Container Scrollable para a lista de empréstimos
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Configurar colunas do grid do scroll frame para dar peso igual a todas
        # exceto o botão, para que fique alinhado
        for i in range(5):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

        # Label de Feedback
        self.label_feedback = ctk.CTkLabel(self, text="", text_color="green", wraplength=400)
        self.label_feedback.pack(pady=10)

        # Armazena referências dos widgets desenhados para não haver problemas no Garbage Collector (embora em tk não precise)
        self.widgets_linhas = []

        # Carrega inicialmente
        self.carregar_lista()

    def formatar_data(self, data_str):
        """Converte de YYYY-MM-DD para DD/MM/YYYY para exibição."""
        try:
            return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            return data_str

    def limpar_lista(self):
        """Destrói todos os widgets filhos do scroll_frame."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

    def carregar_lista(self):
        """Busca os empréstimos ativos e os desenha na interface."""
        self.limpar_lista()

        try:
            emprestimos = self.gestor.obter_emprestimos_ativos()

            if not emprestimos:
                lbl = ctk.CTkLabel(self.scroll_frame, text="Nenhum empréstimo ativo no momento.", text_color="gray")
                lbl.grid(row=0, column=0, columnspan=5, pady=20)
                return

            # Cabeçalhos
            headers = ["Livro", "Usuário", "Retirada", "Previsão", "Ação"]
            for col, texto in enumerate(headers):
                lbl_h = ctk.CTkLabel(self.scroll_frame, text=texto, font=("Arial", 12, "bold"))
                lbl_h.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

            # Linhas
            for row, emp in enumerate(emprestimos, start=1):
                # Info
                lbl_livro = ctk.CTkLabel(self.scroll_frame, text=f"{emp['titulo_curto']} ({emp['id_tombo']})")
                lbl_livro.grid(row=row, column=0, padx=5, pady=5, sticky="w")

                lbl_usuario = ctk.CTkLabel(self.scroll_frame, text=f"{emp['nome_usuario']} ({emp['id_usuario']})")
                lbl_usuario.grid(row=row, column=1, padx=5, pady=5, sticky="w")

                lbl_retirada = ctk.CTkLabel(self.scroll_frame, text=self.formatar_data(emp['data_retirada']))
                lbl_retirada.grid(row=row, column=2, padx=5, pady=5)

                lbl_previsao = ctk.CTkLabel(self.scroll_frame, text=self.formatar_data(emp['data_devolucao_prevista']))
                lbl_previsao.grid(row=row, column=3, padx=5, pady=5)

                # Botão Devolver (usando closure ou lambda curried)
                btn_devolver = ctk.CTkButton(
                    self.scroll_frame,
                    text="Devolver",
                    fg_color="red",
                    hover_color="darkred",
                    width=80,
                    command=lambda t=emp['id_tombo']: self.realizar_devolucao(t)
                )
                btn_devolver.grid(row=row, column=4, padx=5, pady=5)

        except Exception as e:
            self.label_feedback.configure(text=f"Erro ao carregar lista: {str(e)}", text_color="red")

    def realizar_devolucao(self, id_tombo):
        """Chama a devolução pelo ID do tombo correspondente."""
        try:
            sucesso, data_devolucao_real = self.gestor.registrar_devolucao(id_tombo)
            if sucesso:
                msg = f"Devolução do Tombo '{id_tombo}' registrada em {data_devolucao_real}."
                self.label_feedback.configure(text=msg, text_color="green")
                # Recarrega a lista
                self.carregar_lista()
        except Exception as e:
            self.label_feedback.configure(text=f"Erro na devolução: {str(e)}", text_color="red")
            logging.error(f"Erro na interface de listagem/devolução: {e}")
