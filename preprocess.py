import re
import glob
import os
import nltk
from trie import *
#from googletrans import Translator

#nltk.download('vader_lexicon')
unfound_words = []

trie = Trie(language = "es", dict_size = 100000)

def limpiar_emojis_texto(texto):
    EMOJI_RE = re.compile("[\U00010000-\U0010FFFF]", flags=re.UNICODE)
    return EMOJI_RE.sub("", texto).strip()

def validar_emoji_en_texto(texto):
    EMOJI_RE = re.compile("[\U00010000-\U0010FFFF]", flags=re.UNICODE)
    resultado = bool(EMOJI_RE.search(texto))
    return resultado

def validar_alpha_en_texto(texto):
    ALPHA_RE = re.compile(r'[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]')    
    resultado = bool(ALPHA_RE.search(texto))
    return resultado

def normalizacion_texto(texto):
    texto = texto.replace("phasta", "hasta")
    texto = texto.replace("pha", "pa")
    texto = texto.replace("phe", "pe")
    texto = texto.replace("phi", "pi")
    texto = texto.replace("pho", "po")
    texto = texto.replace("phu", "pu")
    texto = texto.replace("lha", "la")
    texto = texto.replace("lhe", "le")
    texto = texto.replace("lhi", "li")
    texto = texto.replace("lho", "lo")
    texto = texto.replace("lhu", "lu")
    texto = texto.replace("kha", "ka")
    texto = texto.replace("khe", "ke")
    texto = texto.replace("khe", "ke")
    texto = re.sub(r'\bke\b', 'que', texto)
    texto = texto.replace("cub.", "cubierta")
    texto = texto.replace("sr", "señor")
    texto = texto.replace("khi", "ki")
    texto = texto.replace("kho", "ko")
    texto = texto.replace("khu", "ku")
    texto = texto.replace("oky", "ok")
    texto = texto.replace("okis", "ok")
    texto = texto.replace("oki", "ok")
    texto = texto.replace("oks", "ok")
    texto = texto.replace("okd", "ok")
    texto = texto.replace("okok", "ok")
    texto = texto.replace("okk", "ok")
    texto = re.sub(r'\bgrs\b', 'gracias', texto)
    texto = texto.replace("graciasss", "gracias")
    texto = texto.replace("gracia a", "gracias a ti")
    texto = re.sub(r'\bgracia\b', 'gracias', texto)
    texto = texto.replace("grax", "gracias")
    texto = texto.replace("gracuas", "gracias")
    texto = texto.replace("gracoas", "gracias")
    texto = texto.replace("gravias", "gracias")
    texto = texto.replace("ntp", "no te preocupes")
    texto = texto.replace("okrok", "ok")
    texto = re.sub(r'\bola\b', 'hola', texto)
    texto = texto.replace("holis", "hola")
    texto = texto.replace("pzas", "piezas")
    texto = texto.replace("complmentos", "complementos")
    texto = texto.replace("Nuevamanete", "nuevamente")
    texto = texto.replace("pzs", "piezas")
    texto = texto.replace("pz", "piezas")
    texto = texto.replace(" qui ", " que ")
    texto = texto.replace("ati", "a ti")
    texto = texto.replace("aty", "a ti")
    texto = re.sub(r'\bti,', 'a ti,', texto)
    texto = texto.replace("ondas", "onda")
    texto = texto.replace("lavoraste", "laboraste")
    texto = texto.replace("bbuenas", "buenas")
    texto = texto.replace(" uenas", " buenas")
    texto = texto.replace("jesusi", "jesus")
    texto = texto.replace("pork", "porque")
    texto = texto.replace("asii", "asi")
    texto = texto.replace("nop", "no")
    texto = re.sub(r'\basta\b', 'hasta', texto)
    texto = re.sub(r'\bud\b', 'usted', texto)
    texto = texto.replace("oyes", "oye")
    texto = texto.replace("srita", "señorita")
    texto = texto.replace("sirfavor", "porfavor")
    texto = texto.replace("xfa", "porfavor")
    texto = texto.replace("porfa", "porfavor")
    texto = texto.replace("porfavorvor", "porfavor")
    texto = texto.replace("por favor", "porfavor")
    texto = texto.replace("por fas", "porfavor")
    texto = texto.replace("por fa", "porfavor")
    texto = re.sub(r'\btmb\b', 'también', texto)
    texto = re.sub(r'\bik\b', 'y que', texto)
    texto = re.sub(r'\boc\b', 'orden de compra', texto)
    texto = re.sub(r'\bnc\b', 'nota de credito', texto)
    texto = re.sub(r'\btc\b', 'tarjeta de credito', texto)
    texto = texto.replace("facturaturitas", "facturas")
    texto = texto.replace("facturaturar", "facturar")
    texto = texto.replace("facturature", "factura")
    texto = texto.replace("facturaturo", "facturo")
    texto = texto.replace("facturatura", "factura")
    texto = re.sub(r'\bfac\b', 'factura', texto)
    texto = texto.replace("gad", "gracias a Dios")
    texto = texto.replace("bdias", "buenos dias")
    texto = texto.replace("bdia", "buen día")
    texto = texto.replace("buen dia", "buen día")
    texto = texto.replace("andjunto", "adjunto")
    texto = texto.replace("aorita", "ahorita")
    texto = texto.replace("vd", "verdad")
    texto = texto.replace("abra", "habra")
    texto = texto.replace("agregharemos", "agregaremos")
    texto = texto.replace("aleajandra", "alejandra")
    texto = texto.replace("bieb", "bien")
    texto = texto.replace("bienn", "bien")
    texto = texto.replace("bnien", "bien")
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
    texto = texto.replace("xfis", "por favor")
    texto = texto.replace("yaaaaa", "ya")
    texto = texto.replace("vidaaaaa", "vida")
    texto = texto.replace("plastoco", "plastico")
    texto = texto.replace("viendop", "viendo")
    texto = texto.replace("hh", "h")
    texto = texto.replace("kh", "k")
    texto = texto.replace("xk", "porque")
    texto = texto.replace("quew", "que")
    texto = texto.replace("img", "imagen")
    texto = texto.replace("oie", "oye")
    texto = texto.replace("oyes", "oye")
    texto = texto.replace("aña", "año")
    texto = texto.replace(" paq ", "paquete")
    texto = texto.replace("revisin", "revision")
    texto = texto.replace("somn", "son")
    texto = texto.replace("sonj", "son")
    texto = texto.replace("mañona", "mañana")
    texto = texto.replace("acjas", "cajas")
    texto = texto.replace("quie", "que")
    texto = texto.replace("queres", "quieres")
    texto = texto.replace("queren", "quieren")
    texto = texto.replace("quere", "quiere")
    texto = texto.replace("queras", "quieras")
    texto = texto.replace("quera", "quiera")
    texto = texto.replace("quero", "quiero")
    texto = texto.replace("estass", "estas")
    texto = texto.replace("esya", "esta")
    texto = re.sub(r'\baun\b', 'aún', texto)
    texto = texto.replace("erann", "eran")
    texto = texto.replace("pence", "pensé")
    texto = texto.replace("mandamelo", "mándamelo")
    texto = re.sub(r'\bcotice\b', 'coticé', texto)
    texto = re.sub(r'\bcuanto\b', 'cuánto', texto)
    texto = re.sub(r'\bcuantas\b', 'cuántas', texto)
    texto = re.sub(r'\bcuantos\b', 'cuántos', texto)
    texto = re.sub(r'\bacrilico\b', 'acrílico', texto)
    texto = re.sub(r'\brazon\b', 'razón', texto)
    texto = re.sub(r'\bmerida\b', 'mérida', texto)
    texto = re.sub(r'\bperdon\b', 'perdón', texto)
    texto = re.sub(r'\bdioso\b', 'dios', texto)
    texto = re.sub(r'\beh\b', 'he', texto)
    texto = texto.replace("plimas", "plumas")
    texto = texto.replace("apieza", "una pieza")
    texto = re.sub(r'\bhunmedas\b', 'húmedas', texto)
    texto = re.sub(r'\balguos\b', 'algunos', texto)
    texto = texto.replace("ahpraita", "ahorita")
    texto = re.sub(r'\bcotizacion\b', 'cotización', texto)
    texto = re.sub(r'\bpregunte\b', 'pregunté', texto)
    texto = re.sub(r'\blapiz\b', 'lápiz', texto)
    texto = texto.replace("carpetade de", "carpeta de")
    texto = texto.replace("piezasa", "piezas")
    texto = texto.replace("jjaja", "jaja")
    texto = re.sub(r'\bquien\b', 'quién', texto)
    texto = re.sub(r'\borita\b', 'ahorita', texto)
    texto = re.sub(r'\bgenerico\b', 'genérico', texto)
    texto = texto.replace("okoiki", "ok")
    texto = re.sub(r'\bsabado\b', 'sábado', texto)
    texto = texto.replace("jrje", "jeje")
    texto = texto.replace("btardes", "buenas tardes")
    texto = texto.replace("sholamente", "solamente")
    texto = texto.replace("remisin", "remision")
    texto = texto.replace("visin", "vision")
    texto = texto.replace("<se editó este mensaje.>", "")
    texto = re.sub(r'\baya\b', 'allá', texto)
    texto = texto.replace("nomnre", "nombre")
    texto = texto.replace("elsta", "esta")
    texto = texto.replace("nuevp", "nuevo")
    texto = re.sub(r'(\d)([a-záéíóúüñ])', r'\1 \2', texto)
    texto = re.sub(r'([a-záéíóúüñ])(\d)', r'\1 \2', texto)
    #texto = re.sub(r'[áéíóúñ]', lambda m: {'á':'a','é':'e','í':'i','ó':'o','ú':'u', 'ñ':'n'}[m.group()], texto)

    return texto

