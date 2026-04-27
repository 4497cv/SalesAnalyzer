"""
tone_evolution.py
Analiza como evoluciona el TONO de cada conversacion a lo largo del tiempo.

Diferencia con sentiment_analysis.py:
  - Usa el analizador de EMOCIONES de pysentimiento (joy, sadness, anger,
    fear, surprise, disgust, others) en lugar de solo POS/NEU/NEG.
  - El foco es el CAMBIO: como transiciona el tono mensaje a mensaje.
  - Calcula metricas de arco narrativo, volatilidad, apertura vs cierre,
    divergencia entre hablantes y matriz de transicion de emociones.

Metricas por sesion:
  opening_emotion     emocion dominante en el primer tercio
  closing_emotion     emocion dominante en el ultimo tercio
  arc_direction       'ascendente' | 'descendente' | 'estable' | 'en_v' | 'en_arco'
  dominant_emotion    emocion mas frecuente en toda la sesion
  volatility          desviacion estandar del score de valencia
  speaker_divergence  diferencia promedio de score entre los dos hablantes
  peak_pos_msg        mensaje con el maximo score positivo
  peak_neg_msg        mensaje con el maximo score negativo

Salidas en output/:
  tone_messages.csv      una fila por mensaje con emocion, scores y posicion
  tone_sessions.csv      metricas agregadas por sesion
  tone_transitions.csv   matriz de transiciones de emocion (A -> B)
  tone_evolution.json    trayectorias completas para visualizacion externa

Instalacion:
  pip install pysentimiento
"""

import os
import sys
import json
import warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AI.nlp_utils import mock_datasets, iter_sessions, load_messages
mock_datasets()

import numpy as np
import pandas as pd
from collections import defaultdict

import workspace
from preprocess import normalize_for_sentiment

# ── emociones y su valencia ───────────────────────────────────────────────────
# Valencia: cuanto contribuye cada emocion al tono positivo/negativo [-1, 1]
EMOTION_VALENCE = {
    "joy":      +1.0,
    "surprise": +0.3,
    "others":    0.0,
    "fear":     -0.5,
    "sadness":  -0.7,
    "disgust":  -0.8,
    "anger":    -1.0,
}

EMOTIONS = list(EMOTION_VALENCE.keys())


# ── carga de modelos ──────────────────────────────────────────────────────────

def load_analyzers():
    try:
        from pysentimiento import create_analyzer
    except Exception as e:
        print(f"ERROR al importar pysentimiento: {e}")
        print("  pip install pysentimiento transformers torch")
        sys.exit(1)

    print("Cargando analizador de emociones…")
    try:
        emotion_analyzer = create_analyzer(task="emotion", lang="es")
    except Exception as e:
        print(f"ERROR al cargar modelo de emociones: {e}")
        sys.exit(1)

    print("Modelos listos.\n")
    return emotion_analyzer


# ── inferencia ────────────────────────────────────────────────────────────────

def analyze_message(text: str, emotion_analyzer) -> dict:
    """
    Retorna emocion dominante, todas las probabilidades y score de valencia
    para un mensaje.
    """
    pred   = emotion_analyzer.predict(text)
    probas = pred.probas

    emotion = pred.output.lower()
    valence = sum(EMOTION_VALENCE.get(e, 0.0) * p for e, p in probas.items())

    return {
        "emotion": emotion,
        "valence": round(valence, 4),
        **{f"p_{e}": round(probas.get(e, 0.0), 4) for e in EMOTIONS},
    }


# ── metricas de arco ──────────────────────────────────────────────────────────

