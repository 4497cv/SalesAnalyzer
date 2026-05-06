"""
Extrae un resumen compacto de cada sesión del corpus para clasificación manual.
Solo procesa sesiones auto-etiquetadas o sin etiqueta (no las etiquetadas a mano por el usuario).
"""
import os, sys, unicodedata, json
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

CORPUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpus')
SELLERS = {'Comercios Unidos', 'Permagraf'}

# Etiquetas puestas manualmente por el usuario (no auto_label.py)
# Las detectamos comparando con el CSV original antes del auto_label
# Por simplicidad: re-procesamos TODAS las sesiones
def norm(s):
    return unicodedata.normalize('NFC', str(s))

def read_messages(client, session):
    for fname in ('mensajes.txt', 'mensajes_processed.txt'):
        path = os.path.join(CORPUS_DIR, client, session, fname)
        if os.path.exists(path):
            msgs = []
            with open(path, encoding='utf-8-sig') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if ':' in line:
                        author, text = line.split(':', 1)
                        author = author.strip()
                        text = text.strip()
                    else:
                        author, text = '?', line
                    if text:
                        msgs.append({'author': author, 'text': text})
            return msgs
    return []

def summarize(msgs, max_chars=300):
    """Concatena los primeros mensajes del cliente hasta max_chars."""
    client_texts = [m['text'] for m in msgs if m['author'] not in SELLERS]
    snippet = ' | '.join(client_texts)
    return snippet[:max_chars]

def main():
    clases_df = pd.read_csv('ML/tf_idf_matrix_clases.csv', encoding='utf-8-sig')

    summaries = []
    missing = []

    for _, row in clases_df.iterrows():
        chat = norm(str(row['Chat']))
        clase = row['Clase'] if pd.notna(row['Clase']) else ''
        parts = chat.split('/')
        if len(parts) < 2:
            missing.append(chat)
            continue
        client, session = parts[0], parts[1]
        msgs = read_messages(client, session)
        if not msgs:
            missing.append(chat)
            summaries.append({'chat': chat, 'clase_actual': clase,
                               'n_msgs': 0, 'snippet': '[SIN CORPUS]'})
            continue
        snippet = summarize(msgs)
        summaries.append({
            'chat': chat,
            'clase_actual': clase,
            'n_msgs': len(msgs),
            'snippet': snippet
        })

    with open('ML/summaries.json', 'w', encoding='utf-8') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)

    print(f"Resúmenes generados: {len(summaries)}")
    print(f"Sin corpus: {len(missing)}")

if __name__ == '__main__':
    main()
