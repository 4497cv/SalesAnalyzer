import os
import sys
import pandas as pd
from collections import defaultdict
from pysentimiento import create_analyzer
import preprocess
import workspace

def predict_messages(messages, analyzer):
    results = []
    for author, text in messages:
        pred = analyzer.predict(text)
        probas = pred.probas
        score = probas.get("POS", 0.0) - probas.get("NEG", 0.0)
        results.append({
            "author": author,
            "text": text,
            "label": pred.output,
            "pos": round(probas.get("POS", 0.0), 4),
            "neu": round(probas.get("NEU", 0.0), 4),
            "neg": round(probas.get("NEG", 0.0), 4),
            "score": round(score, 4),
        })
    return results


def session_metrics(client, date, preds):
    n = len(preds)
    if n == 0:
        return {}

    counts = {"POS": 0, "NEU": 0, "NEG": 0}
    sum_pos = 0.0
    sum_neu = 0.0
    sum_neg = 0.0
    sum_score = 0.0

    for p in preds:
        counts[p["label"]] += 1
        sum_pos += p["pos"]
        sum_neu += p["neu"]
        sum_neg += p["neg"]
        sum_score += p["score"]

    dominant = max(counts, key=counts.get)

    return {
        "client": client,
        "session": date,
        "total_messages": n,
        "pos_count": counts["POS"],
        "neu_count": counts["NEU"],
        "neg_count": counts["NEG"],
        "pos_pct": round(counts["POS"] / n * 100, 1),
        "neu_pct": round(counts["NEU"] / n * 100, 1),
        "neg_pct": round(counts["NEG"] / n * 100, 1),
        "avg_pos": round(sum_pos / n, 4),
        "avg_neu": round(sum_neu / n, 4),
        "avg_neg": round(sum_neg / n, 4),
        "sentiment_score": round(sum_score / n, 4),
        "dominant": dominant,
    }


def author_metrics(all_message_rows):
    by_author = defaultdict(list)
    for row in all_message_rows:
        by_author[row["author"]].append(row)

    rows = []
    for author, preds in sorted(by_author.items()):
        n = len(preds)
        counts = {"POS": 0, "NEU": 0, "NEG": 0}
        sum_score = 0.0
        for p in preds:
            counts[p["label"]] += 1
            sum_score += p["score"]
        dominant = max(counts, key=counts.get)
        rows.append({
            "author": author,
            "total_messages": n,
            "pos_count": counts["POS"],
            "neu_count": counts["NEU"],
            "neg_count": counts["NEG"],
            "pos_pct": round(counts["POS"] / n * 100, 1),
            "neu_pct": round(counts["NEU"] / n * 100, 1),
            "neg_pct": round(counts["NEG"] / n * 100, 1),
            "avg_score": round(sum_score / n, 4),
            "dominant": dominant,
        })

    return pd.DataFrame(rows).sort_values("avg_score", ascending=False)


def run():
    print("Cargando modelo de sentimiento")
    analyzer = create_analyzer(task="sentiment", lang="es")

    session_rows = []
    message_rows = []

    # obtener todas las sesiones del corpus
    corpus_dir = workspace.get_corpus_path()
    sessions = []
    for client in sorted(os.listdir(corpus_dir)):
        client_path = os.path.join(corpus_dir, client)
        if not os.path.isdir(client_path):
            continue
        for session in sorted(os.listdir(client_path)):
            session_path = os.path.join(client_path, session)
            if not os.path.isdir(session_path):
                continue
            fp = os.path.join(session_path, "mensajes_processed.txt")
            if os.path.exists(fp):
                sessions.append((client, session, fp))

    print(f"Sesiones encontradas: {len(sessions)}\n")

    for idx, (client, date, filepath) in enumerate(sessions, 1):
        print(f"[{idx}/{len(sessions)}] {client}/{date}")

        # cargar mensajes de la sesion
        messages = preprocess.load_messages(filepath)

        if not messages:
            print("  no tiene mensajes, omitida.")
            continue

        preds = predict_messages(messages, analyzer)

        # filas a nivel mensaje
        for pred in preds:
            message_rows.append({
                "client": client,
                "session": date,
                "author": pred["author"],
                "text": pred["text"],
                "label": pred["label"],
                "pos": pred["pos"],
                "neu": pred["neu"],
                "neg": pred["neg"],
                "score": pred["score"],
            })

        # metricas de la sesion
        metrics = session_metrics(client, date, preds)
        session_rows.append(metrics)

        print(f"  score={metrics['sentiment_score']:+.3f}  POS={metrics['pos_pct']}%  NEG={metrics['neg_pct']}%")

    # guardar resultados
    session_df = pd.DataFrame(session_rows)
    message_df = pd.DataFrame(message_rows)
    author_df = author_metrics(message_rows)

    session_path = os.path.join(workspace.get_output_path(), "sentiment_by_session.csv")
    author_path = os.path.join(workspace.get_output_path(), "sentiment_by_author.csv")
    msg_path = os.path.join(workspace.get_output_path(), "sentiment_messages.csv")

    session_df.to_csv(session_path, index=False, encoding="utf-8-sig")
    author_df.to_csv(author_path, index=False, encoding="utf-8-sig")
    message_df.to_csv(msg_path, index=False, encoding="utf-8-sig")

    print(f"\nGuardado:")
    print(f"{session_path}")
    print(f"{author_path}")
    print(f"{msg_path}")
