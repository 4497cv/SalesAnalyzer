import os
import sys
import json
import pandas as pd
import workspace

sys.stdout.reconfigure(encoding="utf-8")

PRIORITY_TERMS = {
    "factura", "facturar", "pago", "cotización", "paquete",
    "facturación", "facturame", "pedido", "órden", "existencia", "cotizas", "cotizar",
}

def load_tfidf():
    tf_idf_path = os.path.join(workspace.get_output_path(), "tf_idf_matrix.csv")
    df_tf_idf = pd.read_csv(tf_idf_path, index_col=0, encoding="utf-8-sig")
    return df_tf_idf

def global_ranking(tfidf_df):
    global_score = tfidf_df.sum(axis=0).rename("global_score")
    return global_score

def doc_frequency(tfidf_df):
    doc_freq = (tfidf_df > 0).sum(axis=0).rename("doc_freq")
    return doc_freq

def build_dictionary(global_scores, doc_freq, total_docs):
    base = pd.DataFrame({
        "global_score": global_scores,
        "doc_freq":     doc_freq,
    }).reset_index().rename(columns={"index": "term"})

    base["doc_freq_pct"] = (base["doc_freq"] / total_docs * 100).round(2)
    base["is_bigram"]    = base["term"].str.contains(r" ")

    result = base.sort_values("global_score", ascending=False).reset_index(drop=True)
    result["rank"] = result.index + 1

    return result[["rank", "term", "global_score", "doc_freq", "doc_freq_pct", "is_bigram"]]

def run():
    tfidf_df = load_tfidf()
    global_scores = global_ranking(tfidf_df)
    doc_freq = doc_frequency(tfidf_df)

    dictionary_df = build_dictionary(global_scores, doc_freq, total_docs=len(tfidf_df))

    boost = dictionary_df["global_score"].max() * 10
    mask  = dictionary_df["term"].isin(PRIORITY_TERMS)
    dictionary_df.loc[mask, "global_score"] += boost

    dictionary_df = dictionary_df.sort_values("global_score", ascending=False).reset_index(drop=True)
    dictionary_df["rank"] = dictionary_df.index + 1

    csv_path  = os.path.join(workspace.get_output_path(), "domain_dictionary.csv")
    json_path = os.path.join(workspace.get_output_path(), "domain_dictionary.json")

    dictionary_df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    records = dictionary_df.to_dict(orient="records")
    with open(json_path, "w", encoding="utf-8-sig") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print("se ha generado el archivo %s" % csv_path)
    print("se ha generado el archivo %s" % json_path)
