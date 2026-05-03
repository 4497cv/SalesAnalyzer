import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import workspace

# === STOPWORDS ===
stop_es = set(stopwords.words('spanish'))

# Preservar solo negaciones y cuantificadores con valor semántico real
preservar = {'nunca', 'nada', 'sin', 'menos', 'poco'}
stop_es = stop_es - preservar

# Stopwords de dominio
local_stopwords = {
    # Nombres propios
    'kharely', 'karely', 'kareli', 'lupita', 'alejandra', 'alejanda', 'aleajandra',
    'mirna', 'oriana', 'casandra', 'sinali', 'sofia', 'neftali', 'cassandra',
    'karla', 'carla', 'silvia', 'dora', 'elia', 'betzavel', 'betzabel', 'carmen', 'lolis', 'michelle',
    'rossy', 'rosy', 'rosi', 'rosario', 'rui', 'zuleika', 'zuleica', 'zuelika', 'silva',
    'keyla', 'dora', 'ale', 'laura', 'pedro', 'maria', 'aracely', 'mari', 'raul', 'fabiola', 'tia', 'katia', 'andrea', 'lesli', 'victoria', 'vicbet', 'bic',
    'mari', 'sergio', 'elizabeth', 'patty', 'dios', 'alberto', 'angelita', 'ignacio', 'malu', 'armando', 'daniela', 'jaime', 'jesus', 'alicia',
    # Empresas / vendedor
    'permagraf', 'comercios', 'unidos', 'chiniza', 'siam',
    'auxcomprasvisioncleamcom', 'alejandrapermagrafgmailcom',
    'olfa', '.com', 'mvictoriaagri-nova.com', 'xerox', 'google', 'bic', 'cedis', 'gmail', 'com', 'mexicofolio', 'ptt', 'wa', 'epson',
    'permagrafgmail com', 'permagrafgmail', 'tallerelcapulehotmail', 'tallerelcapulehotmail com', 'pilot', 'kyma', 'pelikan', 'pritt', 'sharpie', 'carnes', 'gps', 'kinera', 'acco', 'azor', 'baco',
    # IDs
    't1', 't2', 't4', 't5', 't6',
    # Apellidos
    'laso', 'roman', 'mora',
    # Sistema WhatsApp
    'eliminaste', 'mensaje', 'eliminó', 'img', 'pdf', 'opus', 'stk', 'wa', 'webp', 'web', 'jpg', 
    # Ruido
    'aa', 'aaa', 'aaaa', 'aah', 'ah', 'ahh', 'ahhh', 'jaja', 'jajaja', 'jajajaja', 'este', 'ok', '☺️', '...', '0⁰', 'jeje', 'jejeje', 'jajaj', 'oh', 'eh', 'oye', 'pa', 'shola',
    # saludos
    'buenos', 'dias', 'día', 'buenas', 'tardes', 'hola', 'dia', 'gracias', 'muchas', 'bien', 'muy', 'hola', 'Qué onda', 'que onda',
    # palabras simpples
    'si', 'no', 'nose', 'pm', 'zas', 'qui', 'que', ' it', 'cf', 'mmm', 'mm',
    #articulos
    'ecg',
    # regionalismos
    'mija', 'onda', 'bendito', 'cañera', 'tomatera', 'dormilona', 
    # lugares
    'sanalona', 'culiacan', 'mazatlan', 'villas', 'estación', 'valle', 'alto',
}


todas_stopwords = list(stop_es | local_stopwords)


# === EXTRAER TEXTO POR CONVERSACIÓN ===
def _extract_text(line):
    parts = line.split(":", 1)
    return parts[1].strip() if len(parts) > 1 else ""

def cargar_conversaciones():
    """Retorna lista de (doc_name, texto_completo) por conversación."""
    corpus_dir = workspace.get_corpus_path()
    documentos = []
    nombres = []

    for client in sorted(os.listdir(corpus_dir)):
        client_path = os.path.join(corpus_dir, client)
        if not os.path.isdir(client_path):
            continue
        for session in sorted(os.listdir(client_path)):
            session_path = os.path.join(client_path, session)
            if not os.path.isdir(session_path):
                continue
            file_path = os.path.join(session_path, "mensajes_processed.txt")
            if not os.path.exists(file_path):
                continue

            with open(file_path, "r", encoding="utf-8-sig") as f:
                lineas = []
                for line in f:
                    line = line.strip()
                    # Filtrar mensajes de sistema
                    if 'eliminaste este mensaje' in line.lower():
                        continue
                    texto = _extract_text(line)
                    if texto:
                        lineas.append(texto)

            texto_completo = " ".join(lineas)
            if texto_completo.strip():  # No agregar docs vacíos
                documentos.append(texto_completo)
                nombres.append(f"{client}/{session}")

    return nombres, documentos

# === PIPELINE PRINCIPAL ===
def run():
    workspace.set_workspace_path(os.path.dirname(os.path.abspath(__file__)))
    output_path = workspace.get_output_path()

    nombres, documentos = cargar_conversaciones()
    print(f"Conversaciones cargadas: {len(documentos)}")

    # TF-IDF con bigramas
    vectorizer = TfidfVectorizer(
        stop_words=todas_stopwords,
        ngram_range=(1, 2),       # unigramas + bigramas
        min_df=3,                 # elimina typos raros
        max_df=0.90,              # elimina palabras ultra-comunes
        max_features=2000,        # limita dimensionalidad
        token_pattern=r'[a-záéíóúüñ]{2,}'  # palabras de 2+ letras, incluye acentos
    )

    X = vectorizer.fit_transform(documentos)
    print(f"Matriz TF-IDF: {X.shape}")

    # Guardar
    tfidf_df = pd.DataFrame(
        X.toarray(),
        index=nombres,
        columns=vectorizer.get_feature_names_out()
    )
    tfidf_df.to_csv(os.path.join(output_path, "tf_idf_matrix.csv"), encoding="utf-8-sig")
    print("TF-IDF guardado")

    # Top 20 términos globales (verificación rápida)
    print("\nTop 20 términos:")
    top = tfidf_df.sum(axis=0).nlargest(50)
    for term, score in top.items():
        print(f"  {score:.3f}  {term}")

    # Top 10 bigramas
    bigramas = [c for c in tfidf_df.columns if ' ' in c]
    if bigramas:
        print(f"\nTop 10 bigramas:")
        bi_top = tfidf_df[bigramas].sum(axis=0).nlargest(20)
        for term, score in bi_top.items():
            print(f"  {score:.3f}  {term}")


if __name__ == "__main__":
    run()