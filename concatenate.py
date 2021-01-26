import logging
from pathlib import Path, PurePath
import os
import sys
import time

start = time.process_time()

class InputError(Exception):
    pass

handler = logging.StreamHandler()
formater = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formater)

logging.getLogger().addHandler(handler)

handler = logging.FileHandler(filename="concatenate.log", mode="a", encoding="utf-8")
handler.setFormatter(formater)  

logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.DEBUG)


workspace_path = "/home/lgro/git/parseLog"
workspace_new  = PurePath(workspace_path, "new")
workspace_old  = PurePath(workspace_path, "old")
workspace_done = PurePath(workspace_path, "done")
file_log_name  = "log-concatenado.csv"

files = Path(workspace_new)

if not files.is_dir():
    logging.fatal(f"O caminho de origem informado não é um diretório: {workspace_new}")
    logging.fatal("Programa finalizado com erro.")
    raise InputError(f"O caminho de origem informado não é um diretório: {workspace_new}")

files = os.listdir(files)

if len(files) == 0:
    logging.info(f"Não foram encontrados arquivos no {workspace_new}")
else:
    logging.info(f"Arquivos encontrados em {workspace_new}: {len(files)}")
    logging.debug(f"Lista dos arquivos encontrados: {', '.join(files)}")

    if not Path(workspace_done).exists():
        logging.warning("Diretório de log não exite, o mesmo sera criado")
        Path(workspace_done).mkdir()
        logging.warning(f"Criado o diretório de log: {workspace_done}")

    if not Path(workspace_old).exists():
        logging.warning("Diretório de arquivos processados não exite, o mesmo sera criado")
        Path(workspace_old).mkdir()
        logging.warning(f"Criado o diretório de log: {workspace_old}")

    try:
        file_log = PurePath(workspace_done, file_log_name)
        logging.info(f"Gerando o arquivo concatenado: {file_log}")
        with open(file_log, "w") as outfile:
            for indice, arquivo in enumerate(files, start=1):
                logging.info(f"Contatenando o arquivo [{indice}/{len(files)}]: {PurePath(workspace_new, arquivo)}")
                with open(PurePath(workspace_new, arquivo), "r") as infile:
                    outfile.write(infile.read())
                    logging.info(f"Conteudo do arquivo gravado com sucesso: {PurePath(workspace_new, arquivo)}")
                logging.info(f"Movendo arquivo para o diretorio old: {PurePath(workspace_old, arquivo)}")
                Path(PurePath(workspace_new, arquivo)).rename(PurePath(workspace_old, arquivo))
            outfile.write("\n")
        stop = time.process_time()
        logging.info(f"Todos os arquivos foram processados com sucesso em: {stop - start}s")
    except Exception as e:
        logging.error(f"Exeção não mapeada: {e} - {sys.exc_info()}")