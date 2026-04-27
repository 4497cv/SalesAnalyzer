"""
sentiment_analysis.py
Analisis de sentimiento por conversacion sobre el corpus de ventas.

Usa pysentimiento (robertuito-sentiment-analysis), modelo RoBERTa entrenado
sobre texto en espanol de redes sociales — bien adaptado al lenguaje informal
de WhatsApp.

Preprocesamiento: reutiliza las funciones de preprocess.py
  - normalize_for_sentiment()  pipeline completo typos+puntuacion+bigramas+limpieza
  - extract_author_text()      parsea lineas 'author:text'

Metricas por sesion (conversacion):
  - conteo y % de mensajes POS / NEU / NEG
  - sentiment_score compuesto en [-1, 1]  (avg_pos - avg_neg)
  - sentimiento dominante
  - desglose por autor (vendedor vs cliente)
  - trayectoria: como evoluciona el sentimiento a lo largo de la conversacion

Salidas en output/:
  sentiment_by_session.csv   una fila por sesion, todas las metricas
  sentiment_by_author.csv    metricas agregadas por autor sobre todo el corpus
  sentiment_messages.csv     una fila por mensaje (nivel mas granular)
  sentiment_trajectory.json  array de scores por posicion relativa en la sesion

Instalacion:
  pip install pysentimiento
"""

import os
import sys
import json
import warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AI.nlp_utils import mock_datasets, iter_sessions as _iter_sessions, load_messages as _load_messages
mock_datasets()

import pandas as pd
from collections import defaultdict

import workspace
from preprocess import extract_author_text, normalize_for_sentiment

# ── carga del modelo ──────────────────────────────────────────────────────────

def load_analyzer():
    try:
        from pysentimiento import create_analyzer
    except Exception as e:
        print(f"ERROR al importar pysentimiento: {e}")
        print("Verifica: pip install pysentimiento transformers torch")
        sys.exit(1)

    print("Cargando modelo de sentimiento (robertuito)…")
    try:
        analyzer = create_analyzer(task="sentiment", lang="es")
    except Exception as e:
        print(f"ERROR al cargar el modelo: {e}")
        sys.exit(1)

    print("Modelo listo.\n")
    return analyzer


# ── lectura del corpus ────────────────────────────────────────────────────────

def iter_sessions(corpus_dir: str):
    return _iter_sessions(corpus_dir)


def load_messages(filepath: str) -> list[tuple[str, str]]:
    return _load_messages(filepath, normalize_for_sentiment)


# ── inferencia de sentimiento ─────────────────────────────────────────────────

LABEL_MAP = {"POS": 1, "NEU": 0, "NEG": -1}

def predict_messages(messages: list[tuple[str, str]], analyzer) -> list[dict]:
    """
    Corre el modelo sobre cada mensaje individualmente.
    (El batch de pysentimiento requiere datasets/pyarrow que puede estar bloqueado
    por Windows Application Control; predict() con string individual no lo necesita.)
    Retorna lista de dicts con author, text, label, pos, neu, neg, score.
    """
    results = []
    for author, text in messages:
        pred   = analyzer.predict(text)
        probas = pred.probas
        score  = probas.get("POS", 0.0) - probas.get("NEG", 0.0)
        results.append({
            "author": author,
            "text":   text,
            "label":  pred.output,
            "pos":    round(probas.get("POS", 0.0), 4),
            "neu":    round(probas.get("NEU", 0.0), 4),
            "neg":    round(probas.get("NEG", 0.0), 4),
            "score":  round(score, 4),
        })
    return results


# ── metricas por sesion ───────────────────────────────────────────────────────

def session_metrics(client: str, date: str, preds: list[dict]) -> dict:
    """Agrega las predicciones de una sesion en una fila de metricas."""
    n = len(preds)
    if n == 0:
        return {}

    counts = {"POS": 0, "NEU": 0, "NEG": 0}
    sum_pos = sum_neu = sum_neg = sum_score = 0.0

    for p in preds:
        counts[p["label"]] += 1
        sum_pos   += p["pos"]
        sum_neu   += p["neu"]
        sum_neg   += p["neg"]
        sum_score += p["score"]

    dominant = max(counts, key=counts.get)

    # trayectoria: score por posicion relativa (10 segmentos)
    trajectory = _trajectory(preds, segments=10)

    return {
        "client":           client,
        "session":          date,
        "total_messages":   n,
        "pos_count":        counts["POS"],
        "neu_count":        counts["NEU"],
        "neg_count":        counts["NEG"],
        "pos_pct":          round(counts["POS"] / n * 100, 1),
        "neu_pct":          round(counts["NEU"] / n * 100, 1),
        "neg_pct":          round(counts["NEG"] / n * 100, 1),
        "avg_pos":          round(sum_pos   / n, 4),
        "avg_neu":          round(sum_neu   / n, 4),
        "avg_neg":          round(sum_neg   / n, 4),
        "sentiment_score":  round(sum_score / n, 4),   # [-1, 1]
        "dominant":         dominant,
        "trajectory":       trajectory,
    }


