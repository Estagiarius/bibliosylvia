import customtkinter as ctk
import logging

class TabEmprestimo(ctk.CTkFrame):
    def __init__(self, master, gestor):
        super().__init__(master)
        self.gestor = gestor

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="Registrar Empréstimo", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

        # Container do Formulário
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        # ID do Usuário
        self.label_usuario = ctk.CTkLabel(self.frame_form, text="ID do Usuário:")
        self.label_usuario.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_usuario = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 123456")
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # ID do Livro (Tombo)
        self.label_tombo = ctk.CTkLabel(self.frame_form, text="ID do Livro (Tombo):")
        self.label_tombo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_tombo = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: LIV-001")
        self.entry_tombo.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Quantidade de Dias
        self.label_dias = ctk.CTkLabel(self.frame_form, text="Dias de Empréstimo:")
        self.label_dias.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_dias = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 7")
        self.entry_dias.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Botão Registrar
        self.btn_registrar = ctk.CTkButton(self, text="Registrar Saída", command=self.registrar_saida)
        self.btn_registrar.pack(pady=20)

        # Label de Feedback
        self.label_feedback = ctk.CTkLabel(self, text="", text_color="green", wraplength=400)
        self.label_feedback.pack(pady=10)

        # Configura as colunas para se expandirem
        self.frame_form.grid_columnconfigure(1, weight=1)

    def registrar_saida(self):
        id_usuario = self.entry_usuario.get().strip()
        id_tombo = self.entry_tombo.get().strip()
        dias = self.entry_dias.get().strip()

        try:
            sucesso, data_prevista = self.gestor.registrar_emprestimo(id_usuario, id_tombo, dias)
            if sucesso:
                msg = f"Empréstimo registrado com sucesso.\nDevolução prevista: {data_prevista}"
                self.label_feedback.configure(text=msg, text_color="green")
                # Limpar campos
                self.entry_usuario.delete(0, 'end')
                self.entry_tombo.delete(0, 'end')
                self.entry_dias.delete(0, 'end')
        except Exception as e:
            self.label_feedback.configure(text=f"Erro: {str(e)}", text_color="red")
            logging.error(f"Erro na interface de empréstimo: {e}")
