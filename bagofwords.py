import os
import pandas as pd
import re
from numpy import dot
from numpy.linalg import norm
import numpy as np
from collections import Counter
import workspace
from nltk.corpus import stopwords

stop_es = stopwords.words('spanish')

local_stopwords = {
    # Nombres propios
    'kharely', 'karely', 'kareli', 'lupita', 'alejandra', 'alejanda', 'aleajandra', 'ene', 'enel', 'joey', 'jones', 'jose', 'wilson', 'juan', 'junio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
    'mirna', 'oriana', 'casandra', 'sinali', 'sofia', 'neftali', 'cassandra', 'lupita', 'manny', 'maricel', 'briceida', 'byrmax',
    'karla', 'carla', 'silvia', 'dora', 'elia', 'betzavel', 'betzabel', 'carmen', 'lolis', 'michelle', 'cris', 'cristtel', 'elva', 'godoy', 'gloria', 'gonzalez', 'goo', 'hernandez', 'janel', 'lbel',
    'rossy', 'rosy', 'rosi', 'rosario', 'rui', 'zuleika', 'zuleica', 'zuelika', 'silva', 'adminelmaster', 'alo', 'am', 'ama', 'ay', 'axion', 'azo',
    'keyla', 'dora', 'ale', 'laura', 'pedro', 'maria', 'aracely', 'mari', 'raul', 'fabiola', 'tia', 'katia', 'andrea', 'lesli', 'victoria', 'vicbet', 'bic', 'victor', 'iker',
    'mari', 'sergio', 'elizabeth', 'patty', 'dios', 'alberto', 'angelita', 'ignacio', 'malu', 'armando', 'daniela', 'jaime', 'jesus', 'alicia', 'ivan', 'jafra', 'karley', 'katya', 'aracely', 'ramírez', 'raúl', 'bnoi',
    'ruiz', 'mary', 'key', 'natura', 'dixon', 'ndia', 'añitos', 
    # Empresas / vendedor
    'permagraf', 'comercios', 'unidos', 'chiniza', 'siam',  'acme', 'anzor', 'cd', 'cfdi', 'cfe', 'craft', 'cv', 'sa', 'de', 'dell', 'depot', 'hp', 'kirkland', 'kleenex', 'klinex', 'kores', 'kynera', 'rey', 'rfc', 'rh', 'rivales', 'roble',
    'auxcomprasvisioncleamcom', 'alejandrapermagrafgmailcom', 'lka', 'maped', 'ty',
    'olfa', '.com', 'mvictoriaagri-nova.com', 'xerox', 'google', 'bic', 'cedis', 'gmail', 'com', 'mexicofolio', 'ptt', 'wa', 'epson', 'ta', 'tallerelcapulehotmailcom', 'tc', 'tecniclik', 'tge', 'tijuana', 'tr', 'buu', 'bv', 'byd', 'byrmax'
    'permagrafgmail com', 'permagrafgmail', 'tallerelcapulehotmail', 'tallerelcapulehotmail com', 'pilot', 'kyma', 'pelikan', 'pritt', 'sharpie', 'carnes', 'gps', 'kinera', 'acco', 'azor', 'baco', 'ipad',
    'auxcomprasvisioncleamcom', 'auxiliardecontabilidadkarfulcom', 'bostitch', 'bostich', 'carlaequiposdeoficina', 'claudiapermagrafgmailcom', 'comprassistemasdeimpresioncom', 'karelyequiposdeoficina',
    'comprasvisioncleamcom', 'energizer', 'escolight', 'essential', 'esterbrook', 'estrada', 'etc', 'fa', 'fcdrsaa', 'fdw', 'febrero', 'fio', 'httpspedidosdeoficina', 'httpscusawebplacecommx', 'httpsmaps', 'ig', 'big',
    # IDs
    't1', 't2', 't4', 't5', 't6', 'ey', 'locker', 'lockers', 'lolys', 'lópez', 'losa', 'litro', 'lux', 'lv', 'mae', 'maily', 'malú', 'maskin', 'masking', 'maskng', 'mastografia', 'sukarne', 'yoyo', 'yeso', 'yuriana', 'zebra', 'xml', 'yucatán',
    # Apellidos
    'laso', 'roman', 'mora', 'paty', 'pc', 'pd', 'pedidosdeoficina', 'pedroinfante', 'pedro', 'infante', 'pentel', 'persme', 'ph', 'pilikan', 'pimp', 'pin', 'pins', 'pl', 'plis', 'rollerball', 'bolsas', 'bolsa',
    # Sistema WhatsApp
    'eliminaste', 'mensaje', 'eliminó', 'img', 'pdf', 'opus', 'stk', 'wa', 'webp', 'web', 'jpg', 'oz', 'padre', 'padrino', 'palicarias', 'sa', 'samsung', 'scotch', 'segosan', 'whatsapp', 'zapata', 'zoologico', 'wax', 'reogan',
    # Ruido
    'aa', 'aaa', 'aaaa', 'aah', 'ah', 'ahh', 'ahhh', 'jaja', 'jajaja', 'jajajaja', 'este', 'ok', '☺️', '...', '0⁰', 'jeje', 'jejeje', 'jajaj', 'oh', 'eh', 'oye', 'pa', 'shola', 'ingasu', 'cloralex', 'gatorades', 'admonferrelaminasgmailcom', 'platos', 'italiano', 'enrute', 'hombre', 'volverme', 'canica', 'canciones', 'desmadre',
    'buenooooo', 'buenoo', 'eh', 'eja', 'em', 'jaj', 'jajajaajajaja', 'jajajaajjaa', 'jajajaj', 'jajajajaa', 'jajajajaja', 'jajajajajaj', 'jajajajajaja', 'jajajajajajaja', 'jajajajajja', 'jajajajja', 'jajjaaaaa',
    'jejej', 'jejejej', 'jejejeje', 'jejejejeje', 'jejje', 'jesucursalristo', 'jfelixfconcreditocommx', 'jijij', 'jijijiji', 'porfa', 'delga', 'bacoflash', 'tares', 'vaga', 'cabos', 'blockcaja', 'italiana', 'pistaches', 'enero', 'vert', 'sujetos', 'miran',  'fuschia', 'block', 'alan', 'aeropuerto', 'aventuras', 'flojeras', 'rei', 'many', 'cojin', 'video', 'tranquila', 'manches', 'yeah', 'meneses'
    'sino', 'chanza', 'reponiendome', 'colgante', 'medicos', 'encierrame', 'santo', 'bailado', 'domingo', 'mirkahigueragmailcom', 'nosé', 'borbon', 'no', 'bb', 'trupper', 'son', 'sol', 'estrellas', 'arreglarme', 'ed', 'mochos', 'dps', 'desengrapadora', 'gises', 'mia', 'cincho',
    # saludos
    'buenos', 'días', 'día', 'buenas', 'tardes', 'hola', 'dia', 'gracias', 'muchas', 'bien', 'muy', 'hola', 'Qué onda', 'que onda', 'fis', 'foamy', 'francés', 'irale', 'iu', 'liquid', 'paper', 'texto',
    'buena tarde', 'buena', 'bueno', 'tarde', 'buen', 'buena', 'quedo', 'da', 'muchísimas', 'ayer', 'hoy', 'broches', 'toner', 'cutter', 'tinta', 'tintas',
    # palabras simpples
    'si', 'no', 'nose', 'pm', 'zas', 'qui', 'que', ' it', 'cf', 'mmm', 'mm', 'um', 'uh', 'aaah', 'an', 'do', 'lease', 'lefort', 'lesly', 'mejia', 'pro', 'correctores', 'corrector',
    # fechas
    'abril', 'negro', 'negra', 'rojo', 'azul', 'amarillo', 'café', 'niq', 'nissa', 'noel', 'niña', 'ofi', 'okidoki', 'okiiis', 'olguin', 'pues',
    #articulos
    'ecg', 'uñas', 'mfp', 'michel', 'mob', 'ms', 'mst', 'muchacha', 'muchacho',' muchachos', 'mx', 'mérida', 'ne', 'negofile', 'orian', 'pvcb', 'pvc', 'pz', 'pza', 'post it', 'block', 'post', 'it', 'bonito', 'fin', 'aquí', 'andamos', 'pasta', 'dura', 'cartón', 'cinta', 'canela', 'marca', 'textos', 'marcatextos', 'verde', 'cutter', 'fin', 'carpetas', 'hojas', 'blancas', 'cuadrados',
    # regionalismos
    'mija', 'onda', 'bendito', 'cañera', 'tomatera', 'dormilona', 'guapo', 'amor', 'cruda', 'mayo', 'member', 'members', 'navolato', 'aaracely', 'cómo', 
    # lugares
    'sanalona', 'culiacan', 'mazatlan', 'villas', 'estación', 'valle', 'alto', 'per', 'gbc', 'cm', 'guamuchil', 'hawian', 'free', 'venadillo', 'guasave', 'harpic', 'hdmi', 'humaya', 'basura', 'bolsas', 'bolsa',
    'mous', 'monitor', 'agua va', 'agua', 'va', 'equiposdeoficina',  'esco', 'beisbol', 'alas', 'cordón',
}

