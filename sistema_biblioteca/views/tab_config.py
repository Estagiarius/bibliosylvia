import customtkinter as ctk
from tkinter import filedialog
import logging
import traceback
from utils.backup_manager import realizar_backup

class TabConfig(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="Configurações e Backup", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

        # Container
        self.frame_config = ctk.CTkFrame(self)
        self.frame_config.pack(pady=10, padx=20, fill="x")

        # Descrição
        self.label_desc = ctk.CTkLabel(
            self.frame_config,
            text="Gere uma cópia do banco de dados (backup) para segurança.\n"
                 "Isso é útil para gravar em pendrives.",
            justify="center"
        )
        self.label_desc.pack(pady=10)

        # Botão Backup
        self.btn_backup = ctk.CTkButton(self.frame_config, text="Realizar Backup do Banco de Dados", command=self.fazer_backup)
        self.btn_backup.pack(pady=20)

        # Label de Feedback
        self.label_feedback = ctk.CTkLabel(self, text="", text_color="green", wraplength=400)
        self.label_feedback.pack(pady=10)

    def fazer_backup(self):
        # Abre o dialog para o usuário escolher o diretório de destino
        diretorio_destino = filedialog.askdirectory(title="Selecione a pasta para salvar o backup")

        if not diretorio_destino:
            self.label_feedback.configure(text="Aviso: Operação cancelada pelo usuário.", text_color="orange")
            return

        try:
            caminho_salvo = realizar_backup(diretorio_destino)
            self.label_feedback.configure(text=f"Sucesso! Backup salvo em:\n{caminho_salvo}", text_color="green")
        except Exception as e:
            # Pegamos o traceback detalhado para o log, mas a string limpa para o usuário
            erro_msg = str(e)
            self.label_feedback.configure(text=f"Erro Crítico: {erro_msg}", text_color="red")
            logging.error(f"Erro na aba de backup: {erro_msg}\n{traceback.format_exc()}")
