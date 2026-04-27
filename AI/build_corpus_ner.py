"""
build_corpus_ner.py
Version de build_corpus.py con Named Entity Recognition (NER).

Hace exactamente lo mismo que build_corpus.py (parseo, agrupacion por fecha,
escritura de mensajes.txt y corpus_report.log), y ademas:

  1. Corre spaCy NER estadistico (es_core_news_md) sobre cada mensaje.
  2. Aplica un EntityRuler con patrones de dominio comercial:
       PRECIO    — "$100", "150 pesos", "1,200 MXN", etc.
       EMAIL     — direcciones de correo
       TELEFONO  — numeros de 10 digitos (formato MX)
       NUM_ORDEN — codigos de orden/pedido alfanumericos
  3. Escribe corpus/{client}/{date}/mensajes_ner.json con anotaciones inline.
  4. Escribe output/ner_entities.csv con todas las entidades del corpus.
  5. Escribe ner_report.log con estadisticas de entidades por cliente/sesion.

Instalacion requerida:
  pip install spacy
  python -m spacy download es_core_news_md
  (alternativa mas rapida: python -m spacy download es_core_news_sm)
"""

import os
import sys
import json
import zipfile
import re
from collections import defaultdict
from datetime import datetime

# ── path setup ────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import workspace

# ── spaCy setup ───────────────────────────────────────────────────────────────
try:
    import spacy
    from spacy.language import Language
except ImportError:
    print("ERROR: spaCy no esta instalado.")
    print("  pip install spacy")
    sys.exit(1)

SPACY_MODEL = "es_core_news_md"
FALLBACK_MODEL = "es_core_news_sm"

def load_nlp():
    for model in (SPACY_MODEL, FALLBACK_MODEL):
        try:
            nlp = spacy.load(model)
            print(f"Modelo spaCy cargado: {model}")
            return nlp
        except OSError:
            continue
    print(f"ERROR: Ningun modelo spaCy encontrado.")
    print(f"  python -m spacy download {SPACY_MODEL}")
    print(f"  python -m spacy download {FALLBACK_MODEL}")
    sys.exit(1)

# ── EntityRuler: patrones de dominio comercial ────────────────────────────────

PRECIO_PATTERNS = [
    # $1,200  /  $1200  /  $ 200
    {"label": "PRECIO", "pattern": [{"TEXT": {"REGEX": r"^\$\d[\d,]*(\.\d+)?$"}}]},
    # 1200 pesos / 1,200 pesos
    {"label": "PRECIO", "pattern": [
        {"TEXT": {"REGEX": r"^\d[\d,]*(\.\d+)?$"}},
        {"LOWER": {"IN": ["pesos", "mxn", "mx", "dlls", "dolares", "usd"]}}
    ]},
    # $ 1200 (con espacio)
    {"label": "PRECIO", "pattern": [
        {"TEXT": "$"},
        {"TEXT": {"REGEX": r"^\d[\d,]*(\.\d+)?$"}}
    ]},
]

EMAIL_PATTERNS = [
    {"label": "EMAIL", "pattern": [{"TEXT": {"REGEX": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"}}]},
]

TELEFONO_PATTERNS = [
    # 10 digitos seguidos
    {"label": "TELEFONO", "pattern": [{"TEXT": {"REGEX": r"^\d{10}$"}}]},
    # (55) 1234-5678 o 55-1234-5678
    {"label": "TELEFONO", "pattern": [{"TEXT": {"REGEX": r"^\(?\d{2,3}\)?\s?\d{4}[-\s]?\d{4}$"}}]},
]

NUM_ORDEN_PATTERNS = [
    # Codigos tipo OC-12345, PED-001, #12345
    {"label": "NUM_ORDEN", "pattern": [{"TEXT": {"REGEX": r"^(OC|PED|ORD|REF|FAC|TKT)[-\s]?\d{3,8}$", "FLAGS": re.IGNORECASE}}]},
    {"label": "NUM_ORDEN", "pattern": [
        {"TEXT": {"IN": ["#", "No.", "no.", "num.", "folio", "pedido", "orden"]}},
        {"TEXT": {"REGEX": r"^\d{3,8}$"}}
    ]},
]

ALL_RULER_PATTERNS = PRECIO_PATTERNS + EMAIL_PATTERNS + TELEFONO_PATTERNS + NUM_ORDEN_PATTERNS


def add_entity_ruler(nlp):
    """Agrega EntityRuler antes del NER estadistico para que los patrones de dominio tengan prioridad."""
    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True})
        ruler.add_patterns(ALL_RULER_PATTERNS)
    return nlp


# ── parseo de lineas WhatsApp ─────────────────────────────────────────────────

# Formato: "DD/MM/YYYY, HH:MM - Autor: texto"
LINE_RE = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[ap]\.?\s*m\.?)?)\s*-\s*([^:]+):\s*(.+)$",
    re.IGNORECASE,
)