def normalizacion_nombres(texto):
    texto = texto.replace("aleajandra", "alejandra")
    texto = texto.replace("aleajandra", "alejanda")
    texto = texto.replace("kharely", "Karely")
    texto = texto.replace("rossy", "rosy")
    texto = texto.replace("betzavel", "betzabel")
    texto = texto.replace("zuleika", "zuleica")
    texto = texto.replace("zuelika", "zuleica")
    texto = texto.replace("casandra", "cassandra")
    texto = texto.replace("ka tia", "katia")
    texto = texto.replace("cerlox", "xerox")
    texto = texto.replace("victorio", "victoria")
    texto = texto.replace("scoch", "scotch")
    return texto

def normalizacion_puntuacion(texto):
    texto = texto.replace("???", "?")
    texto = texto.replace("??", "?")
    texto = texto.replace(" ,", ",")
    texto = texto.replace("  ", " ")
    texto = texto.replace("   ", " ")
    if(".com" not in texto):
        texto = texto.replace(".", " ")
    #texto = texto.replace(" ?", "?")
    texto = texto.replace(",.", "") 
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
    texto = texto.replace("☹️", "")
    texto = texto.replace("☺️", "")
    texto = texto.replace("*", "")
    texto = texto.replace("-¡", "")
    texto = texto.replace("@", "")
    texto = texto.replace("<", "")
    texto = texto.replace(">", "")
    texto = texto.replace(":", "")
    texto = texto.replace("/", "")
    texto = texto.replace("°", "")
    texto = texto.replace("--", "")
    texto = texto.replace(",.", "") 
    texto = texto.replace("()", "")
    texto = texto.replace("}?", "")
    return texto

