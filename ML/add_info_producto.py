import pandas as pd
import unicodedata

def normalize(s):
    return unicodedata.normalize('NFC', str(s).strip())

new_labels = [
    "T1 Carmen Karful 45143/02-03-2026",
    "T1 Carmen Karful 45143/03-02-2026",
    "T1 Carmen Karful 45143/28-02-2026",
    "T1 Carmen Karful 45143/28-03-2026",
    "T2  Oriana 46797 Taller Capule Oriana/05-06-2025",
    "T2  Oriana 46797 Taller Capule Oriana/21-10-2025",
    "T2  Oriana 46797 Taller Capule Oriana/26-09-2025",
    "T2 44338_Chavez A_Victoria/02-09-2025",
    "T2 45101 Vision C_ Cleam/07-05-2025",
    "T2 45101 Vision C_ Cleam/23-09-2025",
    "T2 Daniela 46752/02-09-2025",
    "T2 Daniela 46752/03-12-2024",
    "T2 Daniela 46752/14-01-2026",
    "T2 Daniela 46752/17-12-2025",
    "T2 Daniela 46752/22-10-2024",
    "T2 Daniela 46752/27-09-2024",
    "T2 Daniela 46752/28-03-2025",
    "T2 Daniela 46752/31-01-2025",
    "T4  Carnes selec compras 19256 Sel/14-03-2026",
    "T4  Carnes selec compras 19256 Sel/15-04-2026",
    "T4  Carnes selec compras 19256 Sel/24-01-2026",
    "T4  Carnes selec compras 19256 Sel/30-01-2026",
    "T4 Copycos 16807/20-04-2026",
    "T4 Copycos 16807/21-04-2026",
    "T4 Cuprum Constitucion 44531/05-03-2026",
    "T5 Castilla Shaula/11-03-2026",
    "T5 Castilla Shaula/17-04-2026",
    "t6 CASSANDRA ADMINISTRACION CHINIZA/09-02-2026",
    "T6 Michelle GPS (45574)/14-04-2026",
    "T6 Michelle GPS (45574)/27-03-2026",
    "T6 Sistemas de Impresion Elect. Compras/07-04-2026",
    "T9 Ferre laminas 46266/24-03-2026",
    "T9 Huma Uniformes Y Bordados 41403/04-03-2026",
    "T9 Huma Uniformes Y Bordados 41403/25-03-2026",
    "T9 Miriam Fienmont 45737 Miriam/16-02-2026",
    "T9 Miriam Fienmont 45737 Miriam/18-02-2026",
]

clases_path = "ML/tf_idf_matrix_clases.csv"
df = pd.read_csv(clases_path, encoding="utf-8-sig")
df['Chat'] = df['Chat'].apply(normalize)

new_labels_norm = [normalize(c) for c in new_labels]

matched = 0
already_labeled = 0
not_found = []

for chat_id in new_labels_norm:
    mask = df['Chat'] == chat_id
    if mask.any():
        existing = df.loc[mask, 'Clase'].values[0]
        if pd.notna(existing):
            already_labeled += 1
            print(f"  OVERWRITE [{existing}] → Información de Producto: {chat_id}")
        else:
            matched += 1
        df.loc[mask, 'Clase'] = "Información de Producto"
    else:
        not_found.append(chat_id)

df.to_csv(clases_path, index=False, encoding="utf-8-sig")

print(f"\nResultado:")
print(f"  Nuevas etiquetas: {matched}")
print(f"  Sobreescritas:    {already_labeled}")
print(f"  No encontradas:   {len(not_found)}")
if not_found:
    for c in not_found:
        print(f"    !! {c}")

print("\nDistribución actual:")
print(df['Clase'].value_counts(dropna=False).to_string())
