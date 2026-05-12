import os
import sys
import pandas
from sklearn.linear_model import LogisticRegression
import workspace

def load_tf_idf_train():
    csv_path = os.path.join(workspace.get_ml_path(), "tf_idf_matrix_filtrado.csv")
    df = pandas.read_csv(csv_path, encoding="utf-8-sig", index_col=0)
    return df

def load_tf_idf_clases():
    csv_path = os.path.join(workspace.get_ml_path(), "tf_idf_clases_filtradas.csv")
    df = pandas.read_csv(csv_path, encoding="utf-8-sig")
    df = df.set_index('Chat')
    return df['Clase']

def load_tf_idf_all():
    csv_path = os.path.join(workspace.get_output_path(), "tf_idf_matrix.csv")
    df = pandas.read_csv(csv_path, encoding="utf-8-sig", index_col=0)
    return df

def run():
    # 1. Cargar datos de entrenamiento
    print("Cargando datos...")
    X_train = load_tf_idf_train()
    Y_train = load_tf_idf_clases()

    print(f"  X shape: {X_train.shape}")
    print(f"  Y shape: {Y_train.shape}")
    print(f"  Clases: {list(Y_train.unique())}")

    # 2. Entrenar modelo
    print("\nEntrenando Logistic Regression...")
    model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    model.fit(X_train, Y_train)

    train_score = model.score(X_train, Y_train)
    print(f"  Accuracy en entrenamiento: {train_score:.4f}")

    # 3. Predecir en TODAS las conversaciones del corpus
    print("\nPrediciendo clases para todas las conversaciones...")
    X_all = load_tf_idf_all()

    predicciones = model.predict(X_all)
    probabilidades = model.predict_proba(X_all)
    confianzas = probabilidades.max(axis=1)


    CONFIANZA_MINIMA = 0.4
    clases_finales = []
    for pred, conf in zip(predicciones, confianzas):
        if conf >= CONFIANZA_MINIMA:
            clases_finales.append(pred)
        else:
            clases_finales.append("No Clasificado")

    # 4. Armar y guardar resultado en el mismo formato que antes
    resultado = pandas.DataFrame({
        'chat': X_all.index,
        'topic_cluster': clases_finales,
    })

    out_path = os.path.join(workspace.get_output_path(), "topic_label_chat_cluster.csv")
    resultado.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"  Guardado en: {out_path}")

    # 5. Resumen
    print("\nDistribución de clases predichas:")
    print(resultado['topic_cluster'].value_counts().to_string())
    print(f"\nConfianza  media: {confianzas.mean():.4f}  "
          f"mín: {confianzas.min():.4f}  "
          f"máx: {confianzas.max():.4f}")

    return model, resultado


if __name__ == "__main__":
    run()
