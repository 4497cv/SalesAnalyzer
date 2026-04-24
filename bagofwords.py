import os
import pandas as pd
import re
from numpy import dot
from numpy.linalg import norm
import numpy as np
import math
import workspace
from nltk.corpus import stopwords
stop_es = stopwords.words('spanish')
from trie import *

trie = Trie("es", 50000)
local_stopwords = {'lupita', 'alejandra', 'mensaje', 
                 'sinali', 'zuleika', 'sofia', 'neftali', 'karla', 'aa', 'aah', 'ah', 'ahhh', 'ahh','alejandrapermagrafgmailcom',
                 'ale', 'alejanda', 'alejandrapermagrafgmailcom', 'rossy', 'rosy', 'rosi', 'rosario', 'rui',
                 'zuelika', 'zuleica', 'carla', 'kharely', 'oriana', 'comercios', 'unidos'}

def euclidean_distance(vect_1, vect_2):
    diff = np.array(vect_1) - np.array(vect_2)
    return np.sqrt(np.sum(diff**2))


def cosine_similarity(vect_1, vect_2):
    return dot(vect_1, vect_2) / (norm(vect_1) * norm(vect_2))


def cosine_distance(vect_1, vect_2):
    return 1 - cosine_similarity(vect_1, vect_2)


def process_euclidean_distance_matrix(bow_df) -> None:
    N = bow_df.shape[0]
    eucl_matrix = np.zeros((N, N))
    vectors = bow_df.values

    for i in range(N):
        for j in range(N):
            eucl_matrix[i, j] = euclidean_distance(vectors[i], vectors[j])

    documents_list = bow_df.index.tolist()
    eucl_df = pd.DataFrame(eucl_matrix, index=documents_list, columns=documents_list)

    output_path = workspace.get_output_path()
    eucl_df.to_csv(os.path.join(output_path, "euclidean_dist_matrix.csv"), encoding="utf-8")


def process_cosine_distance_matrix(bow_df) -> None:
    N = bow_df.shape[0]
    cos_mat = np.zeros((N, N))
    vectors = bow_df.values

    for i in range(N):
        for j in range(N):
            cos_mat[i, j] = cosine_distance(vectors[i], vectors[j])

    documents_list = bow_df.index.tolist()
    cos_df = pd.DataFrame(cos_mat, index=documents_list, columns=documents_list)

    output_path = workspace.get_output_path()
    cos_df.to_csv(os.path.join(output_path, "cosine_dist_matrix.csv"), encoding="utf-8")


def pre_process_word(word: str) -> str:
    word = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]', '', word)
    return word.lower()


def _iter_processed_files():
    """Yields (client_name, file_path) for every mensajes_processed.txt in the corpus."""
    corpus_dir = workspace.get_corpus_path()
    for client in os.listdir(corpus_dir):
        client_path = os.path.join(corpus_dir, client)
        if not os.path.isdir(client_path):
            continue
        for session in os.listdir(client_path):
            session_path = os.path.join(client_path, session)
            if not os.path.isdir(session_path):
                continue
            file_path = os.path.join(session_path, "mensajes_processed.txt")
            if os.path.exists(file_path):
                yield client, file_path


def _extract_text(line: str) -> str:
    """Returns only the message text from a 'author:text' line."""
    parts = line.split(":", 1)
    return parts[1] if len(parts) > 1 else ""

def eliminar_stopwords(text):
    stopwords = {'lupita', 'alejandra', 'mensaje', 
                 'sinali', 'zuleika', 'sofia', 'neftali', 'auxcomprasvisioncleamcom',
                 'betzavel', 'betzabel', 'chiniza'}
    

def process_vocabulary(vocab_lim=500) -> set:
    """
    Builds vocabulary from all mensajes_processed.txt files in the corpus.

    Parameters:
        vocab_lim: maximum vocabulary size

    Return:
        set of words
    """
    vocabulary = set()

    for _, file_path in _iter_processed_files():
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                text = _extract_text(line.strip())
                for word in text.split():
                    if len(word) > 1:
                        word = pre_process_word(word)
                        if(word.isalpha()) and\
                          (len(word) > 1) and\
                          (word not in stop_es) and\
                          (word not in local_stopwords):
                            vocabulary.add(word)
                            if len(vocabulary) >= vocab_lim:
                                return vocabulary

    return vocabulary


def process_bag_of_words(vocabulary: set, type="binary") -> None:
    """
    Generates a bag of words where each document is one client (all sessions combined).
    Stores result in output/bow_matrix_{type}.csv.

    Parameters:
        vocabulary: set of words
        type: "binary" or "count"

    Return:
        None
    """
    vocab_list = sorted(list(vocabulary))
    bow_matrix = []
    doc_names = []

    for client, file_path in _iter_processed_files():
        session = os.path.basename(os.path.dirname(file_path))
        doc_name = f"{client}/{session}"
        print(f"processing {doc_name}")
        bow = {word: 0 for word in vocabulary}

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                for word in _extract_text(line.strip()).split():
                    if len(word) > 1:
                        word = pre_process_word(word)
                        if word in bow:
                            if type == "binary":
                                bow[word] = 1
                            else:
                                bow[word] += 1

        bow_matrix.append([bow[w] for w in vocab_list])
        doc_names.append(doc_name)

    bag_of_words_df = pd.DataFrame(bow_matrix, columns=vocab_list, index=doc_names)
    output_path = workspace.get_output_path()
    bag_of_words_df.to_csv(os.path.join(output_path, f"bow_matrix_{type}.csv"), encoding="utf-8")


def process_tf_idf(bow_df) -> None:
    """
    Generates TF-IDF matrix from a BoW DataFrame and stores it in output/tf_idf_matrix.csv.

    Parameters:
        bow_df: pandas DataFrame (count BoW)

    Return:
        None
    """
    idf = {}
    tfidf_matrix = []
    N = bow_df.shape[0]
    df = (bow_df > 0).sum(axis=0)

    for word in bow_df.columns:
        idf[word] = math.log(N / (1 + df[word]))

    for _, row in bow_df.iterrows():
        total_words = row.sum()
        tfidf_row = []
        for word in bow_df.columns:
            tf = row[word] / total_words if total_words > 0 else 0
            tfidf_row.append(tf * idf[word])
        tfidf_matrix.append(tfidf_row)

    tfidf_df = pd.DataFrame(tfidf_matrix, index=bow_df.index, columns=bow_df.columns)
    output_path = workspace.get_output_path()
    tfidf_df.to_csv(os.path.join(output_path, "tf_idf_matrix.csv"), encoding="utf-8")


def __main__():
    workspace.set_workspace_path(os.path.dirname(os.path.abspath(__file__)))

    vocabulary = process_vocabulary(vocab_lim=100000)

    process_bag_of_words(vocabulary, "binary")
    bow_b_df = pd.read_csv(os.path.join(workspace.get_output_path(), "bow_matrix_binary.csv"), index_col=0)

    process_bag_of_words(vocabulary, "count")
    bow_c_df = pd.read_csv(os.path.join(workspace.get_output_path(), "bow_matrix_count.csv"), index_col=0)

    process_tf_idf(bow_c_df)
    process_cosine_distance_matrix(bow_b_df)
    process_euclidean_distance_matrix(bow_b_df)


__main__()
