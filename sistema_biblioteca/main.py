import os
import sys
import logging
import customtkinter as ctk

# Adiciona o diretório atual ao sys.path para garantir que imports funcionem em modo standalone
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configuração global de Logging
# Ficará salvo no mesmo diretório de main.py (standalone)
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    logging.info("Iniciando o Sistema de Biblioteca Escolar.")
    try:
        from views.main_window import MainWindow
        from database.db_config import init_db

        # Inicializa o banco de dados (cria tabelas se não existirem)
        init_db()

        # Configuração da interface gráfica
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        app = MainWindow()
        app.mainloop()

        logging.info("Sistema encerrado normalmente.")
    except Exception as e:
        logging.critical(f"Falha crítica ao iniciar ou executar o sistema: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
