import build_corpus
import preprocess
import bagofwords
import test as tfidf_sklearn
from AI import build_corpus_ner, domain_dictionary, sentiment_analysis, tone_evolution
import workspace
import os
import time
import chat_cluster
import generate_gui_data
import sys

def __main__():
    args = sys.argv[1:]

    # configurar la ruta del workspace actual
    workspace.set_workspace_path(os.path.dirname(os.path.abspath(__file__)))

    if(("-corpus" not in args) and\
       ("-guidata" not in args) and\
       ("-preprocess" not in args) and\
       ("-mat" not in args) and\
       ("-cner" not in args) and\
       ("-domaindict" not in args) and\
       ("-sentiment" not in args) and\
       ("-tone" not in args) and\
       ("-cluster" not in args) and\
       ("-guidata" not in args) and\
       ("-a" not in args)):
        sys.exit("command not selected")
    else:
        print("commands: %s" % args)

    if(("-corpus" in args) or ("-a" in args)):
        t_start = time.time()
        # 1. creacion del corpus en base a mensajes de texto
        print("Etapa 1: Construyendo corpus...")
        build_corpus.run()
        t_stop = time.time()
        total_time = t_stop - t_start
        print("Etapa 1 tiempo = %.2f" % total_time)

    if(("-preprocess" in args) or ("-a" in args)):
        t_start = time.time()
        # 2. preprocesamiento de mensajes
        print("Etapa 2: Preprocesando mensajes...")
        preprocess.run()
        t_stop = time.time()
        total_time = t_stop - t_start
        print("Etapa 2 tiempo = %.2f" % total_time)

    if(("-mat" in args) or ("-a" in args)):
        # calcular bag of words y las matrices TF-IDF, distancia coseno y distancia euclidiana
        print("Etapa 3a: BoW y matrices de distancia...")
        bagofwords.run()

        print("Etapa 3b: TF-IDF con bigramas (sklearn)...")
        #tfidf_sklearn.run()

    if(("-cner" in args) or ("-a" in args)):
        print("Etapa 4: NER sobre el corpus...")
        build_corpus_ner.main()

    if(("-domaindict" in args) or ("-a" in args)):
        print("Etapa 5: Diccionario de dominio...")
        domain_dictionary.main()

    if(("-sentiment" in args) or ("-a" in args)):
        print("Etapa 6: Analisis de sentimiento...")
        sentiment_analysis.main()

    if(("-tone" in args) or ("-a" in args)):
        print("Etapa 7: Evolucion de tono...")
        tone_evolution.main()

    if(("-cluster" in args) or ("-a" in args)):
        print("Etapa 8. Clasificación de conversaciones")
        chat_cluster.run()

    if(("-guidata" in args) or ("-a" in args)):
        print("Etapa 9. Generar Datos para GUI")
        generate_gui_data.main()

    print("\nPipeline completo.")

__main__()