def normalizacion_bigramas(texto):
    norm_bigramas = {"d efavor": "de favor",
                     "con tigo": "contigo",
                     "alomejor": "a lo mejor",
                     "claroquesi": "claro que si",
                     " ala ": "a la",
                     "buend ia": "buen día",
                     " are ": "hare",
                     "acolgar": "a colgar",
                     " ami ": "a mi",
                     " aprogramacion ": "a programacion",
                     " aque ": "a que",
                     " avisasi ": "avisas si",
                     " yavi ": "ya vi",
                     " esque ": "es que",
                     "estabien": "esta bien",
                     "paquetede": "paquete de",
                     "comfu": "con su",
                     "ra tito": "ratito",
                     "tintaquecolor": "tinta que color",
                     "automa tico": "automatico",
                     "corpora tivo": "corporativo",
                     "pa ti": "para ti",
                     "a tu": "a ti",
                     "re sirve": "te sirve",
                     "como estas": "cómo estás",
                     "como esta": "cómo está",
                     "buenosd ias": "buenos dias",
                     }

    for bg_erroneo, bg_forma in norm_bigramas.items():
        # reemplaza el bigrama erroneo con su forma correcta
        texto = texto.replace(bg_erroneo, bg_forma)
    
    return texto

def preprocess_chat(filename, trie_flag = 0):
    
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
            elif line and line[0].isdigit():
                # Formato viejo WhatsApp: DD/MM/YYYY, HH:MM - Author: message
                parts = line.split(" - ", 1)
                if len(parts) < 2:
                    continue
                content_raw = parts[1].strip()
            else:
                # Formato FB/directo: Author: message (sin fecha ni timestamp)
                content_raw = line

            content = content_raw.split(":", 1)

            if(len(content) > 1):
                author = content[0].strip()
                text = content[1].lower().strip()
                # quitar emojis del texto
                if(validar_alpha_en_texto(text) and validar_emoji_en_texto(text)):
                    text = limpiar_emojis_texto(text)

                # normalizar errores de texto, puntuacion y bigramas
                text = normalizacion_texto(text)
                text = normalizacion_puntuacion(text)
                text = normalizacion_bigramas(text)
                text = normalizacion_nombres(text)

                processed_text = author + ":" + text
                words_list = re.split(r"[ .,]+", text)
                
                if(trie_flag):
                    found_words, similar_words, unfound_words = trie.process_text_optimized(words_list)
                    unfound_words.append(unfound_words)

                if(("<Multimedia omitido>" not in line) and\
                   ("Eliminaste este mensaje" not in line) and \
                   ("se eliminó este mensaje" not in line) and \
                   ("(archivo adjunto)"not in line) and \
                   (False == validar_emoji_en_texto(line))):
                    processed_chat.append(processed_text)

    new_file = filename.replace(".txt", "_processed.txt")

    with open(new_file, "w+", encoding="utf-8") as f2:
        for line in processed_chat:
            f2.write(line + "\n")
    
    if(trie_flag):
        with open("unfound_words.txt", "a+", encoding = "utf-8") as f3:
            for element in unfound_words:
                f3.write(str(element) + "\n")

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