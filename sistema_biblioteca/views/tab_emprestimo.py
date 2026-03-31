import customtkinter as ctk
import logging

class TabEmprestimo(ctk.CTkFrame):
    def __init__(self, master, gestor):
        super().__init__(master)
        self.gestor = gestor

        # Layout top
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(pady=10, padx=20, fill="x")

        # Título
        self.label_titulo = ctk.CTkLabel(self.frame_top, text="Registrar Empréstimo", font=("Arial", 20, "bold"))
        self.label_titulo.pack(side="left")

        # Botão de atualizar listas
        self.btn_atualizar_listas = ctk.CTkButton(self.frame_top, text="Atualizar Listas", width=120, command=self.carregar_listas)
        self.btn_atualizar_listas.pack(side="right")

        # Container do Formulário
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        # Seleção de Usuário
        self.label_usuario = ctk.CTkLabel(self.frame_form, text="Usuário:")
        self.label_usuario.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.combo_usuario = ctk.CTkComboBox(self.frame_form, values=["Carregando..."], width=300)
        self.combo_usuario.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Seleção de Livro (Tombo)
        self.label_tombo = ctk.CTkLabel(self.frame_form, text="Livro (Tombo):")
        self.label_tombo.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.combo_livro = ctk.CTkComboBox(self.frame_form, values=["Carregando..."], width=300)
        self.combo_livro.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Quantidade de Dias
        self.label_dias = ctk.CTkLabel(self.frame_form, text="Dias de Empréstimo:")
        self.label_dias.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.entry_dias = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 7")
        self.entry_dias.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.entry_dias.insert(0, "7") # Valor default amigável

        # Botão Registrar
        self.btn_registrar = ctk.CTkButton(self, text="Registrar Saída", command=self.registrar_saida)
        self.btn_registrar.pack(pady=20)

        # Label de Feedback
        self.label_feedback = ctk.CTkLabel(self, text="", text_color="green", wraplength=400)
        self.label_feedback.pack(pady=10)

        # Configura as colunas para se expandirem
        self.frame_form.grid_columnconfigure(1, weight=1)

        # Carrega os dados para os ComboBoxes
        self.carregar_listas()

    def carregar_listas(self):
        """Busca usuários e livros e popula os comboboxes."""
        try:
            # Usuarios
            usuarios = self.gestor.obter_usuarios()
            lista_usuarios = [f"{u['nome']} (ID: {u['id_usuario']})" for u in usuarios]

            if lista_usuarios:
                self.combo_usuario.configure(values=lista_usuarios)
                self.combo_usuario.set(lista_usuarios[0])
            else:
                self.combo_usuario.configure(values=["Nenhum usuário cadastrado"])
                self.combo_usuario.set("Nenhum usuário cadastrado")

            # Livros
            livros = self.gestor.obter_livros()
            lista_livros = [f"{l['titulo_curto']} (Tombo: {l['id_tombo']})" for l in livros]

            if lista_livros:
                self.combo_livro.configure(values=lista_livros)
                self.combo_livro.set(lista_livros[0])
            else:
                self.combo_livro.configure(values=["Nenhum livro cadastrado"])
                self.combo_livro.set("Nenhum livro cadastrado")

            self.label_feedback.configure(text="Listas atualizadas com sucesso.", text_color="blue")
        except Exception as e:
            self.label_feedback.configure(text=f"Erro ao carregar listas: {str(e)}", text_color="red")
            logging.error(f"Erro na interface ao carregar listas: {e}")

    def extrair_id(self, string_combinada, tipo):
        """
        Extrai o ID da string formatada.
        Usuário formato: "Nome (ID: XXX)"
        Livro formato: "Titulo (Tombo: YYY)"
        """
        try:
            if tipo == "usuario":
                # Separa por "ID: " e pega o que vem depois até o ")"
                return string_combinada.split("(ID: ")[1].split(")")[0]
            elif tipo == "livro":
                # Separa por "Tombo: " e pega o que vem depois até o ")"
                return string_combinada.split("(Tombo: ")[1].split(")")[0]
        except IndexError:
            return ""

    def registrar_saida(self):
        usuario_selecionado = self.combo_usuario.get().strip()
        livro_selecionado = self.combo_livro.get().strip()
        dias = self.entry_dias.get().strip()

        id_usuario = self.extrair_id(usuario_selecionado, "usuario")
        id_tombo = self.extrair_id(livro_selecionado, "livro")

        if not id_usuario or not id_tombo:
            self.label_feedback.configure(text="Selecione um Usuário e um Livro válidos.", text_color="red")
            return

        try:
            sucesso, data_prevista = self.gestor.registrar_emprestimo(id_usuario, id_tombo, dias)
            if sucesso:
                msg = f"Empréstimo registrado com sucesso.\nDevolução prevista: {data_prevista}"
                self.label_feedback.configure(text=msg, text_color="green")
        except Exception as e:
            self.label_feedback.configure(text=f"Erro: {str(e)}", text_color="red")
            logging.error(f"Erro na interface de empréstimo: {e}")
