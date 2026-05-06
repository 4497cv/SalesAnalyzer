"""
Reclasifica todas las sesiones usando las reglas mejoradas de auto_label.py.
Preserva solo las correcciones manuales definidas en apply_corrections.py.
"""
import os, sys, unicodedata
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

from auto_label import RULES, classify, read_processed, norm
from apply_corrections import CORRECTIONS

MANUAL = {norm(k): v for k, v in CORRECTIONS.items()}

def main():
    clases_path = 'ML/tf_idf_matrix_clases.csv'
    df = pd.read_csv(clases_path, encoding='utf-8-sig')
    df['Chat'] = df['Chat'].apply(norm)

    changes = {}   # clase_vieja -> clase_nueva -> count
    no_corpus = []
    manual_kept = 0

    for idx, row in df.iterrows():
        chat = row['Chat']
        old_clase = row['Clase'] if pd.notna(row['Clase']) else ''

        # Manual corrections always win
        if chat in MANUAL:
            new_clase = MANUAL[chat]
            df.at[idx, 'Clase'] = new_clase
            manual_kept += 1
            continue

        # No corpus sessions stay as-is
        parts = chat.split('/')
        if len(parts) < 2:
            no_corpus.append(chat)
            continue

        client, session = parts[0], parts[1]
        text, msg_count = read_processed(client, session)
        if not text:
            no_corpus.append(chat)
            continue

        new_clase, _ = classify(text, msg_count)
        df.at[idx, 'Clase'] = new_clase

        if old_clase != new_clase:
            key = (old_clase, new_clase)
            changes[key] = changes.get(key, 0) + 1

    df.to_csv(clases_path, index=False, encoding='utf-8-sig')

    print(f"Correcciones manuales preservadas: {manual_kept}")
    print(f"Sin corpus (sin cambio): {len(no_corpus)}")
    print(f"\nCambios realizados ({sum(changes.values())} total):")
    for (old, new), cnt in sorted(changes.items(), key=lambda x: -x[1]):
        print(f"  {old} → {new}: {cnt}")

    print("\nDistribución final:")
    print(df['Clase'].value_counts(dropna=False).to_string())

if __name__ == '__main__':
    main()
