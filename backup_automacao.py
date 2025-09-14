import os
import shutil
import datetime

# Diretórios principais
SOURCE_DIR = "/home/valcann/backupsFrom"   # Onde os arquivos chegam
DEST_DIR = "/home/valcann/backupsTo"       # Onde os arquivos recentes serão copiados
LOG_FROM = "/home/valcann/backupsFrom.log" # Log com detalhes dos arquivos originais
LOG_TO = "/home/valcann/backupsTo.log"     # Log com os arquivos copiados

# Data atual (para comparar a idade dos arquivos)
today = datetime.datetime.now()

# 1. Listar arquivos do diretório de origem e registrar no log
with open(LOG_FROM, "w") as log_from:
    log_from.write("=== Lista de arquivos do diretório de origem ===\n")
    for filename in os.listdir(SOURCE_DIR):              # Percorre todos os arquivos da pasta
        filepath = os.path.join(SOURCE_DIR, filename)    # Caminho completo do arquivo
        if os.path.isfile(filepath):                     # Garante que é um arquivo (não uma pasta)
            stats = os.stat(filepath)                    # Pega informações do arquivo
            size = stats.st_size                         # Tamanho em bytes
            created = datetime.datetime.fromtimestamp(stats.st_ctime)   # Data de criação
            modified = datetime.datetime.fromtimestamp(stats.st_mtime)  # Última modificação
            # Escreve os dados no arquivo de log
            log_from.write(f"Arquivo: {filename}\n")
            log_from.write(f"Tamanho: {size} bytes\n")
            log_from.write(f"Criado em: {created}\n")
            log_from.write(f"Última modificação: {modified}\n")
            log_from.write("-----------------------------\n")

# 2 e 3. Verificar cada arquivo e separar por idade
with open(LOG_TO, "w") as log_to:
    log_to.write("=== Arquivos copiados para backupsTo ===\n")
    for filename in os.listdir(SOURCE_DIR):              # Percorre novamente os arquivos
        filepath = os.path.join(SOURCE_DIR, filename)
        if os.path.isfile(filepath):
            created = datetime.datetime.fromtimestamp(os.stat(filepath).st_ctime)
            days_old = (today - created).days             # Calcula quantos dias o arquivo tem

            if days_old > 3:
                # Se o arquivo tiver mais de 3 dias → remover
                os.remove(filepath)
            else:
                # Se tiver até 3 dias → copiar para a pasta de destino
                shutil.copy(filepath, DEST_DIR)
                # Registrar no log de destino
                log_to.write(f"Arquivo: {filename} - Copiado em {today}\n")
