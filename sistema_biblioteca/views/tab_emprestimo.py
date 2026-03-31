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

        # Mapas internos para guardar o ID real correspondente ao texto selecionado
        self.mapa_usuarios = {}
        self.mapa_livros = {}

        # Carrega os dados para os ComboBoxes
        self.carregar_listas()

    def carregar_listas(self):
        """Busca usuários e livros e popula os comboboxes (sem expor o ID no texto primário)."""
        self.mapa_usuarios.clear()
        self.mapa_livros.clear()

        try:
            # Usuarios
            usuarios = self.gestor.obter_usuarios()
            lista_usuarios = []

            # Controle para nomes duplicados (ex: dois "João Silva")
            nomes_vistos = {}
            for u in usuarios:
                nome_base = u['nome'].strip()
                if nome_base in nomes_vistos:
                    nomes_vistos[nome_base] += 1
                    # Se tiver duplicata, adiciona um sufixo numérico sutil só para diferenciar
                    nome_exibicao = f"{nome_base} ({nomes_vistos[nome_base]})"
                else:
                    nomes_vistos[nome_base] = 1
                    nome_exibicao = nome_base

                lista_usuarios.append(nome_exibicao)
                # Guarda o ID real no dicionário, atrelado ao nome exato do ComboBox
                self.mapa_usuarios[nome_exibicao] = u['id_usuario']

            if lista_usuarios:
                self.combo_usuario.configure(values=lista_usuarios)
                self.combo_usuario.set(lista_usuarios[0])
            else:
                self.combo_usuario.configure(values=["Nenhum usuário cadastrado"])
                self.combo_usuario.set("Nenhum usuário cadastrado")

            # Livros
            livros = self.gestor.obter_livros()
            lista_livros = []

            titulos_vistos = {}
            for l in livros:
                titulo_base = l['titulo_curto'].strip()
                if titulo_base in titulos_vistos:
                    titulos_vistos[titulo_base] += 1
                    titulo_exibicao = f"{titulo_base} - Cópia {titulos_vistos[titulo_base]}"
                else:
                    titulos_vistos[titulo_base] = 1
                    titulo_exibicao = titulo_base

                lista_livros.append(titulo_exibicao)
                # Guarda o Tombo real (ID numérico) no dicionário
                self.mapa_livros[titulo_exibicao] = l['id_tombo']

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

    def registrar_saida(self):
        usuario_selecionado = self.combo_usuario.get().strip()
        livro_selecionado = self.combo_livro.get().strip()
        dias = self.entry_dias.get().strip()

        # Resgata os IDs reais usando os dicionários internos mapeados
        id_usuario = self.mapa_usuarios.get(usuario_selecionado)
        id_tombo = self.mapa_livros.get(livro_selecionado)

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
