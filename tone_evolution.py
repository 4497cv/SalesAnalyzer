import os
import sys
import pandas as pd
from pysentimiento import create_analyzer
import preprocess
import workspace

sys.stdout.reconfigure(encoding="utf-8")

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


def analyze_message(text, emotion_analyzer):
    pred = emotion_analyzer.predict(text)
    probas = pred.probas
    emotion = pred.output.lower()
    valence = 0.0
    for e, p in probas.items():
        valence += EMOTION_VALENCE.get(e, 0.0) * p
    result = {"emotion": emotion, "valence": round(valence, 4)}
    for e in EMOTIONS:
        result[f"p_{e}"] = round(probas.get(e, 0.0), 4)
    return result


def run():
    workspace.set_workspace_path(os.path.dirname(os.path.abspath(__file__)))
    corpus_dir = workspace.get_corpus_path()
    output_dir = workspace.get_output_path()

    print("Cargando analizador de emociones")
    emotion_analyzer = create_analyzer(task="emotion", lang="es")

    all_message_rows = []

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

        messages = preprocess.load_messages(filepath)

        if not messages:
            print("  sin mensajes, omitida.")
            continue

        n = len(messages)
        for pos, (author, text) in enumerate(messages):
            result = analyze_message(text, emotion_analyzer)
            all_message_rows.append({
                "client": client,
                "session": date,
                "position": pos,
                "position_pct": round(pos / max(n - 1, 1) * 100, 1),
                "author": author,
                "text": text,
                "emotion": result["emotion"],
                "valence": result["valence"],
                "p_joy": result["p_joy"],
                "p_surprise": result["p_surprise"],
                "p_others": result["p_others"],
                "p_fear": result["p_fear"],
                "p_sadness": result["p_sadness"],
                "p_disgust": result["p_disgust"],
                "p_anger": result["p_anger"],
            })

        print(f"  {n} mensajes procesados")

    msg_path = os.path.join(output_dir, "tone_messages.csv")
    pd.DataFrame(all_message_rows).to_csv(msg_path, index=False, encoding="utf-8-sig")
    print(f"\nGuardado: {msg_path}")