"""
domain_dictionary.py
Reads the TF-IDF matrix produced by test.py (or bagofwords.py) and applies three
complementary ML techniques to surface domain vocabulary:

  1. Global ranking        — sum-of-TF-IDF per term → overall importance
  2. K-Means clustering    — groups sessions, then extracts top terms per cluster
  3. LDA topic modelling   — discovers latent topics, tags each term with its
                             dominant topic and semantic label

Outputs:
  output/domain_dictionary.csv   — one row per term, all annotations
  output/domain_dictionary.json  — same data, easier to embed in other tools
"""

import os
import sys
import json
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.preprocessing import normalize

# ── path setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import workspace

# ── constants ────────────────────────────────────────────────────────────────
N_CLUSTERS   = 5    # one per client in the corpus
N_TOPICS     = 8    # LDA topics
TOP_PER_CLUSTER = 30
TOP_PER_TOPIC   = 25
MIN_GLOBAL_SCORE = 0.0  # keep all terms; filter downstream if needed

# Human-readable labels assigned after inspecting the top words of each topic.
# They are placeholders — re-run and update after you see the actual terms.
TOPIC_LABELS = {
    0: "producto_consulta",
    1: "precio_cotizacion",
    2: "pedido_entrega",
    3: "pago_facturacion",
    4: "soporte_problema",
    5: "confirmacion_seguimiento",
    6: "promocion_oferta",
    7: "logistica_envio",
}


# ── helpers ──────────────────────────────────────────────────────────────────

def load_tfidf(output_path: str) -> pd.DataFrame:
    path = os.path.join(output_path, "tf_idf_matrix.csv")
    if not os.path.exists(path):
        print(f"ERROR: tf_idf_matrix.csv not found at {path}")
        print("Run test.py (or bagofwords.py) first to generate it.")
        sys.exit(1)

    df = pd.read_csv(path, index_col=0, encoding="utf-8-sig")
    print(f"TF-IDF matrix loaded: {df.shape[0]} sessions × {df.shape[1]} terms")
    return df


def global_ranking(tfidf_df: pd.DataFrame) -> pd.Series:
    """Sum of TF-IDF scores across all sessions — proxy for global importance."""
    return tfidf_df.sum(axis=0).rename("global_score")


def doc_frequency(tfidf_df: pd.DataFrame) -> pd.Series:
    """Number of sessions where the term appears (score > 0)."""
    return (tfidf_df > 0).sum(axis=0).rename("doc_freq")


def run_kmeans(tfidf_df: pd.DataFrame, n_clusters: int) -> tuple[np.ndarray, pd.DataFrame]:
    """
    K-Means on the session vectors.
    Returns (labels array, cluster_term_df).
    cluster_term_df has columns: term, cluster_id, cluster_rank (1=most important).
    """
    X = normalize(tfidf_df.values, norm="l2")
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(X)

    rows = []
    centers = km.cluster_centers_
    for cid in range(n_clusters):
        # top terms by centroid weight
        top_idx = np.argsort(centers[cid])[::-1][:TOP_PER_CLUSTER]
        for rank, idx in enumerate(top_idx, start=1):
            rows.append({
                "term":         tfidf_df.columns[idx],
                "cluster_id":   cid,
                "cluster_rank": rank,
            })

    return labels, pd.DataFrame(rows)


def run_lda(tfidf_df: pd.DataFrame, n_topics: int) -> tuple[np.ndarray, pd.DataFrame]:
    """
    LDA on the TF-IDF matrix (LDA expects non-negative values, which TF-IDF satisfies).
    Returns (doc-topic matrix, topic_term_df).
    topic_term_df has columns: term, topic_id, topic_label, topic_rank.
    """
    X = tfidf_df.values.astype(float)
    X = np.clip(X, 0, None)   # ensure non-negative

    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=20,
        learning_method="batch",
    )
    doc_topic = lda.fit_transform(X)

    # dominant topic for every term (argmax over topics axis)
    dominant_topic = np.argmax(lda.components_, axis=0)  # shape: (n_features,)

    # rank within dominant topic (position in sorted order for that topic)
    topic_sorted = {tid: np.argsort(lda.components_[tid])[::-1].tolist()
                    for tid in range(n_topics)}

    rows = []
    for idx, term in enumerate(tfidf_df.columns):
        tid = int(dominant_topic[idx])
        rank = topic_sorted[tid].index(idx) + 1
        rows.append({
            "term":        term,
            "topic_id":    tid,
            "topic_label": TOPIC_LABELS.get(tid, f"topic_{tid}"),
            "topic_rank":  rank,
        })

    return doc_topic, pd.DataFrame(rows)


