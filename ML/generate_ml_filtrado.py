"""
Genera ML/tf_idf_matrix_filtrado.csv y ML/tf_idf_clases_filtradas.csv
filtrando output/tf_idf_matrix.csv a solo las sesiones etiquetadas en
ML/tf_idf_matrix_clases.csv.
"""
import os
import pandas as pd
import unicodedata

def norm(s):
    return unicodedata.normalize('NFC', str(s))

workspace_dir = os.path.dirname(os.path.abspath(__file__))

# Cargar matriz TF-IDF completa
tfidf_path = os.path.join(workspace_dir, 'output', 'tf_idf_matrix.csv')
tfidf = pd.read_csv(tfidf_path, encoding='utf-8-sig', index_col=0)
tfidf.index = [norm(x) for x in tfidf.index]

# Cargar etiquetas (fuente de verdad)
clases_path = os.path.join(workspace_dir, 'ML', 'tf_idf_matrix_clases.csv')
clases = pd.read_csv(clases_path, encoding='utf-8-sig')
clases['Chat'] = clases['Chat'].apply(norm)

# Filtrar solo filas etiquetadas
labeled = clases.dropna(subset=['Clase'])
print(f"Sesiones etiquetadas: {len(labeled)} / {len(clases)} total")
print("\nDistribución de clases:")
print(labeled['Clase'].value_counts().to_string())

# Verificar que todos los chats etiquetados existen en la matriz TF-IDF
missing = labeled[~labeled['Chat'].isin(tfidf.index)]
if not missing.empty:
    print(f"\nADVERTENCIA: {len(missing)} chats en clases no encontrados en TF-IDF:")
    for row in missing.itertuples():
        print(f"  {row.Chat}")

# Filtrar la matriz TF-IDF
chats_labeled = labeled['Chat'].tolist()
tfidf_filtrado = tfidf.loc[tfidf.index.isin(chats_labeled)]
# Mantener el orden del archivo de clases
tfidf_filtrado = tfidf_filtrado.reindex([c for c in chats_labeled if c in tfidf_filtrado.index])

print(f"\nMatriz filtrada: {tfidf_filtrado.shape}")

# Guardar tf_idf_matrix_filtrado.csv
out_filtrado = os.path.join(workspace_dir, 'ML', 'tf_idf_matrix_filtrado.csv')
tfidf_filtrado.to_csv(out_filtrado, encoding='utf-8-sig')
print(f"Guardado: ML/tf_idf_matrix_filtrado.csv")

# Guardar tf_idf_clases_filtradas.csv (mismo orden que filtrado)
clases_filtradas = labeled[labeled['Chat'].isin(tfidf_filtrado.index)].copy()
clases_filtradas = clases_filtradas.set_index('Chat').reindex(tfidf_filtrado.index).reset_index()
clases_filtradas = clases_filtradas.rename(columns={'index': 'Chat'})
out_clases = os.path.join(workspace_dir, 'ML', 'tf_idf_clases_filtradas.csv')
clases_filtradas.to_csv(out_clases, index=False, encoding='utf-8-sig')
print(f"Guardado: ML/tf_idf_clases_filtradas.csv")
