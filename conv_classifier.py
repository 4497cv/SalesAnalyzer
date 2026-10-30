import os
import joblib
import pandas
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier
import workspace
import auto_label

RANDOM_STATE = 42
# clases con menos ejemplos se agrupan en "Otras" para entrenar
MIN_SAMPLES = 20
# por debajo de esta probabilidad la conversacion queda como "No Clasificado"
CONFIANZA_MINIMA = 0.4
FEATURES = ["texto", "n_msgs"]

# mejores hiperparametros encontrados con el grid search del notebook "Classification Conv.ipynb"
XGB_PARAMS = {
    "max_depth": 3,
    "learning_rate": 0.1,
    "n_estimators": 200,
    "colsample_bytree": 0.5,
    "min_child_weight": 1,
}

def get_model_path():
    return os.path.join(workspace.get_ml_path(), "xgb_conv_classifier.joblib")

def get_gold_path():
    return os.path.join(workspace.get_ml_path(), "muestra_etiquetado.csv")

def load_dataset():
    # etiquetas generadas por las reglas de auto_label.py
    labels_path = os.path.join(workspace.get_ml_path(), "tf_idf_matrix_clases.csv")
    df_labels = pandas.read_csv(labels_path, encoding="utf-8-sig")

    rows = []
    for chat, clase in zip(df_labels["Chat"], df_labels["Clase"]):
        client, session = chat.split("/", 1)
        texto, n_msgs = auto_label.read_processed_chat(client, session)
        rows.append({
            "Chat": chat,
            "texto": auto_label.normalize(texto),
            "n_msgs": n_msgs,
            "Clase": clase,
        })
    return pandas.DataFrame(rows)

def build_pipeline(**xgb_params):
    # xgb_params permite sobreescribir cualquier parametro de XGBClassifier
    params = {
        "objective": "multi:softprob",
        "subsample": 0.8,
        "tree_method": "hist",
        "eval_metric": "mlogloss",
        "random_state": RANDOM_STATE,
        "n_jobs": -1,
        **XGB_PARAMS,
        **xgb_params,
    }
    return Pipeline([
        ("feats", ColumnTransformer([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True), "texto"),
            ("n_msgs", "passthrough", ["n_msgs"]),
        ])),
        ("xgb", XGBClassifier(**params)),
    ])

def get_rare_classes(clases):
    counts = clases.value_counts()
    return set(counts[counts < MIN_SAMPLES].index)

def train(data):
    # solo entrenamos con conversaciones con texto y con una clase asignada por las reglas
    train_df = data[(data["Clase"] != auto_label.SIN_CLASE) & (data["texto"] != "")]

    # la muestra de etiquetado manual nunca se usa para entrenar
    gold_path = get_gold_path()
    if os.path.exists(gold_path):
        gold_chats = set(pandas.read_csv(gold_path, encoding="utf-8-sig")["Chat"])
        train_df = train_df[~train_df["Chat"].isin(gold_chats)]

    raras = get_rare_classes(train_df["Clase"])
    y_raw = train_df["Clase"].where(~train_df["Clase"].isin(raras), "Otras")

    le = LabelEncoder()
    y = le.fit_transform(y_raw)

    model = build_pipeline()
    model.fit(train_df[FEATURES], y, xgb__sample_weight=compute_sample_weight("balanced", y))

    print(f"  Entrenado con {len(train_df)} conversaciones")
    print(f"  Clases: {list(le.classes_)}")
    if raras:
        print(f"  Agrupadas en 'Otras': {sorted(raras)}")

    return {"model": model, "label_encoder": le, "raras": raras}

def predict(bundle, data):
    model = bundle["model"]
    le = bundle["label_encoder"]

    probabilidades = model.predict_proba(data[FEATURES])
    predicciones = le.inverse_transform(probabilidades.argmax(axis=1))
    confianzas = probabilidades.max(axis=1)

    clases_finales = []
    for pred, conf, texto, clase_regla in zip(predicciones, confianzas, data["texto"], data["Clase"]):
        if not texto or conf < CONFIANZA_MINIMA:
            clases_finales.append(auto_label.SIN_CLASE)
        elif pred == "Otras":
            # "Otras" agrupa clases raras; si la regla detecto una de ellas usamos la clase especifica
            if clase_regla in bundle["raras"]:
                clases_finales.append(clase_regla)
            else:
                clases_finales.append(auto_label.SIN_CLASE)
        else:
            clases_finales.append(pred)

    return clases_finales, confianzas

def run():
    # 1. Cargar textos y etiquetas de las reglas
    print("Cargando conversaciones...")
    data = load_dataset()
    print(f"  Se han encontrado {len(data)} conversaciones")

    # 2. Entrenar el modelo
    print("\nEntrenando XGBoost...")
    bundle = train(data)
    joblib.dump(bundle, get_model_path())
    print(f"  Modelo guardado en: {get_model_path()}")

    # 3. Clasificar todas las conversaciones
    print("\nClasificando conversaciones...")
    clases, confianzas = predict(bundle, data)

    resultado = pandas.DataFrame({
        "chat": data["Chat"],
        "topic_cluster": clases,
        "confianza": confianzas.round(3),
        "clase_regla": data["Clase"],
    })

    # 4. Guardar en el formato que espera generate_gui_data.py
    out_path = os.path.join(workspace.get_output_path(), "topic_label_chat_cluster.csv")
    resultado.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"  Guardado en: {out_path}")

    # 5. Resumen
    print("\nDistribución de clases predichas:")
    print(resultado["topic_cluster"].value_counts().to_string())
    coincide = (resultado["topic_cluster"] == resultado["clase_regla"]).mean()
    print(f"\nCoincidencia con las reglas: {coincide:.1%}")
    print(f"Confianza  media: {confianzas.mean():.4f}  mín: {confianzas.min():.4f}  máx: {confianzas.max():.4f}")

    return bundle, resultado

if __name__ == "__main__":
    workspace.set_workspace_path(os.path.dirname(os.path.abspath(__file__)))
    run()