def _smooth(values: list[float], window: int = 3) -> list[float]:
    """Media movil simple para suavizar la trayectoria."""
    if len(values) < window:
        return values
    result = []
    for i in range(len(values)):
        lo = max(0, i - window // 2)
        hi = min(len(values), i + window // 2 + 1)
        result.append(round(sum(values[lo:hi]) / (hi - lo), 4))
    return result


def classify_arc(valences: list[float]) -> str:
    """
    Clasifica la forma del arco emocional de la sesion.
      ascendente  — el tono mejora hacia el final
      descendente — el tono empeora hacia el final
      en_v        — cae a la mitad y se recupera
      en_arco     — sube a la mitad y cae
      estable     — sin cambio significativo
    """
    if len(valences) < 4:
        return "estable"

    n    = len(valences)
    mid  = n // 2
    avg_first  = sum(valences[:mid]) / mid
    avg_second = sum(valences[mid:]) / (n - mid)
    avg_middle = sum(valences[n//4: 3*n//4]) / (n // 2)

    delta = avg_second - avg_first
    THRESHOLD = 0.08

    if abs(delta) < THRESHOLD:
        return "estable"
    if delta > THRESHOLD:
        # sube al final — pero si el medio fue mas alto que ambos extremos es arco
        if avg_middle < min(avg_first, avg_second) - THRESHOLD:
            return "en_v"
        return "ascendente"
    else:
        if avg_middle > max(avg_first, avg_second) + THRESHOLD:
            return "en_arco"
        return "descendente"


def dominant_in_range(emotions: list[str]) -> str:
    if not emotions:
        return "others"
    counts = defaultdict(int)
    for e in emotions:
        counts[e] += 1
    return max(counts, key=counts.get)


# ── metricas de hablantes ─────────────────────────────────────────────────────

def speaker_divergence(preds: list[dict]) -> float:
    """
    Diferencia promedio de valencia entre los dos hablantes principales.
    0 = convergen, 1+ = divergen.
    """
    by_speaker = defaultdict(list)
    for p in preds:
        by_speaker[p["author"]].append(p["valence"])

    speakers = list(by_speaker.keys())
    if len(speakers) < 2:
        return 0.0

    avgs = [sum(v) / len(v) for v in by_speaker.values()]
    return round(abs(avgs[0] - avgs[1]), 4)


# ── metricas por sesion ───────────────────────────────────────────────────────

def session_metrics(client: str, date: str, preds: list[dict]) -> dict:
    n = len(preds)
    if n == 0:
        return {}

    valences = [p["valence"] for p in preds]
    emotions = [p["emotion"] for p in preds]

    third = max(1, n // 3)
    opening_emotions = emotions[:third]
    closing_emotions = emotions[n - third:]

    # pico positivo y negativo (indices)
    peak_pos_idx = int(np.argmax(valences))
    peak_neg_idx = int(np.argmin(valences))

    smooth = _smooth(valences)

    return {
        "client":             client,
        "session":            date,
        "total_messages":     n,
        "dominant_emotion":   dominant_in_range(emotions),
        "opening_emotion":    dominant_in_range(opening_emotions),
        "closing_emotion":    dominant_in_range(closing_emotions),
        "arc_direction":      classify_arc(valences),
        "avg_valence":        round(sum(valences) / n, 4),
        "volatility":         round(float(np.std(valences)), 4),
        "speaker_divergence": speaker_divergence(preds),
        "peak_pos_valence":   round(valences[peak_pos_idx], 4),
        "peak_pos_msg":       preds[peak_pos_idx]["text"][:80],
        "peak_neg_valence":   round(valences[peak_neg_idx], 4),
        "peak_neg_msg":       preds[peak_neg_idx]["text"][:80],
        # distribucion de emociones
        **{f"pct_{e}": round(emotions.count(e) / n * 100, 1) for e in EMOTIONS},
        # trayectoria suavizada (para JSON)
        "_trajectory":        smooth,
    }


# ── matriz de transiciones ────────────────────────────────────────────────────

def build_transition_matrix(all_preds: list[dict]) -> pd.DataFrame:
    """
    Cuenta cuantas veces la emocion E1 es seguida por la emocion E2
    dentro de la misma sesion.
    """
    counts = defaultdict(lambda: defaultdict(int))

    current_session = None
    prev_emotion    = None

    for p in all_preds:
        session_key = f"{p['client']}/{p['session']}"
        if session_key != current_session:
            current_session = session_key
            prev_emotion    = None

        if prev_emotion is not None:
            counts[prev_emotion][p["emotion"]] += 1
        prev_emotion = p["emotion"]

    df = pd.DataFrame(counts).fillna(0).astype(int)
    # asegurar que todas las emociones aparecen como filas y columnas
    for e in EMOTIONS:
        if e not in df.index:
            df.loc[e] = 0
        if e not in df.columns:
            df[e] = 0
    return df.loc[EMOTIONS, EMOTIONS]


# ── resumen en consola ────────────────────────────────────────────────────────

def print_summary(session_df: pd.DataFrame, trans_df: pd.DataFrame) -> None:
    print(f"\n{'='*65}")
    print(f"EVOLUCION DE TONO  —  {len(session_df)} sesiones")
    print(f"{'='*65}")

    print("\nDistribucion de arco emocional:")
    arc_counts = session_df["arc_direction"].value_counts()
    for arc, count in arc_counts.items():
        bar = "█" * count
        print(f"  {arc:<15} {count:>4}  {bar}")

    print("\nEmocion de apertura mas frecuente:")
    for emotion, count in session_df["opening_emotion"].value_counts().head(4).items():
        print(f"  {emotion:<15} {count}")

    print("\nEmocion de cierre mas frecuente:")
    for emotion, count in session_df["closing_emotion"].value_counts().head(4).items():
        print(f"  {emotion:<15} {count}")

    print("\nVolatilidad promedio por cliente:")
    vol = session_df.groupby("client")["volatility"].mean().sort_values(ascending=False)
    for client, v in vol.items():
        bar = "█" * int(v * 20)
        print(f"  {client:<40} {v:.3f}  {bar}")

    print("\nSesiones con mayor volatilidad (tono inestable):")
    top_vol = session_df.nlargest(5, "volatility")[
        ["client", "session", "volatility", "arc_direction", "dominant_emotion"]
    ]
    print(top_vol.to_string(index=False))

    print("\nSesiones con arco ascendente (conversacion que mejora):")
    asc = session_df[session_df["arc_direction"] == "ascendente"][
        ["client", "session", "avg_valence", "opening_emotion", "closing_emotion"]
    ].head(8)
    print(asc.to_string(index=False) if not asc.empty else "  (ninguna)")

    print("\nTransiciones de emocion mas frecuentes:")
    flat = trans_df.stack().reset_index()
    flat.columns = ["de", "a", "count"]
    flat = flat[flat["de"] != flat["a"]].nlargest(10, "count")
    for _, row in flat.iterrows():
        print(f"  {row['de']:<12} → {row['a']:<12}  {int(row['count'])}")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    workspace.set_workspace_path(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    corpus_dir = workspace.get_corpus_path()
    output_dir = workspace.get_output_path()

    emotion_analyzer = load_analyzers()

    all_message_rows = []
    session_rows     = []
    trajectory_data  = {}

    sessions = list(iter_sessions(corpus_dir))
    print(f"Sesiones encontradas: {len(sessions)}\n")

    for idx, (client, date, filepath) in enumerate(sessions, 1):
        print(f"[{idx}/{len(sessions)}] {client}/{date}", end=" … ", flush=True)

        messages = load_messages(filepath, normalize_for_sentiment)
        if not messages:
            print("sin mensajes, omitida.")
            continue

        preds = []
        for author, text in messages:
            result = analyze_message(text, emotion_analyzer)
            preds.append({"author": author, "text": text, **result})

        # filas a nivel mensaje
        for pos, pred in enumerate(preds):
            all_message_rows.append({
                "client":       client,
                "session":      date,
                "position":     pos,
                "position_pct": round(pos / max(len(preds) - 1, 1) * 100, 1),
                **pred,
            })

        metrics = session_metrics(client, date, preds)
        traj    = metrics.pop("_trajectory")
        session_rows.append(metrics)
        trajectory_data[f"{client}/{date}"] = traj

        print(f"arco={metrics['arc_direction']}  "
              f"dominante={metrics['dominant_emotion']}  "
              f"volatilidad={metrics['volatility']:.3f}")

    session_df = pd.DataFrame(session_rows)
    message_df = pd.DataFrame(all_message_rows)
    trans_df   = build_transition_matrix(all_message_rows)

    # guardar
    session_path = os.path.join(output_dir, "tone_sessions.csv")
    msg_path     = os.path.join(output_dir, "tone_messages.csv")
    trans_path   = os.path.join(output_dir, "tone_transitions.csv")
    traj_path    = os.path.join(output_dir, "tone_evolution.json")

    session_df.to_csv(session_path, index=False, encoding="utf-8-sig")
    message_df.to_csv(msg_path,     index=False, encoding="utf-8-sig")
    trans_df.to_csv(trans_path,     encoding="utf-8-sig")
    with open(traj_path, "w", encoding="utf-8-sig") as f:
        json.dump(trajectory_data, f, ensure_ascii=False, indent=2)

    print_summary(session_df, trans_df)

    print(f"\nGuardado:")
    print(f"  {session_path}")
    print(f"  {msg_path}")
    print(f"  {trans_path}")
    print(f"  {traj_path}")


if __name__ == "__main__":
    main()
