import os
import zipfile
from collections import defaultdict
from datetime import datetime
import workspace

SOURCE_DIR = workspace.get_workspace_path()
CORPUS_DIR = workspace.get_corpus_path()
EXPORTS_DIR = workspace.get_chat_exports()

report_entries = []

def parse_chat_lines(lines, chat_name):
    by_date = defaultdict(list)
    for line in lines:
        line = line.replace("\n", "").strip()
        if not line:
            continue

        # Procesar formato de whatsapp actual: [DD/MM/YY, HH:MM:SS a.m.] Author: Message
        if line.startswith("["):
            bracket_end = line.find("]")
            if bracket_end == -1:
                continue
            date_time = line[1:bracket_end]
            date_parts = date_time.split(",", 1)
            if len(date_parts) < 2:
                continue
            raw_date = date_parts[0].strip()
        else:
            # Procesar formato de whatsapp antiguo: DD/MM/YYYY, HH:MM - Author: Message
            parts = line.split("-", 1)
            if len(parts) < 2:
                continue
            date_time = parts[0].strip()
            date_parts = date_time.split(",", 1)
            if len(date_parts) < 2:
                continue
            raw_date = date_parts[0].strip()

        try:
            day, month, year = raw_date.split("/")
            if len(year) == 2:
                year = "20" + year
            folder_date = f"{int(day):02d}-{int(month):02d}-{year}"
        except ValueError:
            continue

        by_date[folder_date].append(line)
        
    return by_date

def get_client_name(chat_name):
    prefix = "Chat de WhatsApp con "
    if chat_name.startswith(prefix):
        return chat_name[len(prefix):]
    return chat_name

def save_corpus(by_date, chat_name):
    client = get_client_name(chat_name)
    total_messages = 0

    for date, messages in by_date.items():
        date_dir = os.path.join(CORPUS_DIR, client, date)
        os.makedirs(date_dir, exist_ok=True)
        out_path = os.path.join(date_dir, "mensajes.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(messages))
        print(f"  {client}/{date} — {len(messages)} mensajes")
        total_messages += len(messages)
    
    report_entries.append((client, len(by_date), total_messages))

def process_txt(filepath):
    # obtener el nombre del chat objetivo
    chat_name = os.path.splitext(os.path.basename(filepath))[0]

    # obtener el contenido del archivo especificado
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # procesar el contenido del chat
    by_date = parse_chat_lines(lines, chat_name)

    # almacenar el contenido del chat por cliente y fecha en el corpus
    save_corpus(by_date, chat_name)

def process_zip(filepath):
    # obtener el nombre del archivo zip 
    zip_name = os.path.splitext(os.path.basename(filepath))[0]

    with zipfile.ZipFile(filepath, "r") as z:
        for name in z.namelist():
            if name.endswith(".txt"):
                base = os.path.splitext(os.path.basename(name))[0]
                # _chat.txt es el nombre generico que usan las exportaciones nuevas de WhatsApp
                chat_name = zip_name if base == "_chat" else base
                with z.open(name) as f:
                    lines = f.read().decode("utf-8").splitlines(keepends=True)
                by_date = parse_chat_lines(lines, chat_name)
                save_corpus(by_date, chat_name)

def run():
    # exportamos chats de whatsapp si el directorio del corpus no existe
    if not os.path.isdir(CORPUS_DIR):
        print("Exportando chats de archivos .zip")
        # verificar si el directorio EXPORTS_DIR existe
        if os.path.isdir(EXPORTS_DIR):
            for filename in os.listdir(EXPORTS_DIR):
                if filename.endswith(".zip"):
                    filepath = os.path.join(EXPORTS_DIR, filename)
                    print(f"Procesando zip: {filename}")
                    process_zip(filepath)
        else:
            print(f"Carpeta no encontrada: {EXPORTS_DIR}")
    else:
        print(f"La carpeta {CORPUS_DIR} ya existe")

    # verificamos si existe el directorio de corpus
    if os.path.isdir(CORPUS_DIR):
        for filename in os.listdir(SOURCE_DIR):
            # obtener la ruta del archivo actual en el directoria principal del repositorio
            filepath = os.path.join(SOURCE_DIR, filename)
            # nombre del archivo sin extension
            filename_parsed = os.path.splitext(filename)[0] 
            # verificar que la extension del archivo sea .txt
            if(True == filename.endswith(".txt")) and\
            (filename_parsed not in ("mensajes", "mensajes_processed")):
                print(f"Procesando: {filename}")
                # iniciar el procesamiento del archivo
                process_txt(filepath)
    else:
        print(f"Carpeta no encontrada: {CORPUS_DIR}")


    print("\nCorpus generado en:", CORPUS_DIR)

    report_path = os.path.join(SOURCE_DIR, "corpus_report.log")

    with open(report_path, "w", encoding="utf-8") as r:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        r.write(f"Reporte de corpus — {timestamp}\n")
        total_sesiones = sum(n for _, n, _ in report_entries)
        r.write(f"Total de chats procesados: {len(report_entries)}\n")
        r.write(f"Total de sesiones: {total_sesiones}\n\n")
        for client, num_dates, num_messages in sorted(report_entries):
            r.write(f"  {client}: {num_dates} sesiones, {num_messages} mensajes\n")

    print(f"Reporte guardado en: {report_path}")
