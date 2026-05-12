import os
import pandas as pd
import math
import workspace
from bagofwords import local_stopwords
from nltk.corpus import stopwords

stop_es = set(stopwords.words('spanish'))
todas_stopwords = list(stop_es | local_stopwords)

def process_tf_idf(bow_df):
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

def run():
    workspace.set_workspace_path(os.path.dirname(os.path.abspath(__file__)))

    bow_c_df = pd.read_csv(os.path.join(workspace.get_output_path(), "bow_matrix_count.csv"), index_col=0)
    tfidf_df = process_tf_idf(bow_c_df)
    tfidf_df.to_csv(os.path.join(workspace.get_output_path(), "tf_idf_matrix.csv"), encoding="utf-8-sig")
    print("se ha generado tf_idf_matrix.csv")

if __name__ == "__main__":
    run()