def pre_process_word(word):
    word = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]', '', word)
    word.lower()
    return word.lower()

def get_client_and_path():
    # obtenemos el cliente a partir de la lista del directorio del corpus
    for client in os.listdir(workspace.get_corpus_path()):
        # obtenemos la ruta del cliente
        client_path = os.path.join(workspace.get_corpus_path(), client)
        # verificamos que la ruta exista
        if not os.path.isdir(client_path):
            continue

        for session in os.listdir(client_path):
            # obtenemos la ruta de la sesion encontrada
            session_path = os.path.join(client_path, session)
            # verificamos si esta ruta es valida
            if not os.path.isdir(session_path):
                continue
            # obtenemos la ruta del archivo
            file_path = os.path.join(session_path, "mensajes_processed.txt")

            if os.path.exists(file_path):
                yield client, file_path


def _extract_text(line: str) -> str:
    """Returns only the message text from a 'author:text' line."""
    parts = line.split(":", 1)
    return parts[1] if len(parts) > 1 else ""
    

def process_vocabulary(vocab_lim=500, bigram_min_df=3):
    vocabulary = set()
    bigram_doc_freq = Counter()

    for _, file_path in get_client_and_path():
        doc_bigrams = set()
        with open(file_path, "r", encoding="utf-8-sig") as f:
            for line in f:
                tokens = []
                for word in _extract_text(line.strip()).split():
                    if len(word) > 1:
                        word = pre_process_word(word)
                        if word.isalpha() and len(word) > 1 \
                                and word not in stop_es \
                                and word not in local_stopwords:
                            vocabulary.add(word)
                            tokens.append(word)
                for i in range(len(tokens) - 1):
                    doc_bigrams.add(f"{tokens[i]} {tokens[i+1]}")
        for bg in doc_bigrams:
            bigram_doc_freq[bg] += 1

    for bg, df in bigram_doc_freq.most_common():
        if df < bigram_min_df:
            break
        vocabulary.add(bg)

    if len(vocabulary) > vocab_lim:
        unigrams = {v for v in vocabulary if ' ' not in v}
        top_bigrams = []
        for bg, _ in bigram_doc_freq.most_common():
            if bigram_doc_freq[bg] >= bigram_min_df:
                top_bigrams.append(bg)
        limit = max(0, vocab_lim - len(unigrams))
        vocabulary = unigrams | set(top_bigrams[:limit])

    return vocabulary


