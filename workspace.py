
import os
import sys

workspace_path = os.path.dirname(os.path.abspath(__file__))
key_path = ""
articles_path = ""
texts_path = ""

def set_workspace_path(path, debug = 0):
    global workspace_path
    if(os.path.exists(path)):
        workspace_path = path
        if(debug): print("set new workspace: %s" % path)
    else:
        print(">> ERROR: Path does not exist: %s" % path)
        sys.exit()   

def get_workspace_path() -> str:
    global workspace_path
    return workspace_path

def get_guardian_key_path():
    global key_path, workspace_path
    key_path = os.path.join(workspace_path, "cfg", "guardian_key.txt")
    if(os.path.exists(key_path)):
        return key_path
    else:
        print(">> ERROR: Guardian key was not found in %s" % key_path)
        sys.exit()

def get_articles_path(debug = 0):
    global articles_path, workspace_path
    articles_path = os.path.join(workspace_path, "temp","guardian", "articles")

    if(os.path.exists(articles_path)):
        if(debug): print("Path exists for articles %s" % articles_path)
    else:
        if(debug): print("New path created for articles %s" % articles_path)
        os.makedirs(articles_path, exist_ok=True)

    return articles_path

def get_texts_path(debug = 0):
    global texts_path, workspace_path
    texts_path = os.path.join(workspace_path, "temp","guardian", "texts")

    if(os.path.exists(texts_path)):
        if(debug): print("Path exists for articles %s" % texts_path)
    else:
        if(debug): print("New path created for articles %s" % texts_path)
        os.makedirs(texts_path, exist_ok=True)

    return texts_path

def get_corpus_path(debug = 0):
    global workspace_path
    corpus_path = os.path.join(workspace_path, "corpus")

    if(os.path.exists(corpus_path)):
        if(debug): print("Path exists for corpus %s" % corpus_path)
    else:
        if(debug): print("New path created for corpus %s" % corpus_path)
        os.makedirs(corpus_path, exist_ok=True)

    return corpus_path

def get_chat_exports(debug = 0):
    global workspace_path
    corpus_path = os.path.join(workspace_path, "chat exports")

    if(os.path.exists(corpus_path)):
        if(debug): print("Path exists for corpus %s" % corpus_path)
    else:
        if(debug): print("New path created for corpus %s" % corpus_path)
        os.makedirs(corpus_path, exist_ok=True)

    return corpus_path

def get_output_path(debug = 0):
    global workspace_path
    output_path = os.path.join(workspace_path, "output")

    if(os.path.exists(output_path)):
        if(debug): print("Path exists for output %s" % output_path)
    else:
        if(debug): print("New path created for output %s" % output_path)
        os.makedirs(output_path, exist_ok=True)

    return output_path