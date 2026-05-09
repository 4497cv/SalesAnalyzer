import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import workspace
from bagofwords import local_stopwords
import math

# === STOPWORDS ===
stop_es = set(stopwords.words('spanish'))

# Preservar solo negaciones y cuantificadores con valor semántico real
preservar = {'nunca', 'nada', 'sin', 'menos', 'poco'}
stop_es = stop_es - preservar

todas_stopwords = list(stop_es | local_stopwords)

# === EXTRAER TEXTO POR CONVERSACIÓN ===
def _extract_text(line):
    parts = line.split(":", 1)
    return parts[1].strip() if len(parts) > 1 else ""

def process_tf_idf(bow_df) -> None:
    """
    Generates TF-IDF matrix from a BoW DataFrame and stores it in output/tf_idf_matrix.csv.

    Parameters:
        bow_df: pandas DataFrame (count BoW)

    Return:
        None
    """
    idf = {}
    tfidf_matrix = []
    N = bow_df.shape[0]
    df = (bow_df > 0).sum(axis=0)

    for word in bow_df.columns:
        idf[word] = math.log(N / (1 + df[word]))

    for _, row in bow_df.iterrows():
        total_words = row.sum()
        tfidf_row = []
        for word in bow_df.columns:
            tf = row[word] / total_words if total_words > 0 else 0
            tfidf_row.append(tf * idf[word])
        tfidf_matrix.append(tfidf_row)

    tfidf_df = pd.DataFrame(tfidf_matrix, index=bow_df.index, columns=bow_df.columns)
    return tfidf_df

def run(custom=1):
    workspace.set_workspace_path(os.path.dirname(os.path.abspath(__file__)))
    
    print("Running Custom TF-IDF")
    # calcular matriz TF-IDF
    bow_c_df = pd.read_csv(os.path.join(workspace.get_output_path(), "bow_matrix_count.csv"), index_col=0)
    tfidf_df = process_tf_idf(bow_c_df)
    tfidf_df.to_csv(os.path.join(workspace.get_output_path(), "tf_idf_matrix.csv"), encoding="utf-8-sig")

if __name__ == "__main__":
    run()