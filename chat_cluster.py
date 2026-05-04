import os
import sys
import glob
import pandas

sys.stdout.reconfigure(encoding="utf-8")


def load_domain_dict():
    csv_path = os.path.join(os.path.dirname(__file__), "output", "domain_dictionary.csv")
    df = pandas.read_csv(csv_path, encoding="utf-8-sig")
    return df

SELLERS = {"Comercios Unidos", "Permagraf"}

def cluster_chat(filename, term_weights):
    topic_scores = {}
    matched_terms = {}  # term -> topic_label (deduplicated)

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" not in line:
                continue
            _, message = line.split(":", 1)

            words = message.split()
            unigrams = words
            bigrams  = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]

            for term in unigrams+bigrams:
                if term in term_weights:
                    topic, score = term_weights[term]
                    topic_scores[topic] = topic_scores.get(topic, 0) + score
                    matched_terms[term] = topic

    return topic_scores, matched_terms


def run():
    corpus_dir = os.path.join(os.path.dirname(__file__), "corpus")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    df_domain = load_domain_dict()
    term_weights = {
        row.term: (row.topic_label, row.global_score)
        for row in df_domain.itertuples()
        if pandas.notna(row.topic_label)
    }

    rows = []
    all_matched = []
    for txt_file in glob.glob(os.path.join(corpus_dir, "**", "*.txt"), recursive=True):
        if txt_file.endswith("_processed.txt"):
            print(f"Procesando: {txt_file}")
            topic_scores, matched_terms = cluster_chat(txt_file, term_weights)
            row = {"chat": os.path.relpath(txt_file, corpus_dir)}
            row.update(topic_scores)
            rows.append(row)
            all_matched.append(matched_terms)

    result_df = pandas.DataFrame(rows).fillna(0)
    topic_cols = [c for c in result_df.columns if c != "chat"]
    result_df[topic_cols] = result_df[topic_cols].astype(int)

    has_match = result_df[topic_cols].sum(axis=1) > 0
    result_df["topic_cluster"] = None
    result_df.loc[has_match, "topic_cluster"] = result_df.loc[has_match, topic_cols].idxmax(axis=1)

    result_df["matched_terms"] = [
        "; ".join(f"{t}({lbl})" for t, lbl in sorted(m.items())) if m else ""
        for m in all_matched
    ]

    out_path = os.path.join(output_dir, "topic_label_chat_cluster.csv")
    result_df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"Guardado: {out_path}")
    print("\nDistribución de clusters:")
    print(result_df["topic_cluster"].value_counts(dropna=False).to_string())



if __name__ == "__main__":
    run()