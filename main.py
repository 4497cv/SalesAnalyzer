import workspace
import os
import sys
import time
import webbrowser
import subprocess

def __main__():
    args = sys.argv[1:]

    # configurar la ruta del workspace actual
    workspace.set_workspace_path(os.path.dirname(os.path.abspath(__file__)))

    if(("-corpus" not in args) and\
       ("-guidata" not in args) and\
       ("-preprocess" not in args) and\
       ("-mat" not in args) and\
       ("-ner" not in args) and\
       ("-domaindict" not in args) and\
       ("-sentiment" not in args) and\
       ("-tone" not in args) and\
       ("-cluster" not in args) and\
       ("-guidata" not in args) and\
       ("-help" not in args) and\
       ("-a" not in args)):
        print("escribe -help para ver los comandos disponibles...")
        sys.exit("comando no seleccionado")
    else:
        print("comandos: %s" % args)

    if(("-corpus" in args)):
        import build_corpus
        t_start = time.time()
        # 1. creacion del corpus en base a mensajes de texto
        print("Etapa 1: Construyendo corpus")
        build_corpus.run()
        t_stop = time.time()
        total_time = t_stop - t_start
        print("Etapa 1 tiempo = %.2f" % total_time)

    if(("-preprocess" in args) or ("-a" in args)):
        import preprocess
        t_start = time.time()
        # 2. preprocesamiento de mensajes
        print("Etapa 2: Preprocesando mensajes")
        preprocess.run()
        t_stop = time.time()
        total_time = t_stop - t_start
        print("Etapa 2 tiempo = %.2f" % total_time)

    if(("-mat" in args) or ("-a" in args)):
        import bagofwords
        import tf_idf
        # 3. calcular bag of words y las matrices TF-IDF, distancia coseno y distancia euclidiana
        print("Etapa 3a: BoW y matrices de distancia")
        bagofwords.run()

        print("Etapa 3b: TF-IDF con bigramas...")
        tf_idf.run()

    if(("-domaindict" in args) or ("-a" in args)):
        import domain_dict
        print("Etapa 4: Diccionario de dominio")
        domain_dict.run()

    if(("-sentiment" in args) or ("-a" in args)):
        import sentiment_analysis
        print("Etapa 5: Analisis de sentimiento")
        sentiment_analysis.run()

    if(("-tone" in args) or ("-a" in args)):
        import tone_evolution
        print("Etapa 6: Evolucion de tono")
        tone_evolution.run()

    if(("-cluster" in args) or ("-a" in args)):
        import auto_label
        print("Etapa 7. Clasificación de conversaciones")
        auto_label.run()

    if(("-guidata" in args) or ("-a" in args)):
        import generate_gui_data
        print("Etapa 8. Generar Datos para GUI")
        generate_gui_data.main()
        gui_dir = os.path.join(workspace.get_workspace_path(), "GUI")
        puerto = 8765
        subprocess.Popen([sys.executable, "-m", "http.server", str(puerto)], cwd=gui_dir)
        time.sleep(0.5)
        webbrowser.open(f"http://localhost:{puerto}/Comercios%20Unidos%20Insights.html")

    if("-help" in args):
        print("-a: ejecutar todas las etapas del pipeline ")
        print("-corpus: construir corpus desde exportaciones de WhatsApp")
        print("-preprocess: preprocesar mensajes del corpus")
        print("-mat: calcular matrices BoW y TF-IDF")
        print("-domaindict: generar diccionario de dominio")
        print("-sentiment: analisis de sentimiento")
        print("-tone: analisis de evolucion de tono")
        print("-cluster: clasificacion de conversaciones")
        print("-guidata: generar datos para la GUI")

    print("\nPipeline completo.")

__main__()