def process_bag_of_words(vocabulary, type="binary"):
    vocab_list = sorted(list(vocabulary))
    has_bigrams = False
    for v in vocabulary:
        if ' ' in v:
            has_bigrams = True
            break
    bow_matrix = []
    doc_names = []

    for client, file_path in get_client_and_path():
        session = os.path.basename(os.path.dirname(file_path))
        doc_name = f"{client}/{session}"
        print(f"processing {doc_name}")
        bow = {word: 0 for word in vocabulary}

        with open(file_path, "r", encoding="utf-8-sig") as f:
            for line in f:
                tokens = []
                for word in _extract_text(line.strip()).split():
                    if len(word) > 1:
                        w = pre_process_word(word)
                        if not w.isalpha() or len(w) <= 1:
                            continue
                        if w in bow:
                            if type == "binary":
                                bow[w] = 1
                            else:
                                bow[w] += 1
                        if w not in stop_es and w not in local_stopwords:
                            tokens.append(w)

                if has_bigrams:
                    for i in range(len(tokens) - 1):
                        bg = f"{tokens[i]} {tokens[i+1]}"
                        if bg in bow:
                            if type == "binary":
                                bow[bg] = 1
                            else:
                                bow[bg] += 1

        bow_matrix.append([bow[w] for w in vocab_list])
        doc_names.append(doc_name)

    bag_of_words_df = pd.DataFrame(bow_matrix, columns=vocab_list, index=doc_names)
    output_path = workspace.get_output_path()
    bag_of_words_df.to_csv(os.path.join(output_path, f"bow_matrix_{type}.csv"), encoding="utf-8-sig")

def run():
    # crear el vocabulario en base a todos los mensajes del corpus
    vocabulary = process_vocabulary(vocab_lim=100000, bigram_min_df=3)
    # generar bag of words a partir del vocabulario
    process_bag_of_words(vocabulary, "count")