def build_dictionary(
    global_scores: pd.Series,
    doc_freq: pd.Series,
    cluster_df: pd.DataFrame,
    topic_df: pd.DataFrame,
    total_docs: int,
) -> pd.DataFrame:
    """
    Merges all signals into a single domain dictionary DataFrame.
    One row per unique term.
    """
    # base: all terms with their global score and doc frequency
    base = pd.DataFrame({
        "global_score": global_scores,
        "doc_freq":     doc_freq,
    }).reset_index().rename(columns={"index": "term"})

    base["doc_freq_pct"] = (base["doc_freq"] / total_docs * 100).round(2)
    base["is_bigram"]    = base["term"].str.contains(r" ")

    # best cluster assignment (lowest rank = most representative)
    best_cluster = (
        cluster_df.sort_values("cluster_rank")
        .drop_duplicates("term", keep="first")[["term", "cluster_id", "cluster_rank"]]
    )

    # best topic assignment
    best_topic = (
        topic_df.sort_values("topic_rank")
        .drop_duplicates("term", keep="first")[["term", "topic_id", "topic_label", "topic_rank"]]
    )

    result = (
        base
        .merge(best_cluster, on="term", how="left")
        .merge(best_topic,   on="term", how="left")
        .sort_values("global_score", ascending=False)
        .reset_index(drop=True)
    )

    result["rank"] = result.index + 1
    cols = [
        "rank", "term", "global_score", "doc_freq", "doc_freq_pct",
        "is_bigram", "cluster_id", "cluster_rank", "topic_id", "topic_label", "topic_rank",
    ]
    return result[cols]


def print_summary(dictionary_df: pd.DataFrame, n_topics: int) -> None:
    print(f"\n{'='*60}")
    print(f"DOMAIN DICTIONARY  —  {len(dictionary_df)} terms")
    print(f"{'='*60}")

    print("\nTop 30 terms by global TF-IDF score:")
    top30 = dictionary_df.head(30)
    for _, row in top30.iterrows():
        bigram_flag = " [bigram]" if row["is_bigram"] else ""
        print(f"  {row['rank']:>4}. {row['term']:<30} score={row['global_score']:.4f}  "
              f"docs={int(row['doc_freq'])} ({row['doc_freq_pct']:.1f}%)  "
              f"topic={row['topic_label']}{bigram_flag}")

    print(f"\nTop bigrams:")
    bigrams = dictionary_df[dictionary_df["is_bigram"]].head(20)
    for _, row in bigrams.iterrows():
        print(f"  {row['rank']:>4}. {row['term']:<35} score={row['global_score']:.4f}")

    print(f"\nTerms per topic:")
    for tid in range(n_topics):
        label = TOPIC_LABELS.get(tid, f"topic_{tid}")
        terms = dictionary_df[dictionary_df["topic_id"] == tid].head(10)["term"].tolist()
        print(f"  [{tid}] {label}: {', '.join(terms)}")

    print(f"\nTerms per cluster (top 5 each):")
    for cid in sorted(dictionary_df["cluster_id"].dropna().unique()):
        terms = (
            dictionary_df[dictionary_df["cluster_id"] == cid]
            .sort_values("cluster_rank")
            .head(5)["term"]
            .tolist()
        )
        print(f"  Cluster {int(cid)}: {', '.join(terms)}")


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    workspace.set_workspace_path(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    output_path = workspace.get_output_path()

    # 1. load data
    tfidf_df = load_tfidf(output_path)

    # 2. global term ranking
    global_scores = global_ranking(tfidf_df)
    doc_freq      = doc_frequency(tfidf_df)

    # 3. K-Means clustering
    print(f"\nRunning K-Means (k={N_CLUSTERS})…")
    session_labels, cluster_df = run_kmeans(tfidf_df, N_CLUSTERS)

    # 4. LDA topic modelling
    print(f"Running LDA (n_topics={N_TOPICS})…")
    doc_topic, topic_df = run_lda(tfidf_df, N_TOPICS)

    # 5. build unified dictionary
    dictionary_df = build_dictionary(
        global_scores, doc_freq, cluster_df, topic_df, total_docs=len(tfidf_df)
    )

    # 6. save
    csv_path  = os.path.join(output_path, "domain_dictionary.csv")
    json_path = os.path.join(output_path, "domain_dictionary.json")

    dictionary_df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    records = dictionary_df.to_dict(orient="records")
    with open(json_path, "w", encoding="utf-8-sig") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print_summary(dictionary_df, N_TOPICS)

    print(f"\nSaved:")
    print(f"  {csv_path}")
    print(f"  {json_path}")

    # 7. also save per-cluster and per-topic breakdowns for inspection
    cluster_summary_path = os.path.join(output_path, "domain_dict_by_cluster.csv")
    cluster_df.to_csv(cluster_summary_path, index=False, encoding="utf-8-sig")

    topic_summary_path = os.path.join(output_path, "domain_dict_by_topic.csv")
    topic_df.to_csv(topic_summary_path, index=False, encoding="utf-8-sig")

    print(f"  {cluster_summary_path}")
    print(f"  {topic_summary_path}")


if __name__ == "__main__":
    main()
