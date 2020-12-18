import argparse
import datetime
import re
import os
import csv
import sys
import logging  
from pathlib import Path, PurePath
import platform

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%m/%d/%Y %H:%M:%S', 
    level=logging.INFO)

class ParseLog():
    def __init__(self, arquivo, execucao=1, output_dir=f"{Path(Path.cwd(),'output')}", cabecalho=False):

        # Variaveis do arquivo csv
        self.cores = None
        self.erros = None
        self.execucao = execucao
        self.fim = None
        self.folder = None
        self.host1 = None
        self.host2 = None
        self.hostname = platform.uname()[1]
        self.inicio = None
        self.media_kb_segundo = None
        self.memoria_usada_mb = None
        self.mensagem_duplicada_destino = None
        self.mensagem_duplicada_origem = None
        self.mensagem_erro = "NAO ENCONTRADO"
        self.mensagem_ignorada = None
        self.mensagem_nula_destino = None
        self.mensagem_nula_origem = None
        self.mensagem_por_segundo = None
        self.mensagem_transferida = None
        self.tempo_total = None
        self.total_ignorado_kb = None
        self.total_mensagem_deletada_destino = None
        self.total_mensagem_deletada_origem = None
        self.total_mensagem_destino = None
        self.total_mensagem_origem = None
        self.total_transferido_kb = None
        self.usuario = None
        self.usuario2 = None

        # Variaveis de controle do programa
        self.arquivo = Path(arquivo).absolute()
        self.linhas = self.ler_arquivo_de_log(arquivo)
        self.output_dir = output_dir
        self.cabecalho = cabecalho

    def busca_data_inicio(self, linha):
        regex = r"Transfer started on\s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            data_obj = datetime.datetime.strptime(m.group(1), "%a %b %d %H:%M:%S %Y")
            self.inicio = data_obj.strftime("%d/%m/%Y %H:%M:%S")
            logging.debug(f"[{self.arquivo}] Data de Inicio: {self.inicio}")
        
    def busca_data_fim(self, linha):
        # Convertendo data do formato 'Fri Jul 24 00:39:09 2020' para '24/07/2020 00:39:09'
        regex = r"Transfer ended on\s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            data_obj = datetime.datetime.strptime(m.group(1), "%a %b %d %H:%M:%S %Y")
            self.fim = data_obj.strftime("%d/%m/%Y %H:%M:%S")
            logging.debug(f"[{self.arquivo}] Data de Fim: {self.fim}")

    def busca_tempo_total(self, linha):
        regex = r"Transfer time\s+: (.*) sec"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.tempo_total = m.group(1)
            logging.debug(f"[{self.arquivo}] Tempo total: {self.tempo_total}")

    def busca_pastas_sincronizada(self, linha):
        regex = r"Folders synced\s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.folder = m.group(1)
            logging.debug(f"[{self.arquivo}] Pastas sincronizadas: {self.folder}")

    def busca_mensagem_transferida(self, linha):
        regex = r"Messages transferred\s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.mensagem_transferida = m.group(1)
            logging.debug(f"[{self.arquivo}] Mensagem Transferiada: {self.mensagem_transferida}")

    def busca_mensagem_ignorada(self, linha):
        regex = r"Messages skipped \s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.mensagem_ignorada = m.group(1)
            logging.debug(f"[{self.arquivo}] Mensagem Ignorada: {self.mensagem_ignorada}")

    def busca_mensagem_duplicada_origem(self, linha):
        regex = r"Messages found duplicate on host1\s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.mensagem_duplicada_origem = m.group(1)
            logging.debug(f"[{self.arquivo}] Mensagem duplicada origem: {self.mensagem_duplicada_origem}")

    def busca_mensagem_duplicada_destino(self, linha):
        regex = r"Messages found duplicate on host2\s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.mensagem_duplicada_destino = m.group(1)
            logging.debug(f"[{self.arquivo}] Mensagem duplicada destino: {self.mensagem_duplicada_destino}")

    def busca_mensagem_nula_origem(self, linha):
        regex = r"Messages void \(noheader\) on host1\s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.mensagem_nula_origem = m.group(1)
            logging.debug(f"[{self.arquivo}] Mensagem nula origem: {self.mensagem_nula_origem}")


    def busca_mensagem_nula_destino(self, linha):
        regex = r"Messages void \(noheader\) on host2\s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.mensagem_nula_destino = m.group(1)
            logging.debug(f"[{self.arquivo}] Mensagem nula destino: {self.mensagem_nula_destino}")


    def busca_total_mensagem_origem(self, linha):
        regex = r"Messages found in host1 not in host2\s+: (\d+) messages"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.total_mensagem_origem = m.group(1)
            logging.debug(f"[{self.arquivo}] Total mensagem origem: {self.total_mensagem_origem}")

    def busca_total_mensagem_destino(self, linha):
        regex = r"Messages found in host2 not in host1\s+: (\d+) messages"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.total_mensagem_destino = m.group(1)
            logging.debug(f"[{self.arquivo}] Total mensagem destino: {self.total_mensagem_destino}")


    def busca_total_mensagem_deletada_origem(self, linha):
        regex = r"Messages deleted on host1\s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.total_mensagem_deletada_origem = m.group(1)
            logging.debug(f"[{self.arquivo}] Total mensagem deletada origem: {self.total_mensagem_deletada_origem}")

    def busca_total_mensagem_deletada_destino(self, linha):
        regex = r"Messages deleted on host2\s+: (.*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.total_mensagem_deletada_destino = m.group(1)
            logging.debug(f"[{self.arquivo}] Total mensagem deletada destino: {self.total_mensagem_deletada_destino}")


    def busca_total_transferido(self, linha):
        regex = r"Total bytes transferred\s+: ([^\s]*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.total_transferido_kb = m.group(1)
            logging.debug(f"[{self.arquivo}] Total transferido: {self.total_transferido_kb}")

    def busca_total_ignorado_kb(self, linha):
        regex = r"Total bytes skipped\s+: ([^\s]*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.total_ignorado_kb = m.group(1)
            logging.debug(f"[{self.arquivo}] Total ignorado KB: {self.total_ignorado_kb}")

    def busca_mensagem_por_segundo(self, linha):
        regex = r"Message rate\s+: ([^\s]*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.mensagem_por_segundo = m.group(1)
            logging.debug(f"[{self.arquivo}] Mensagem por segundo: {self.mensagem_por_segundo}")

    def busca_media_kb_por_segundo(self, linha):
        regex = r"Average bandwidth rate\s+: ([^\s]*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.media_kb_segundo = m.group(1)
            logging.debug(f"[{self.arquivo}] Média kb por segundo: {self.media_kb_segundo}")


    def busca_memoria_usada_media(self, linha):
        regex = r"Memory consumption at the end\s+: ([^\(]*) "
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.memoria_usada_mb = m.group(1)
            logging.debug(f"[{self.arquivo}] Mémória usada média: {self.memoria_usada_mb}")
            
    def busca_cores(self, linha):
        regex = r"Load end is\s+: .*(\d+) cores"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.cores = m.group(1)
            logging.debug(f"[{self.arquivo}] Quantidade de Cores: {self.cores}")


    def busca_usuario(self, linha):
        regex = r"^[^\s]*imapsync(.exe)? .* --user1 (?P<user1>[^\s]*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.usuario = m.group("user1")
            logging.debug(f"[{self.arquivo}] Usuário: {self.usuario}")


    def busca_usuario2(self, linha):
        regex = r"^[^\s]*imapsync(.exe)? .* --user2 (?P<user2>[^\s]*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.usuario2 = m.group("user2")
            logging.debug(f"[{self.arquivo}] Usuário2: {self.usuario2}")

    def busca_host1(self, linha):
        regex = r"^[^\s]*imapsync(.exe)? .* --host1 (?P<host1>[^\s]*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.host1 = m.group("host1")
            logging.debug(f"[{self.arquivo}] Host1: {self.host1}")

    def busca_host2(self, linha):
        regex = r"^[^\s]*imapsync(.exe)? .* --host2 (?P<host2>[^\s]*)"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.host2 = m.group("host2")
            logging.debug(f"[{self.arquivo}] Host2: {self.host2}")

    def busca_erros(self, linha):
        regex = r"Detected (\d+) errors"
        p = re.compile(regex)
        m = p.match(linha)
        if m: 
            self.erros = m.group(0)
            logging.debug(f"[{self.arquivo}] Erros: {self.erros}")
    
    def gravar_csv(self):
        try:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Erro ao criar diretório de saida: {self.output_dir}: {e}")
            os.sys.exit(1)

        try:
            output_csv = PurePath(self.output_dir,f"{Path(self.arquivo).name}.csv")
            with open(output_csv, 'a', newline='') as csvfile:
                file = csv.writer(csvfile, delimiter=";")

                if self.cabecalho and Path(output_csv).stat().st_size == 0:
                    file.writerow(
                        [
                            "INICIO",
                            "FIM",
                            "TEMPO_TOTAL",
                            "MENSAGEM_TRANSFERIDA",
                            "MENSAGEM_IGNORADA",
                            "MENSAGEM_DUPLICADA_ORIGEM",
                            "MENSAGEM_DUPLICADA_DESTINO",
                            "MENSAGEM_NULA_ORIGEM",
                            "MENSAGEM_NULA_DESTINO",
                            "TOTAL_MENSAGEM_ORIGEM",
                            "TOTAL_MENSAGEM_DESTINO",
                            "TOTAL_MENSAGEM_DELETADA_ORIGEM",
                            "TOTAL_MENSAGEM_DELETADA_DESTINO",
                            "TOTAL_TRANSFERIDO_KB",
                            "TOTAL_IGNORADO_KB",
                            "MENSAGEM_POR_SEGUNDO",
                            "MEDIA_KB_SEGUNDO",
                            "MEMORIA_USADA_MB",
                            "CORES",
                            "USUARIO",
                            "FOLDER",
                            "HOSTNAME",
                            "EXECUCAO",
                            "ERROS",
                            "MENSAGEM_ERRO",
                            "ARQUIVO",
                            "HOST1",
                            "HOST2",
                            "USUARIO2"
                        ]
                    )
                file.writerow(
                    [
                        self.inicio,
                        self.fim,
                        self.tempo_total,
                        self.mensagem_transferida,
                        self.mensagem_ignorada,
                        self.mensagem_duplicada_origem,
                        self.mensagem_duplicada_destino,
                        self.mensagem_nula_origem,
                        self.mensagem_nula_destino,
                        self.total_mensagem_origem,
                        self.total_mensagem_destino,
                        self.total_mensagem_deletada_origem,
                        self.total_mensagem_deletada_destino,
                        self.total_transferido_kb,
                        self.total_ignorado_kb,
                        self.mensagem_por_segundo,
                        self.media_kb_segundo,
                        self.memoria_usada_mb,
                        self.cores,
                        self.usuario,
                        self.folder,
                        self.hostname,
                        self.execucao,
                        self.erros,
                        self.mensagem_erro,
                        self.arquivo,
                        self.host1,
                        self.host2,
                        self.usuario2
                    ]
                )
                logging.info(f"[{self.arquivo}] Registros salvos com sucesso no arquivo {output_csv}")
        except Exception as e:
            logging.error(f"Erro ao abrir o arquivo csv {output_csv}: {e}")
            os.sys.exit(1)

    def ler_arquivo_de_log(self, arquivo):
        try:
            logging.debug(f"Lendo o arquivo de log: {arquivo}")
            return [x.strip() for x in Path(self.arquivo).read_text().splitlines()]
        except Exception as e:
            logging.error(f"Erro ao ler o arquivo {self.arquivo}: {e}")

    def realizar_parse(self):
        for linha in self.linhas:
            self.busca_data_inicio(linha)
            self.busca_data_fim(linha)
            self.busca_tempo_total(linha)
            self.busca_pastas_sincronizada(linha)
            self.busca_mensagem_transferida(linha)
            self.busca_mensagem_ignorada(linha)
            self.busca_mensagem_duplicada_origem(linha)
            self.busca_mensagem_duplicada_destino(linha)
            self.busca_mensagem_nula_origem(linha)
            self.busca_mensagem_nula_destino(linha)
            self.busca_total_mensagem_origem(linha)
            self.busca_total_mensagem_destino(linha)
            self.busca_total_mensagem_deletada_origem(linha)
            self.busca_total_mensagem_deletada_destino(linha)
            self.busca_total_transferido(linha)
            self.busca_total_ignorado_kb(linha)
            self.busca_mensagem_por_segundo(linha)
            self.busca_media_kb_por_segundo(linha)
            self.busca_memoria_usada_media(linha)
            self.busca_cores(linha)
            self.busca_usuario(linha)
            self.busca_usuario2(linha)
            self.busca_erros(linha)
            self.busca_host1(linha)
            self.busca_host2(linha)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arquivo", help="Arquivo de lgo a ser realizado o parse")
    parser.add_argument("-e", "--execucao", help="O número da execução (default: 1)", type=int, default=1)
    parser.add_argument("-c", "--cabecalho", help="Inclui o header no arquivo csv", action="store_true")
    parser.add_argument("-o", "--output", help="Diretório de saida do arquivo csv gerado (default: ./output)", default="output")
    parser.add_argument("-v", "--verbose", help="Habilita o nível de debug", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.info(f"Habilitando a execução em modo debug")
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        logging.info(f"Estamos na execução ({args.execucao}) do arquivo: {args.arquivo}")
        logcvs = ParseLog(arquivo=args.arquivo, execucao=args.execucao, output_dir=args.output, cabecalho=args.cabecalho)
        logcvs.realizar_parse()
        logcvs.gravar_csv()
        logging.info(f"Arquivo processado com sucesso: {args.arquivo}")
    except Exception as e:
        logging.error(f"Ocorreu erro ao executar a parse do arquivo {args.arquivo}: {e}")
        os.sys.exit(1)
