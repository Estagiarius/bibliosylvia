import customtkinter as ctk
import logging

class TabCadastros(ctk.CTkFrame):
    def __init__(self, master, gestor):
        super().__init__(master)
        self.gestor = gestor

        # Layout com duas colunas para os formulários
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ------------------- Formulário de Usuários -------------------
        self.frame_usuario = ctk.CTkFrame(self)
        self.frame_usuario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.label_titulo_usu = ctk.CTkLabel(self.frame_usuario, text="Cadastrar Usuário", font=("Arial", 16, "bold"))
        self.label_titulo_usu.pack(pady=10)

        # Campos (ID automático)
        self.entry_nome_usuario = ctk.CTkEntry(self.frame_usuario, placeholder_text="Nome Completo")
        self.entry_nome_usuario.pack(pady=10, padx=20, fill="x")

        self.combo_tipo = ctk.CTkComboBox(self.frame_usuario, values=["Aluno", "Professor", "Funcionário"])
        self.combo_tipo.pack(pady=10, padx=20, fill="x")
        self.combo_tipo.set("Aluno")

        self.btn_cad_usuario = ctk.CTkButton(self.frame_usuario, text="Cadastrar", command=self.cadastrar_usuario)
        self.btn_cad_usuario.pack(pady=15)

        self.label_feedback_usu = ctk.CTkLabel(self.frame_usuario, text="", text_color="green", wraplength=200)
        self.label_feedback_usu.pack(pady=5)

        # ------------------- Formulário de Livros -------------------
        self.frame_livro = ctk.CTkFrame(self)
        self.frame_livro.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.label_titulo_livro = ctk.CTkLabel(self.frame_livro, text="Cadastrar Livro Físico", font=("Arial", 16, "bold"))
        self.label_titulo_livro.pack(pady=10)

        # Campos (ID automático)
        self.entry_titulo_curto = ctk.CTkEntry(self.frame_livro, placeholder_text="Título Curto (Ex: Dom Casmurro)")
        self.entry_titulo_curto.pack(pady=10, padx=20, fill="x")

        self.btn_cad_livro = ctk.CTkButton(self.frame_livro, text="Cadastrar", command=self.cadastrar_livro)
        self.btn_cad_livro.pack(pady=15)

        self.label_feedback_livro = ctk.CTkLabel(self.frame_livro, text="", text_color="green", wraplength=200)
        self.label_feedback_livro.pack(pady=5)

    def cadastrar_usuario(self):
        nome = self.entry_nome_usuario.get().strip()
        tipo = self.combo_tipo.get().strip()

        try:
            id_gerado = self.gestor.cadastrar_usuario(nome, tipo)
            self.label_feedback_usu.configure(text=f"Usuário {nome} cadastrado com ID {id_gerado}!", text_color="green")
            self.entry_nome_usuario.delete(0, 'end')
        except Exception as e:
            self.label_feedback_usu.configure(text=f"Erro: {str(e)}", text_color="red")
            logging.error(f"Erro na interface de cadastro de usuário: {e}")

    def cadastrar_livro(self):
        titulo = self.entry_titulo_curto.get().strip()

        try:
            id_gerado = self.gestor.cadastrar_livro(titulo)
            self.label_feedback_livro.configure(text=f"Livro {titulo} cadastrado com Tombo {id_gerado}!", text_color="green")
            self.entry_titulo_curto.delete(0, 'end')
        except Exception as e:
            self.label_feedback_livro.configure(text=f"Erro: {str(e)}", text_color="red")
            logging.error(f"Erro na interface de cadastro de livro: {e}")
