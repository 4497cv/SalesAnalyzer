import re
import glob
import os
import nltk


#from googletrans import Translator

#nltk.download('vader_lexicon')

def normalizacion_texto(texto):
    texto = texto.replace("oky", "ok")
    texto = texto.replace("ati", "a ti")
    texto = texto.replace("aty", "a ti")
    texto = texto.replace("asii", "asi")
    texto = texto.replace("asii", "asi")
    texto = texto.replace("asta", "hasta")
    texto = texto.replace("asii", "asi")
    texto = texto.replace("andjunto", "adjunto")
    texto = texto.replace("aorita", "ahorita")
    texto = texto.replace("abra", "habra")
    texto = texto.replace("agregharemos", "agregaremos")
    texto = texto.replace("aleajandra", "alejandra")
    texto = texto.replace("bieb", "bien")
    texto = texto.replace("cres", "crees")
    texto = texto.replace("cuanrto", "cuanto")
    texto = texto.replace("domucilio", "domicilio")
    texto = texto.replace("sipis", "si")
    texto = texto.replace("sip", "si")
    texto = texto.replace("sio", "si")
    texto = texto.replace("similhares", "similares")
    texto = texto.replace("shabra", "sabra")
    texto = texto.replace("siii", "si")
    texto = texto.replace("sii", "si")
    texto = texto.replace("sustitua", "sustituya")
    texto = texto.replace("xfis", "porfis")
    texto = texto.replace("yaaaaa", "ya")
    texto = texto.replace("vidaaaaa", "vida")
    texto = texto.replace("plastoco", "plastico")
    texto = texto.replace("viendop", "viendo")
    texto = texto.replace("hh", "h")
    texto = texto.replace("kh", "k")
    texto = texto.replace("ð", "")
    texto = texto.replace("Ÿ", "")
    texto = texto.replace("˜", "")
    texto = texto.replace("â", "")
    texto = texto.replace("œ", "")
    texto = texto.replace("¨", "")
    texto = texto.replace("Š", "")
    texto = texto.replace("{", "")
    texto = texto.replace("}", "")
    texto = texto.replace("[", "")
    texto = texto.replace("]", "")
    texto = texto.replace("*", "")
    texto = texto.replace("@", "")
    texto = texto.replace("pha", "pa")
    texto = texto.replace("phe", "pa")
    texto = texto.replace("phi", "pa")
    texto = texto.replace("scoch", "scotch")

    texto = texto.replace("paq", "paquetes")
    #texto = re.sub(r'[áéíóúñ]', lambda m: {'á':'a','é':'e','í':'i','ó':'o','ú':'u', 'ñ':'n'}[m.group()], texto)

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
                     "porfavor": "por favor",
                     "alomejor": "a lo mejor",
                     "ala": "a la",
                     "are": "hare",
                     "acjas": "cajas",
                     "acolgar": "a colgar",
                     "ami": "a mi",
                     "aprogramacion": "a programacion",
                     "aque": "a que",
                     "avisasi": "avisas si",
                     "yavi": "ya vi"}

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
            # Formato nuevo: [DD/MM/YY, HH:MM:SS p.m.] Author: message
            if line.startswith("["):
                bracket_end = line.find("]")
                if bracket_end == -1:
                    continue
                content_raw = line[bracket_end + 1:].strip()
            else:
                # Formato viejo: DD/MM/YYYY, HH:MM - Author: message
                chat_data = line.split("-", 1)
                if len(chat_data) < 2:
                    continue
                content_raw = chat_data[1].strip()

            content = content_raw.split(":", 1)

            if(len(content) > 1):
                author = content[0].strip()
                text = content[1].lower().strip()
                # normalizar errores de texto, puntuacion y bigramas
                text = normalizacion_texto(text)
                text = normalizacion_puntuacion(text)
                text = normalizacion_bigramas(text)

                processed_text = author + ":" + text
                words_list = re.split(r"[ .,]+", text)

                #found_words, similar_words, unfound_words = trie.process_text_optimized(words_list)
                #print(similar_words)

                if("<Multimedia omitido>" not in line):
                    processed_chat.append(processed_text)

    new_file = filename.replace(".txt", "_processed.txt")

    with open(new_file, "w+", encoding="utf-8") as f2:
        for line in processed_chat:
            f2.write(line + "\n")

def extract_author_text(line: str) -> tuple[str, str]:
    """
    Parsea una linea en formato 'author:text' de mensajes_processed.txt.
    Retorna (author, text). Si no hay ':', retorna ('', line).
    """
    parts = line.strip().split(":", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return "", line.strip()


def clean_for_sentiment(texto: str) -> str:
    """
    Limpieza adicional orientada a sentiment analysis:
    - Elimina URLs
    - Elimina menciones @usuario
    - Colapsa espacios multiples
    - Elimina tokens numericos puros (precios, telefonos no aportan sentimiento)
    - Elimina tokens de un solo caracter
    """
    texto = re.sub(r"https?://\S+|www\.\S+", "", texto)
    texto = re.sub(r"@\w+", "", texto)
    texto = re.sub(r"\b\d+\b", "", texto)
    tokens = [t for t in texto.split() if len(t) > 1]
    return " ".join(tokens).strip()


def normalize_for_sentiment(texto: str) -> str:
    """
    Pipeline completo para preparar un mensaje antes de sentiment analysis.
    Aplica: correccion de typos -> puntuacion -> bigramas -> limpieza de sentimiento.
    """
    texto = normalizacion_texto(texto)
    texto = normalizacion_puntuacion(texto)
    texto = normalizacion_bigramas(texto)
    texto = clean_for_sentiment(texto)
    return texto


def run():
    corpus_dir = os.path.join(os.path.dirname(__file__), "corpus")
    for txt_file in glob.glob(os.path.join(corpus_dir, "**", "*.txt"), recursive=True):
        if not txt_file.endswith("_processed.txt"):
            print(f"Procesando: {txt_file}")
            preprocess_chat(txt_file)


if __name__ == "__main__":
    run()