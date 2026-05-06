# SalesAnalyzer

Herramienta de análisis de chats de ventas exportados de WhatsApp. Preprocesa los mensajes, construye un corpus estructurado y genera representaciones vectoriales (Bag of Words, TF-IDF) para analizar similitud entre conversaciones.

## Estructura del proyecto

```
SalesAnalyzer/
├── chat exports/        # Exportaciones de WhatsApp (.zip o .txt)
├── corpus/              # Corpus generado por build_corpus.py
│   └── {cliente}/
│       └── {fecha}/
│           ├── mensajes.txt
│           └── mensajes_processed.txt
├── output/              # Matrices generadas (CSV)
├── build_corpus.py      # Organiza los chats exportados en el corpus
├── preprocess.py        # Limpieza y normalización de mensajes
├── bagofwords.py        # Vectorización y matrices de distancia
├── trie.py              # Estructura Trie con diccionario en español
└── workspace.py         # Gestión de rutas del proyecto
```

## Pipeline

```
chat exports/ → build_corpus.py → corpus/ → preprocess.py → bagofwords.py → output/
```

### 1. `build_corpus.py`
Lee los archivos `.txt` o `.zip` de la carpeta `chat exports/` y organiza los mensajes por cliente y fecha en `corpus/{cliente}/{fecha}/mensajes.txt`.

### 2. `preprocess.py`
Normaliza cada `mensajes.txt` (errores tipográficos, puntuación, bigramas) y valida las palabras contra el Trie. Genera `mensajes_processed.txt` con el formato `autor:texto`.

### 3. `bagofwords.py`
Lee los archivos `mensajes_processed.txt` del corpus y genera en `output/`:

| Archivo | Descripción |
|---|---|
| `bow_matrix_binary.csv` | Bag of Words binario (0/1) |
| `bow_matrix_count.csv` | Bag of Words por frecuencia |
| `tf_idf_matrix.csv` | Matriz TF-IDF |
| `cosine_dist_matrix.csv` | Distancia coseno entre documentos |
| `euclidean_dist_matrix.csv` | Distancia euclidiana entre documentos |

Cada fila del DataFrame representa una sesión (`cliente/fecha`).

## Dependencias

```
pandas
numpy
nltk
wordfreq
word_forms
```

Instalar:
```bash
pip install pandas numpy nltk wordfreq word_forms
```

Descargar recursos de NLTK:
```python
import nltk
nltk.download('stopwords')
```

## Uso

```bash
# 1. Colocar exportaciones en chat exports/ y construir el corpus
python build_corpus.py

# 2. Preprocesar los mensajes
python preprocess.py

# 3. Generar matrices
python bagofwords.py
```
