import build_corpus
import preprocess
import bagofwords
import test as tfidf_sklearn
from AI import build_corpus_ner, domain_dictionary, sentiment_analysis, tone_evolution

print("=" * 50)
print("Etapa 1: Construyendo corpus...")
print("=" * 50)
build_corpus.run()

print("\n" + "=" * 50)
print("Etapa 2: Preprocesando mensajes...")
print("=" * 50)
preprocess.run()

print("\n" + "=" * 50)
print("Etapa 3a: BoW y matrices de distancia...")
print("=" * 50)
#bagofwords.run()

print("\n" + "=" * 50)
print("Etapa 3b: TF-IDF con bigramas (sklearn)...")
print("=" * 50)
#tfidf_sklearn.run()

print("\n" + "=" * 50)
print("Etapa 4: NER sobre el corpus...")
print("=" * 50)
#build_corpus_ner.main()

print("\n" + "=" * 50)
print("Etapa 5: Diccionario de dominio...")
print("=" * 50)
#domain_dictionary.main()

print("\n" + "=" * 50)
print("Etapa 6: Analisis de sentimiento...")
print("=" * 50)
#sentiment_analysis.main()

print("\n" + "=" * 50)
print("Etapa 7: Evolucion de tono...")
print("=" * 50)
#tone_evolution.main()

print("\nPipeline completo.")