def parse_line(line: str):
    """
    Retorna (folder_date, author, text) o None si la linea no coincide.
    folder_date tiene formato DD-MM-YYYY.
    """
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    raw_date, _, author, text = m.groups()
    try:
        day, month, year = raw_date.split("/")
        folder_date = f"{int(day):02d}-{int(month):02d}-{year}"
    except ValueError:
        return None
    return folder_date, author.strip(), text.strip()


def parse_chat_lines(lines):
    """Agrupa lineas por fecha; retorna dict[folder_date -> list[raw_line]]."""
    by_date = defaultdict(list)
    for line in lines:
        line = line.replace("\n", "").strip()
        if not line:
            continue
        parsed = parse_line(line)
        if parsed:
            folder_date = parsed[0]
            by_date[folder_date].append(line)
    return by_date


def get_client_name(chat_name: str) -> str:
    prefix = "Chat de WhatsApp con "
    return chat_name[len(prefix):] if chat_name.startswith(prefix) else chat_name


# ── NER sobre un mensaje ──────────────────────────────────────────────────────

def extract_entities(text: str, nlp) -> list[dict]:
    """Retorna lista de {text, label, start, end} para el texto dado."""
    doc = nlp(text)
    return [
        {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
        for ent in doc.ents
    ]


# ── escritura del corpus ──────────────────────────────────────────────────────

def process_session(raw_lines: list[str], client: str, date: str, nlp, corpus_dir: str) -> list[dict]:
    """
    Escribe mensajes.txt (identico al original) y mensajes_ner.json.
    Retorna lista de registros de entidades para el CSV global.
    """
    date_dir = os.path.join(corpus_dir, client, date)
    os.makedirs(date_dir, exist_ok=True)

    # mensajes.txt — sin cambios respecto al original
    with open(os.path.join(date_dir, "mensajes.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(raw_lines))

    # anotaciones NER
    annotated_messages = []
    entity_records = []

    for raw in raw_lines:
        parsed = parse_line(raw)
        if not parsed:
            continue
        _, author, text = parsed
        entities = extract_entities(text, nlp)

        annotated_messages.append({
            "author":   author,
            "text":     text,
            "entities": entities,
        })

        for ent in entities:
            entity_records.append({
                "client":  client,
                "session": date,
                "author":  author,
                "entity":  ent["text"],
                "label":   ent["label"],
                "context": text[:80],
            })

    # resumen de entidades por tipo para la sesion
    entity_summary = defaultdict(list)
    for msg in annotated_messages:
        for ent in msg["entities"]:
            val = ent["text"]
            if val not in entity_summary[ent["label"]]:
                entity_summary[ent["label"]].append(val)

    ner_doc = {
        "client":         client,
        "session":        date,
        "total_messages": len(annotated_messages),
        "entity_summary": dict(entity_summary),
        "messages":       annotated_messages,
    }

    with open(os.path.join(date_dir, "mensajes_ner.json"), "w", encoding="utf-8") as f:
        json.dump(ner_doc, f, ensure_ascii=False, indent=2)

    return entity_records


# ── procesado de fuentes ──────────────────────────────────────────────────────

def process_txt(filepath: str, nlp, corpus_dir: str) -> list[dict]:
    chat_name = os.path.splitext(os.path.basename(filepath))[0]
    client = get_client_name(chat_name)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    by_date = parse_chat_lines(lines)
    all_records = []
    for date, raw_lines in by_date.items():
        print(f"  {client}/{date} — {len(raw_lines)} mensajes")
        records = process_session(raw_lines, client, date, nlp, corpus_dir)
        all_records.extend(records)
    return all_records


def process_zip(filepath: str, nlp, corpus_dir: str) -> list[dict]:
    all_records = []
    with zipfile.ZipFile(filepath, "r") as z:
        for name in z.namelist():
            if name.endswith(".txt"):
                chat_name = os.path.splitext(os.path.basename(name))[0]
                client = get_client_name(chat_name)
                with z.open(name) as f:
                    lines = f.read().decode("utf-8").splitlines(keepends=True)
                by_date = parse_chat_lines(lines)
                for date, raw_lines in by_date.items():
                    print(f"  {client}/{date} — {len(raw_lines)} mensajes")
                    records = process_session(raw_lines, client, date, nlp, corpus_dir)
                    all_records.extend(records)
    return all_records


# ── reporte ───────────────────────────────────────────────────────────────────

def write_ner_report(all_records: list[dict], source_dir: str) -> None:
    """Escribe ner_report.log con estadisticas de entidades por cliente y tipo."""
    report_path = os.path.join(source_dir, "ner_report.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # agrupar por cliente
    by_client = defaultdict(list)
    for r in all_records:
        by_client[r["client"]].append(r)

    # conteo global por etiqueta
    label_counts = defaultdict(int)
    for r in all_records:
        label_counts[r["label"]] += 1

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Reporte NER — {timestamp}\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"Total de entidades extraidas: {len(all_records)}\n\n")

        f.write("Distribucion por etiqueta:\n")
        for label, count in sorted(label_counts.items(), key=lambda x: -x[1]):
            f.write(f"  {label:<15} {count}\n")

        f.write("\n")
        for client, records in sorted(by_client.items()):
            client_labels = defaultdict(set)
            for r in records:
                client_labels[r["label"]].add(r["entity"])
            f.write(f"\n{client} ({len(records)} entidades):\n")
            for label, vals in sorted(client_labels.items()):
                sample = sorted(vals)[:10]
                f.write(f"  {label}: {', '.join(sample)}\n")

    print(f"Reporte NER guardado en: {report_path}")


def write_ner_csv(all_records: list[dict], output_dir: str) -> None:
    """Escribe output/ner_entities.csv con todas las entidades."""
    import csv
    csv_path = os.path.join(output_dir, "ner_entities.csv")
    fieldnames = ["client", "session", "author", "label", "entity", "context"]
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_records)
    print(f"CSV de entidades guardado en: {csv_path}")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    workspace.set_workspace_path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    source_dir = workspace.get_workspace_path()
    corpus_dir = workspace.get_corpus_path()
    output_dir = workspace.get_output_path()
    exports_dir = os.path.join(source_dir, "chat exports")

    # cargar modelo NER
    nlp = load_nlp()
    nlp = add_entity_ruler(nlp)

    all_entity_records = []

    # procesar .txt sueltos en la raiz
    for filename in os.listdir(source_dir):
        if filename.endswith(".txt") and filename not in ("mensajes.txt", "mensajes_processed.txt"):
            print(f"\nProcesando: {filename}")
            filepath = os.path.join(source_dir, filename)
            records = process_txt(filepath, nlp, corpus_dir)
            all_entity_records.extend(records)

    # procesar .zip en chat exports/
    if os.path.isdir(exports_dir):
        for filename in os.listdir(exports_dir):
            if filename.endswith(".zip"):
                print(f"\nProcesando zip: {filename}")
                filepath = os.path.join(exports_dir, filename)
                records = process_zip(filepath, nlp, corpus_dir)
                all_entity_records.extend(records)
    else:
        print(f"Carpeta no encontrada: {exports_dir}")

    print(f"\nCorpus generado en: {corpus_dir}")
    print(f"Total entidades detectadas: {len(all_entity_records)}")

    # reportes
    write_ner_report(all_entity_records, source_dir)
    write_ner_csv(all_entity_records, output_dir)


if __name__ == "__main__":
    main()
