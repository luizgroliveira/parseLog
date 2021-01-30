import logging
from pathlib import Path, PurePath
import os
import sys
import time
import argparse

def main(work_path, log_name):
    start = time.process_time()

    class InputError(Exception):
        pass

    workspace_path = Path(work_path)
    #workspace_new  = PurePath(workspace_path, "new")
    workspace_old  = PurePath(workspace_path.parent, "old")
    workspace_done = PurePath(workspace_path.parent, "done")
    workspace_log  = PurePath(workspace_path.parent, "log")
    file_log_name  = log_name

    files = Path(workspace_path)

    if not files.is_dir():
        logging.fatal(f"O caminho de origem informado não é um diretório: {workspace_path}")
        logging.fatal("Programa finalizado com erro.")
        raise InputError(f"O caminho de origem informado não é um diretório: {workspace_path}")

    if not Path(workspace_log).exists():
            logging.warning("Diretório de arquivos dos logs não existe, o mesmo sera criado")
            Path(workspace_log).mkdir()
            logging.warning(f"Criado o diretório de log: {workspace_log}")

    #if not Path(workspace_new).exists():
    #        logging.warning("Diretório de arquivos novos não existe, o mesmo sera criado")
    #        Path(workspace_new).mkdir()
    #        logging.warning(f"Criado o diretório de arquivos novos: {workspace_new}")

    handler = logging.StreamHandler()
    formater = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formater)

    logging.getLogger().addHandler(handler)

    handler = logging.FileHandler(filename=f"{workspace_log}/concatenate.log", mode="a", encoding="utf-8")
    handler.setFormatter(formater)

    logging.getLogger().addHandler(handler)
    #logging.getLogger().setLevel(logging.INFO)

    files = os.listdir(files)

    if len(files) == 0:
        logging.info(f"Não foram encontrados arquivos no {workspace_path}")
    else:
        logging.info(f"Arquivos encontrados em {workspace_path}: {len(files)}")
        logging.debug(f"Lista dos arquivos encontrados: {', '.join(files)}")

        if not Path(workspace_done).exists():
            logging.warning("Diretório concluído não existe, o mesmo sera criado")
            Path(workspace_done).mkdir()
            logging.warning(f"Criado o diretório done: {workspace_done}")

        if not Path(workspace_old).exists():
            logging.warning("Diretório old para arquivos processados não existe, o mesmo sera criado")
            Path(workspace_old).mkdir()
            logging.warning(f"Criado o diretório old para processados: {workspace_old}")

        if not Path(workspace_log).exists():
            logging.warning("Diretório de arquivos dos logs não existe, o mesmo sera criado")
            Path(workspace_log).mkdir()
            logging.warning(f"Criado o diretório de log: {workspace_log}")

        try:
            file_log = PurePath(workspace_done, file_log_name)
            logging.info(f"Gerando o arquivo concatenado: {file_log}")
            with open(file_log, "a") as outfile:
                for indice, arquivo in enumerate(files, start=1):
                    logging.info(f"Concatenando o arquivo [{indice}/{len(files)}]: {PurePath(workspace_path, arquivo)}")
                    with open(PurePath(workspace_path, arquivo), "r") as infile:
                        outfile.write(infile.read())
                        logging.info(f"Conteudo do arquivo gravado com sucesso: {PurePath(workspace_path, arquivo)}")
                    logging.info(f"Movendo arquivo para o diretorio old: {PurePath(workspace_old, arquivo)}")
                    Path(PurePath(workspace_path, arquivo)).rename(PurePath(workspace_old, arquivo))
                #outfile.write("\n")
            stop = time.process_time()
            logging.info(f"Todos os arquivos foram processados com sucesso em: {stop - start}s")
        except Exception as e:
            logging.error(f"Exeção não mapeada: {e} - {sys.exc_info()}")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Diretório aonde encontram-se os arquivos a serem concatenados", type=str)
    parser.add_argument("-o", "--output", help="Nome do arquivo concatenado (default: base_email.csv)", default="base_email.csv", type=str)
    parser.add_argument("-v", "--verbose", help="Habilita o nível de debug", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.info(f"Habilitando a execução em modo debug")
        logging.getLogger().setLevel(logging.DEBUG)

    main(args.dir, args.output)