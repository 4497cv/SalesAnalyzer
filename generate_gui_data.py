"""
Generates GUI/conversations_data.js from output/tone_messages.csv and
output/sentiment_by_author.csv.
Run once after each pipeline execution: python generate_gui_data.py
"""
import csv, json, re
from collections import defaultdict, Counter
import workspace

SELLERS = {"Comercios Unidos", "Permagraf"}

EMOTION_ORDER  = ["others", "joy", "anger", "sadness", "surprise", "fear", "disgust"]
EMOTION_COLORS = {
    "others":   "var(--emo-others-fg)",
    "joy":      "var(--emo-joy-fg)",
    "anger":    "var(--emo-anger-fg)",
    "sadness":  "var(--emo-sadness-fg)",
    "surprise": "var(--emo-surprise-fg)",
    "fear":     "var(--emo-fear-fg)",
    "disgust":  "var(--emo-others-fg)",
}


def client_id(name):
    return re.sub(r'[^a-z0-9]', '_', name.lower()).strip('_')[:48]


def extract_office(client):
    m = re.match(r'^(T\d+|t\d+)', client)
    return m.group(1).upper() if m else "—"


def session_to_date(session):
    parts = session.split("-")
    if len(parts) == 3:
        return f"{parts[2]}-{parts[1]}-{parts[0]}"
    return session


def load_domain_dictionary(out_dir):
    path = out_dir + "/domain_dictionary.csv"
    terms = []
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            terms.append({
                "rank":        int(row["rank"]),
                "term":        row["term"],
                "score":       round(float(row["global_score"]), 3),
                "docFreq":     int(row["doc_freq"]),
                "docFreqPct":  round(float(row["doc_freq_pct"]), 1),
                "isBigram":    row["is_bigram"] == "True",
                "topicLabel":  row["topic_label"],
                "topicRank":   int(row["topic_rank"]),
            })
    return terms


