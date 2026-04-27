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
    # Patrones fonéticos: trabajan dentro de palabras, sin \b
    texto = re.sub(r'phasta', 'hasta', texto)
    texto = re.sub(r'pha', 'pa', texto)
    texto = re.sub(r'phe', 'pe', texto)
    texto = re.sub(r'phi', 'pi', texto)
    texto = re.sub(r'pho', 'po', texto)
    texto = re.sub(r'phu', 'pu', texto)
    texto = re.sub(r'lha', 'la', texto)
    texto = re.sub(r'lhe', 'le', texto)
    texto = re.sub(r'lhi', 'li', texto)
    texto = re.sub(r'lho', 'lo', texto)
    texto = re.sub(r'lhu', 'lu', texto)
    texto = re.sub(r'kha', 'ka', texto)
    texto = re.sub(r'khe', 'ke', texto)
    texto = re.sub(r'khi', 'ki', texto)
    texto = re.sub(r'kho', 'ko', texto)
    texto = re.sub(r'khu', 'ku', texto)
    # Palabras completas con \b
    texto = re.sub(r'\bke\b', 'que', texto)
    texto = re.sub(r'\bcub\.', 'cubierta', texto)
    texto = re.sub(r'\bsr\b', 'señor', texto)
    texto = re.sub(r'\bokok\b', 'ok', texto)
    texto = re.sub(r'\bokrok\b', 'ok', texto)
    texto = re.sub(r'\bokis\b', 'ok', texto)
    texto = re.sub(r'\boky\b', 'ok', texto)
    texto = re.sub(r'\bokk\b', 'ok', texto)
    texto = re.sub(r'\bokd\b', 'ok', texto)
    texto = re.sub(r'\boki\b', 'ok', texto)
    texto = re.sub(r'\boks\b', 'ok', texto)
    texto = re.sub(r'\bokoiki\b', 'ok', texto)
    texto = re.sub(r'\bgrs\b', 'gracias', texto)
    texto = re.sub(r'\bgraciasss\b', 'gracias', texto)
    texto = re.sub(r'gracia a', 'gracias a ti', texto)
    texto = re.sub(r'\bgracia\b', 'gracias', texto)
    texto = re.sub(r'\bgrax\b', 'gracias', texto)
    texto = re.sub(r'\bgracuas\b', 'gracias', texto)
    texto = re.sub(r'\bgraccias\b', 'gracias', texto)
    texto = re.sub(r'\bgracoas\b', 'gracias', texto)
    texto = re.sub(r'\bgravias\b', 'gracias', texto)
    texto = re.sub(r'\bpulgracias\b', 'gracias', texto)
    texto = re.sub(r'\bpagracias\b', 'gracias', texto)
    texto = re.sub(r'\bntp\b', 'no te preocupes', texto)
    texto = re.sub(r'\bola\b', 'hola', texto)
    texto = re.sub(r'\bholis\b', 'hola', texto)
    texto = re.sub(r'\bpzas\b', 'piezas', texto)
    texto = re.sub(r'\bpzs\b', 'piezas', texto)
    texto = re.sub(r'\bpz\b', 'piezas', texto)
    texto = re.sub(r'\bpiezasa\b', 'piezas', texto)
    texto = re.sub(r'\bcomplmentos\b', 'complementos', texto)
    texto = re.sub(r'\bnuevamanete\b', 'nuevamente', texto)
    texto = re.sub(r'\bqui\b', 'que', texto)
    texto = re.sub(r'\bati\b', 'a ti', texto)
    texto = re.sub(r'\baty\b', 'a ti', texto)
    texto = re.sub(r'\bti,', 'a ti,', texto)
    texto = re.sub(r'\bondas\b', 'onda', texto)
    texto = re.sub(r'\blavoraste\b', 'laboraste', texto)
    texto = re.sub(r'\bbbuenas\b', 'buenas', texto)
    texto = re.sub(r'\buenas\b', 'buenas', texto)
    texto = re.sub(r'\bjesusi\b', 'jesus', texto)
    texto = re.sub(r'\bpork\b', 'porque', texto)
    texto = re.sub(r'\bxk\b', 'porque', texto)
    texto = re.sub(r'\basii\b', 'así', texto)
    texto = re.sub(r'\basi\b', 'así', texto)
    texto = re.sub(r'\bnop\b', 'no', texto)
    texto = re.sub(r'\bpasare\b', 'pasaré', texto)
    texto = re.sub(r'\beconomicas\b', 'económicas', texto)
    texto = re.sub(r'\bmas\b', 'más', texto)
    texto = re.sub(r'\basta\b', 'hasta', texto)
    texto = re.sub(r'\bud\b', 'usted', texto)
    texto = re.sub(r'\bpongame\b', 'póngame', texto)
    texto = re.sub(r'\baqui\b', 'aquí', texto)
    texto = re.sub(r'\bdiosas\b', 'dios', texto)
    texto = re.sub(r'\boyes\b', 'oye', texto)
    texto = re.sub(r'\boie\b', 'oye', texto)
    texto = re.sub(r'\bsrita\b', 'señorita', texto)
    texto = re.sub(r'\bporfavorvor\b', 'porfavor', texto)
    texto = re.sub(r'\bsirfavor\b', 'porfavor', texto)
    texto = re.sub(r'\bporfa\b', 'porfavor', texto)
    texto = re.sub(r'\bxfa\b', 'porfavor', texto)
    texto = re.sub(r'por fas', 'porfavor', texto)
    texto = re.sub(r'por favor', 'porfavor', texto)
    texto = re.sub(r'por fa', 'porfavor', texto)
    texto = re.sub(r'\btmb\b', 'también', texto)
    texto = re.sub(r'\bik\b', 'y que', texto)
    texto = re.sub(r'\boc\b', 'orden de compra', texto)
    texto = re.sub(r'\bnc\b', 'nota de credito', texto)
    texto = re.sub(r'\btc\b', 'tarjeta de credito', texto)
    texto = re.sub(r'\bfacturaturitas\b', 'facturas', texto)
    texto = re.sub(r'\bfacturaturar\b', 'facturar', texto)
    texto = re.sub(r'\bfacturature\b', 'factura', texto)
    texto = re.sub(r'\bfacturaturo\b', 'facturo', texto)
    texto = re.sub(r'\bfacturatura\b', 'factura', texto)
    texto = re.sub(r'\bfac\b', 'factura', texto)
    texto = re.sub(r'\bgad\b', 'gracias a dios', texto)
    texto = re.sub(r'\bbdias\b', 'buenos dias', texto)
    texto = re.sub(r'\bbdia\b', 'buen día', texto)
    texto = re.sub(r'buen dia', 'buen día', texto)
    texto = re.sub(r'\bandjunto\b', 'adjunto', texto)
    texto = re.sub(r'\baorita\b', 'ahorita', texto)
    texto = re.sub(r'\bahpraita\b', 'ahorita', texto)
    texto = re.sub(r'\borita\b', 'ahorita', texto)
    texto = re.sub(r'\bvd\b', 'verdad', texto)
    texto = re.sub(r'\babra\b', 'habra', texto)
    texto = re.sub(r'\bagregharemos\b', 'agregaremos', texto)
    texto = re.sub(r'\baleajandra\b', 'alejandra', texto)
    texto = re.sub(r'\bbieb\b', 'bien', texto)
    texto = re.sub(r'\bbienn\b', 'bien', texto)
    texto = re.sub(r'\bbnien\b', 'bien', texto)
    texto = re.sub(r'\bcres\b', 'crees', texto)
    texto = re.sub(r'\bcuanrto\b', 'cuanto', texto)
    texto = re.sub(r'\bdomucilio\b', 'domicilio', texto)
    texto = re.sub(r'\bsipis\b', 'si', texto)
    texto = re.sub(r'\bsip\b', 'si', texto)
    texto = re.sub(r'\bsio\b', 'si', texto)
    texto = re.sub(r'\bsiii\b', 'si', texto)
    texto = re.sub(r'\bsii\b', 'si', texto)
    texto = re.sub(r'\bsimilhares\b', 'similares', texto)
    texto = re.sub(r'\bshabra\b', 'sabra', texto)
    texto = re.sub(r'\bsustitua\b', 'sustituya', texto)
    texto = re.sub(r'\bxfis\b', 'por favor', texto)
    texto = re.sub(r'\byaaaaa\b', 'ya', texto)
    texto = re.sub(r'\bvidaaaaa\b', 'vida', texto)
    texto = re.sub(r'\bplastoco\b', 'plastico', texto)
    texto = re.sub(r'\bviendop\b', 'viendo', texto)
    texto = re.sub(r'\bhh\b', 'h', texto)
    texto = re.sub(r'\bkh\b', 'k', texto)
    texto = re.sub(r'\bquew\b', 'que', texto)
    texto = re.sub(r'\bimg\b', 'imagen', texto)
    texto = re.sub(r'\baña\b', 'año', texto)
    texto = re.sub(r'\bpaq\b', 'paquete', texto)
    texto = re.sub(r'\brevisin\b', 'revision', texto)
    texto = re.sub(r'\bremisin\b', 'remision', texto)
    texto = re.sub(r'\bvisin\b', 'vision', texto)
    texto = re.sub(r'\bsomn\b', 'son', texto)
    texto = re.sub(r'\bsonj\b', 'son', texto)
    texto = re.sub(r'\bmañona\b', 'mañana', texto)
    texto = re.sub(r'\bacjas\b', 'cajas', texto)
    texto = re.sub(r'\bquie\b', 'que', texto)
    texto = re.sub(r'\bqueres\b', 'quieres', texto)
    texto = re.sub(r'\bqueren\b', 'quieren', texto)
    texto = re.sub(r'\bquere\b', 'quiere', texto)
    texto = re.sub(r'\bqueras\b', 'quieras', texto)
    texto = re.sub(r'\bquera\b', 'quiera', texto)
    texto = re.sub(r'\bquero\b', 'quiero', texto)
    texto = re.sub(r'\bestass\b', 'estas', texto)
    texto = re.sub(r'\besya\b', 'esta', texto)
    texto = re.sub(r'\belsta\b', 'esta', texto)
    texto = re.sub(r'\bps\b', 'pues', texto)
    texto = re.sub(r'\becho\b', 'hecho', texto)
    texto = re.sub(r'\bare\b', 'haré', texto)
    texto = re.sub(r'\bproximo\b', 'próximo', texto)
    texto = re.sub(r'\bcu\b', 'cada una', texto)
    texto = re.sub(r'\bunaanto\b', 'cuanto', texto)
    texto = re.sub(r'\bytu\b', 'y tu', texto)
    texto = re.sub(r'\baun\b', 'aún', texto)
    texto = re.sub(r'\bpodia\b', 'podía', texto)
    texto = re.sub(r'\bpodra\b', 'podrá', texto)
    texto = re.sub(r'\bllegarian\b', 'llegarían', texto)
    texto = re.sub(r'\bllegaria\b', 'llegaría', texto)
    texto = re.sub(r'\benvies\b', 'envíes', texto)
    texto = re.sub(r'\benvias\b', 'envías', texto)
    texto = re.sub(r'\benvio\b', 'envío', texto)
    texto = re.sub(r'\berann\b', 'eran', texto)
    texto = re.sub(r'\bseran\b', 'serán', texto)
    texto = re.sub(r'\bpence\b', 'pensé', texto)
    texto = re.sub(r'\bmandamelo\b', 'mándamelo', texto)
    texto = re.sub(r'\bmandame\b', 'mándame', texto)
    texto = re.sub(r'\bnetro\b', 'neto', texto)
    texto = re.sub(r'\bsalocitar\b', 'solicitar', texto)
    texto = re.sub(r'\bagreagar\b', 'agregar', texto)
    texto = re.sub(r'\bagregharemos\b', 'agregaremos', texto)
    texto = re.sub(r'\bunaal\b', 'una', texto)
    texto = re.sub(r'\bapieza\b', 'una pieza', texto)
    texto = re.sub(r'what app', 'whatsapp', texto)
    texto = re.sub(r'\bimprimi\b', 'imprimí', texto)
    texto = re.sub(r'\bsubi\b', 'subí', texto)
    texto = re.sub(r'\bbiolencia\b', 'violencia', texto)
    texto = re.sub(r'\bremision\b', 'remisión', texto)
    texto = re.sub(r'\bguia\b', 'guía', texto)
    texto = re.sub(r'\bquen\b', 'quien', texto)
    texto = re.sub(r'\bquien\b', 'quién', texto)
    texto = re.sub(r'\bpal\b', 'para', texto)
    texto = re.sub(r'\besquela\b', 'escuela', texto)
    texto = re.sub(r'\besperhar[eé]\b', 'esperaré', texto)
    texto = re.sub(r'\besperhar\b', 'esperar', texto)
    texto = re.sub(r'\bcotice\b', 'coticé', texto)
    texto = re.sub(r'\bcuanto\b', 'cuánto', texto)
    texto = re.sub(r'\bcuantas\b', 'cuántas', texto)
    texto = re.sub(r'\bcuantos\b', 'cuántos', texto)
    texto = re.sub(r'\bacrilico\b', 'acrílico', texto)
    texto = re.sub(r'\brazon\b', 'razón', texto)
    texto = re.sub(r'\bmerida\b', 'mérida', texto)
    texto = re.sub(r'\bperdon\b', 'perdón', texto)
    texto = re.sub(r'\bdioso\b', 'dios', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bpagaria\b', 'pagaría', texto)
    texto = re.sub(r'con ña', 'con la', texto)
    texto = re.sub(r'\beh\b', 'he', texto)
    texto = re.sub(r'\bplimas\b', 'plumas', texto)
    texto = re.sub(r'\bhunmedas\b', 'húmedas', texto)
    texto = re.sub(r'\balguos\b', 'algunos', texto)
    texto = re.sub(r'\bcotizacion\b', 'cotización', texto)
    texto = re.sub(r'\bpregunte\b', 'pregunté', texto)
    texto = re.sub(r'\blapiz\b', 'lápiz', texto)
    texto = re.sub(r'carpetade de', 'carpeta de', texto)
    texto = re.sub(r'\bjjaja\b', 'jaja', texto)
    texto = re.sub(r'\bgenerico\b', 'genérico', texto)
    texto = re.sub(r'\bsabado\b', 'sábado', texto)
    texto = re.sub(r'\brebice\b', 'revisé', texto)
    texto = re.sub(r'\brevise\b', 'revisé', texto)
    texto = re.sub(r'\bjrje\b', 'jeje', texto)
    texto = re.sub(r'\bbtardes\b', 'buenas tardes', texto)
    texto = re.sub(r'\bsholamente\b', 'solamente', texto)
    texto = re.sub(r'<se editó este mensaje\.>', '', texto)
    texto = re.sub(r'\baya\b', 'allá', texto)
    texto = re.sub(r'\bnomnre\b', 'nombre', texto)
    texto = re.sub(r'\bnuevp\b', 'nuevo', texto)
    texto = re.sub(r'(\d)([a-záéíóúüñ])', r'\1 \2', texto)
    texto = re.sub(r'([a-záéíóúüñ])(\d)', r'\1 \2', texto)
    #texto = re.sub(r'[áéíóúñ]', lambda m: {'á':'a','é':'e','í':'i','ó':'o','ú':'u', 'ñ':'n'}[m.group()], texto)

    return texto

def normalizacion_nombres(texto):
    texto = texto.replace("aleajandra", "alejandra")
    texto = texto.replace("aleajandra", "alejanda")
    texto = texto.replace("kharely", "karely")
    texto = texto.replace("kharély", "karely")
    texto = texto.replace("rossy", "rosy")
    texto = texto.replace("betzavel", "betzabel")
    texto = texto.replace("zuleika", "zuleica")
    texto = texto.replace("zuelika", "zuleica")
    texto = texto.replace("casandra", "cassandra")
    texto = texto.replace("ka tia", "katia")
    texto = texto.replace("cerlox", "xerox")
    texto = texto.replace("victorio", "victoria")
    texto = texto.replace("scoch", "scotch")
    texto = texto.replace("postis", "post it")
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