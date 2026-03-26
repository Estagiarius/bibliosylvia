import customtkinter as ctk
import logging

class TabDevolucao(ctk.CTkFrame):
    def __init__(self, master, gestor):
        super().__init__(master)
        self.gestor = gestor

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="Registrar Devolução", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

        # Container do Formulário
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        # ID do Livro (Tombo)
        self.label_tombo = ctk.CTkLabel(self.frame_form, text="ID do Livro (Tombo):")
        self.label_tombo.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_tombo = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: LIV-001")
        self.entry_tombo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Botão Registrar Devolução
        self.btn_registrar = ctk.CTkButton(self, text="Registrar Entrada/Baixa", command=self.registrar_entrada)
        self.btn_registrar.pack(pady=20)

        # Label de Feedback
        self.label_feedback = ctk.CTkLabel(self, text="", text_color="green", wraplength=400)
        self.label_feedback.pack(pady=10)

        # Configura as colunas para se expandirem
        self.frame_form.grid_columnconfigure(1, weight=1)

    def registrar_entrada(self):
        id_tombo = self.entry_tombo.get().strip()

        try:
            sucesso, data_devolucao_real = self.gestor.registrar_devolucao(id_tombo)
            if sucesso:
                msg = f"Devolução registrada com sucesso em {data_devolucao_real}."
                self.label_feedback.configure(text=msg, text_color="green")
                # Limpar campo
                self.entry_tombo.delete(0, 'end')
        except Exception as e:
            self.label_feedback.configure(text=f"Erro: {str(e)}", text_color="red")
            logging.error(f"Erro na interface de devolução: {e}")