def load_topic_clusters(out_dir):
    cluster_path = out_dir + "/topic_label_chat_cluster.csv"
    lookup = {}
    with open(cluster_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            parts = row["chat"].replace("\\", "/").split("/")
            if len(parts) >= 2:
                lookup[(parts[0], parts[1])] = row["topic_cluster"] or None
    return lookup


def main():
    out_dir     = workspace.get_output_path()
    tone_path   = out_dir + "/tone_messages.csv"
    author_path = out_dir + "/sentiment_by_author.csv"

    domain_dictionary = load_domain_dictionary(out_dir)
    topic_clusters    = load_topic_clusters(out_dir)

    # ── Pass 1: tone_messages → conversations + dashboard metrics ──
    groups        = defaultdict(list)
    all_valences  = []
    emotion_count = Counter()

    with open(tone_path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            groups[(row["client"], row["session"])].append(row)
            all_valences.append(float(row["valence"]))
            emotion_count[row["emotion"]] += 1

    # Build conversations
    conversations = []
    seen_clients  = {}

    for (client, session), rows in sorted(groups.items()):
        rows.sort(key=lambda r: int(r["position"]))

        sellers_seen = {r["author"] for r in rows if r["author"] in SELLERS}
        seller_label = next(iter(sellers_seen), "Comercios Unidos")

        messages = []
        for r in rows:
            author = r["author"]
            role = "seller" if author in SELLERS else "client"
            messages.append({
                "t":          f"#{int(r['position']) + 1}",
                "posPct":     round(float(r["position_pct"]), 1),
                "author":     author,
                "role":       role,
                "text":       r["text"],
                "valence":    round(float(r["valence"]), 4),
                "emotion":    r["emotion"],
                "p_joy":      round(float(r["p_joy"]), 4),
                "p_surprise": round(float(r["p_surprise"]), 4),
                "p_others":   round(float(r["p_others"]), 4),
                "p_fear":     round(float(r["p_fear"]), 4),
                "p_sadness":  round(float(r["p_sadness"]), 4),
                "p_disgust":  round(float(r["p_disgust"]), 4),
                "p_anger":    round(float(r["p_anger"]), 4),
            })

        valences = [m["valence"] for m in messages]
        avg_v    = round(sum(valences) / len(valences), 4) if valences else 0.0
        cid      = client_id(client)

        conversations.append({
            "id":              f"{cid}__{session}",
            "clientId":        cid,
            "clientName":      client,
            "session":         session,
            "office":          extract_office(client),
            "date":            session_to_date(session),
            "seller":          seller_label,
            "avgValence":      avg_v,
            "msgCount":        len(messages),
            "hasAlert":        any(m["valence"] < -0.15 for m in messages),
            "topicCluster":    topic_clusters.get((client, session)),
            "productMentions": [],
            "objections":      [],
            "messages":        messages,
        })

        if cid not in seen_clients:
            seen_clients[cid] = {
                "id":            cid,
                "name":          client,
                "office":        extract_office(client),
                "segment":       "—",
                "category":      "—",
                "contact":       client,
                "phone":         "—",
                "since":         "—",
                "recompra":      "—",
                "ltv":           0,
                "conversations": 0,
            }
        seen_clients[cid]["conversations"] += 1

    clients = sorted(seen_clients.values(), key=lambda c: c["name"])

    # ── Dashboard KPIs ──
    avg_valence = round(sum(all_valences) / len(all_valences), 4) if all_valences else 0.0

    emotion_dist = []
    for name in EMOTION_ORDER:
        count = emotion_count.get(name, 0)
        if count:
            emotion_dist.append({
                "name":  name,
                "count": count,
                "color": EMOTION_COLORS[name],
            })
    # append any unexpected emotion labels at the end
    for name, count in emotion_count.items():
        if name not in EMOTION_ORDER and count:
            emotion_dist.append({
                "name":  name,
                "count": count,
                "color": EMOTION_COLORS.get(name, "var(--emo-others-fg)"),
            })

    # ── Pass 2: sentiment_by_author → authorSentiment ──
    author_sentiment = []
    with open(author_path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            author = row["author"]
            role   = "seller" if author in SELLERS else "client"
            vendor = extract_office(author) if role == "client" else "—"
            author_sentiment.append({
                "author":        author,
                "vendedora":     vendor,
                "role":          role,
                "totalMessages": int(row["total_messages"]),
                "posPct":        round(float(row["pos_pct"]), 1),
                "neuPct":        round(float(row["neu_pct"]), 1),
                "negPct":        round(float(row["neg_pct"]), 1),
                "avgScore":      round(float(row["avg_score"]), 4),
                "dominant":      row["dominant"],
            })

    # ── Write JS ──
    gui_path = workspace.get_workspace_path() + "/GUI/conversations_data.js"
    with open(gui_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated by generate_gui_data.py — do not edit by hand\n")
        f.write("(function(){\n")

        f.write("  window.MOCK.conversations = ")
        f.write(json.dumps(conversations, ensure_ascii=False))
        f.write(";\n")

        f.write("  window.MOCK.clients = ")
        f.write(json.dumps(clients, ensure_ascii=False))
        f.write(";\n")

        f.write("  window.MOCK.authorSentiment = ")
        f.write(json.dumps(author_sentiment, ensure_ascii=False))
        f.write(";\n")

        f.write("  window.MOCK.emotionDist = ")
        f.write(json.dumps(emotion_dist, ensure_ascii=False))
        f.write(";\n")

        f.write("  window.MOCK.domainDictionary = ")
        f.write(json.dumps(domain_dictionary, ensure_ascii=False))
        f.write(";\n")

        f.write(f"  window.MOCK.kpis.conversations      = {len(conversations)};\n")
        f.write(f"  window.MOCK.kpis.conversationsDelta = null;\n")
        f.write(f"  window.MOCK.kpis.messagesProcessed  = {len(all_valences)};\n")
        f.write(f"  window.MOCK.kpis.avgValence         = {avg_valence};\n")
        f.write(f"  window.MOCK.kpis.avgValenceDelta    = null;\n")
        f.write(f"  window.MOCK.kpis.authors            = {len(author_sentiment)};\n")

        f.write("})();\n")

    print(f"OK  {len(conversations)} conversaciones, {len(clients)} clientes, "
          f"{len(all_valences)} mensajes, avgValence={avg_valence} -> {gui_path}")


if __name__ == "__main__":
    main()
