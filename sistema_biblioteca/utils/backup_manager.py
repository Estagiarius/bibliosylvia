import shutil
import os
import logging
from datetime import datetime
from database.db_config import get_db_path

def realizar_backup(diretorio_destino):
    """
    Copia o banco de dados 'dados_escola.db' para o diretório de destino fornecido,
    adicionando a data atual ao nome do arquivo.
    """
    if not diretorio_destino:
        raise ValueError("Diretório de destino não especificado.")

    if not os.path.exists(diretorio_destino) or not os.path.isdir(diretorio_destino):
        raise ValueError(f"O diretório destino '{diretorio_destino}' não é válido.")

    caminho_db_origem = get_db_path()

    if not os.path.exists(caminho_db_origem):
        raise FileNotFoundError(f"Arquivo de banco de dados não encontrado em: {caminho_db_origem}")

    data_atual_str = datetime.now().strftime('%d_%m_%Y')
    novo_nome = f"dados_escola_backup_{data_atual_str}.db"
    caminho_db_destino = os.path.join(diretorio_destino, novo_nome)

    try:
        shutil.copy2(caminho_db_origem, caminho_db_destino)
        logging.info(f"Backup realizado com sucesso: {caminho_db_destino}")
        return caminho_db_destino
    except IOError as e:
        erro_msg = f"Falha de I/O ao gravar o arquivo de backup em {caminho_db_destino}: {e}"
        logging.error(erro_msg)
        raise IOError(erro_msg)
    except Exception as e:
        erro_msg = f"Erro inesperado ao realizar backup: {e}"
        logging.error(erro_msg)
        raise RuntimeError(erro_msg)
