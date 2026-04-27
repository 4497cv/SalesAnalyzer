"""
nlp_utils.py
Utilidades compartidas entre los scripts de NLP del directorio AI/.

  _mock_datasets()   workaround para el bloqueo de pyarrow.dataset en Windows
  iter_sessions()    itera los mensajes_processed.txt del corpus
  load_messages()    lee (author, texto_normalizado) de un archivo de sesion
"""

import os
import sys
import types
import importlib.machinery
from unittest.mock import MagicMock


def mock_datasets():
    """
    En algunos entornos Windows, pyarrow.dataset usa una DLL bloqueada por
    Application Control. Como solo hacemos inferencia (no entrenamiento),
    mockeamos el modulo antes de que transformers lo intente cargar.
    Debe llamarse antes de cualquier import de transformers/pysentimiento.
    """
    def _make_mod(name):
        mod = types.ModuleType(name)
        mod.__spec__ = importlib.machinery.ModuleSpec(name, None)
        mod.__path__ = []
        mod.__package__ = name
        return mod

    datasets_mod = _make_mod("datasets")
    datasets_mod.Dataset = MagicMock
    datasets_mod.DatasetDict = MagicMock
    sys.modules["datasets"] = datasets_mod

    for name in [
        "datasets.arrow_dataset", "datasets.features", "datasets.formatting",
        "datasets.iterable_dataset", "datasets.info", "datasets.splits",
        "datasets.utils", "pyarrow.dataset",
    ]:
        sys.modules.setdefault(name, _make_mod(name))


def iter_sessions(corpus_dir: str):
    """Yields (client, date, filepath) para cada mensajes_processed.txt del corpus."""
    for client in sorted(os.listdir(corpus_dir)):
        client_path = os.path.join(corpus_dir, client)
        if not os.path.isdir(client_path):
            continue
        for session in sorted(os.listdir(client_path)):
            session_path = os.path.join(client_path, session)
            if not os.path.isdir(session_path):
                continue
            fp = os.path.join(session_path, "mensajes_processed.txt")
            if os.path.exists(fp):
                yield client, session, fp


def load_messages(filepath: str, normalize_fn) -> list[tuple[str, str]]:
    """
    Lee un mensajes_processed.txt y retorna lista de (author, texto_normalizado).
    Los mensajes que quedan vacios despues de normalizar se descartan.
    """
    from preprocess import extract_author_text
    messages = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            author, text = extract_author_text(line)
            text = normalize_fn(text)
            if text:
                messages.append((author, text))
    return messages