def _trajectory(preds: list[dict], segments: int = 10) -> list[float]:
    """
    Divide la sesion en `segments` tramos iguales y calcula el score
    promedio de cada tramo. Util para ver si el sentimiento mejora o
    empeora a lo largo de la conversacion.
    """
    n = len(preds)
    if n == 0:
        return []
    size = max(1, n // segments)
    traj = []
    for i in range(0, n, size):
        chunk = preds[i: i + size]
        avg = sum(p["score"] for p in chunk) / len(chunk)
        traj.append(round(avg, 4))
    return traj


# ── metricas por autor ────────────────────────────────────────────────────────

def author_metrics(all_message_rows: list[dict]) -> pd.DataFrame:
    """
    Agrupa todas las predicciones por autor y calcula sus metricas globales.
    Permite distinguir el patron de sentimiento del vendedor vs. cada cliente.
    """
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
            "author":          author,
            "total_messages":  n,
            "pos_count":       counts["POS"],
            "neu_count":       counts["NEU"],
            "neg_count":       counts["NEG"],
            "pos_pct":         round(counts["POS"] / n * 100, 1),
            "neu_pct":         round(counts["NEU"] / n * 100, 1),
            "neg_pct":         round(counts["NEG"] / n * 100, 1),
            "avg_score":       round(sum_score / n, 4),
            "dominant":        dominant,
        })

    return pd.DataFrame(rows).sort_values("avg_score", ascending=False)


# ── impresion de resumen ──────────────────────────────────────────────────────

def print_summary(session_df: pd.DataFrame) -> None:
    print(f"\n{'='*65}")
    print(f"RESUMEN DE SENTIMIENTO  —  {len(session_df)} sesiones")
    print(f"{'='*65}")

    global_score = session_df["sentiment_score"].mean()
    print(f"\nScore global del corpus:  {global_score:+.4f}")

    dist = session_df["dominant"].value_counts()
    total = len(session_df)
    print("\nDistribucion de sesiones por sentimiento dominante:")
    for label in ("POS", "NEU", "NEG"):
        count = dist.get(label, 0)
        bar = "█" * int(count / total * 40)
        print(f"  {label}  {count:>4} sesiones  {bar}")

    print("\nTop 10 sesiones mas positivas:")
    top_pos = session_df.nlargest(10, "sentiment_score")[
        ["client", "session", "sentiment_score", "pos_pct", "neg_pct", "total_messages"]
    ]
    print(top_pos.to_string(index=False))

    print("\nTop 10 sesiones mas negativas:")
    top_neg = session_df.nsmallest(10, "sentiment_score")[
        ["client", "session", "sentiment_score", "pos_pct", "neg_pct", "total_messages"]
    ]
    print(top_neg.to_string(index=False))

    print("\nScore promedio por cliente:")
    by_client = (
        session_df.groupby("client")["sentiment_score"]
        .mean()
        .sort_values(ascending=False)
    )
    for client, score in by_client.items():
        bar = "█" * int((score + 1) / 2 * 30)
        print(f"  {client:<40} {score:+.4f}  {bar}")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    workspace.set_workspace_path(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    corpus_dir = workspace.get_corpus_path()
    output_dir = workspace.get_output_path()

    analyzer = load_analyzer()

    session_rows    = []
    message_rows    = []
    trajectory_data = {}

    sessions = list(iter_sessions(corpus_dir))
    print(f"Sesiones encontradas: {len(sessions)}\n")

    for idx, (client, date, filepath) in enumerate(sessions, 1):
        print(f"[{idx}/{len(sessions)}] {client}/{date}", end=" … ", flush=True)

        messages = load_messages(filepath)
        if not messages:
            print("sin mensajes, omitida.")
            continue

        preds = predict_messages(messages, analyzer)

        # filas a nivel mensaje
        for pred in preds:
            message_rows.append({
                "client":  client,
                "session": date,
                **pred,
            })

        # metricas de sesion
        metrics = session_metrics(client, date, preds)
        traj    = metrics.pop("trajectory")
        session_rows.append(metrics)
        trajectory_data[f"{client}/{date}"] = traj

        print(f"score={metrics['sentiment_score']:+.3f}  "
              f"POS={metrics['pos_pct']}%  NEG={metrics['neg_pct']}%")

    # DataFrames
    session_df = pd.DataFrame(session_rows)
    message_df = pd.DataFrame(message_rows)
    author_df  = author_metrics(message_rows)

    # guardar CSVs
    session_path = os.path.join(output_dir, "sentiment_by_session.csv")
    author_path  = os.path.join(output_dir, "sentiment_by_author.csv")
    msg_path     = os.path.join(output_dir, "sentiment_messages.csv")
    traj_path    = os.path.join(output_dir, "sentiment_trajectory.json")

    session_df.to_csv(session_path, index=False, encoding="utf-8-sig")
    author_df.to_csv(author_path,   index=False, encoding="utf-8-sig")
    message_df.to_csv(msg_path,     index=False, encoding="utf-8-sig")
    with open(traj_path, "w", encoding="utf-8-sig") as f:
        json.dump(trajectory_data, f, ensure_ascii=False, indent=2)

    print_summary(session_df)

    print(f"\nGuardado:")
    print(f"  {session_path}")
    print(f"  {author_path}")
    print(f"  {msg_path}")
    print(f"  {traj_path}")


if __name__ == "__main__":
    main()
