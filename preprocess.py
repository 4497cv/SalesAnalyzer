import re
import glob
import os
import nltk
#from googletrans import Translator

#nltk.download('vader_lexicon')

def normalizacion_texto(texto):
    texto = texto.replace("oky", "ok")
    texto = texto.replace("paq", "paquetes")
    return texto

def normalizacion_puntuacion(texto):
    texto = texto.replace("???", "?")
    texto = texto.replace("??", "?")
    texto = texto.replace(" ,", ",")
    texto = texto.replace("  ", " ")
    #texto = texto.replace(" ?", "?")
    return texto

def normalizacion_bigramas(texto):
    norm_bigramas = {"d efavor": "de favor",
                     "con tigo": "contigo",
                     "porfavor": "por favor"}

    for bg_erroneo, bg_forma in norm_bigramas.items():
        # reemplaza el bigrama erroneo con su forma correcta
        texto = texto.replace(bg_erroneo, bg_forma)
    
    return texto

def preprocess_chat(filename):
    #pre-procesamiento del texto
    with open(filename, "r", encoding = "utf-8") as f:
        raw_chat = []
        processed_chat = []
        for line in f.readlines():
            line = line.replace("\n", "")
            raw_chat.append(line)

        for line in raw_chat:
            # separar fecha y hora del contenido
            chat_data = line.split("-", 1)
            # solo tomar en cuenta los mensajes que tienen fecha y el mensaje tiene contenido
            if len(chat_data) < 2:
                continue

            date_time = chat_data[0]
            date_time = date_time.split(",", 1)
            date = date_time[0]
            time = date_time[1]

            content = chat_data[1]
            content = content.split(":", 1)
            
            if(len(content) > 1):
                author = content[0]
                author = author[1:]
                text = content[1].lower()
                text = text[1:]
                # normalizar errores de texto, puntuacion y bigramas
                text = normalizacion_texto(text)
                text = normalizacion_puntuacion(text)
                text = normalizacion_bigramas(text)

                processed_text = author + ":" + text
                print(processed_text)

                if("<Multimedia omitido>" not in line):
                    processed_chat.append(processed_text)

    new_file = filename.replace(".txt", "_processed.txt")

    with open(new_file, "w+", encoding="utf-8") as f2:
        for line in processed_chat:
            f2.write(line + "\n")

corpus_dir = os.path.join(os.path.dirname(__file__), "corpus")
for txt_file in glob.glob(os.path.join(corpus_dir, "**", "*.txt"), recursive=True):
    if not txt_file.endswith("_processed.txt"):
        print(f"Procesando: {txt_file}")
        preprocess_chat(txt_file)