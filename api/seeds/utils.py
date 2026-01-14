import json
import os
import glob
from django.conf import settings


def get_json_data(filename):
    """
    Lê um arquivo JSON da pasta api/docs/ e retorna os dados.
    """
    docs_path = os.path.join(settings.BASE_DIR, "docs")
    file_path = os.path.join(docs_path, filename)

    if not os.path.exists(file_path):
        print(f"Warning: File not found: {file_path}")
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_files_by_pattern(pattern):
    """
    Retorna lista de caminhos do sistema de arquivos na pasta docs que correspondam ao padrão.
    """
    docs_path = os.path.join(settings.BASE_DIR, "api", "docs")
    return glob.glob(os.path.join(docs_path, pattern))


def parse_attributes(attr_array):
    """
    Converte o array [For, Agi, Int, Von] do JSON para um dict.
    """
    if not attr_array or len(attr_array) < 4:
        return {"strength": 0, "agility": 0, "intelligence": 0, "will": 0}

    return {
        "strength": attr_array[0],
        "agility": attr_array[1],
        "intelligence": attr_array[2],
        "will": attr_array[3],
    }


def parse_requirements(req_array):
    """
    Transforma o array de requisitos do JSON (ex: ['n', 5, 'h', ['X']]) em texto legível.
    """
    if not req_array or not isinstance(req_array, list):
        return ""

    texts = []
    i = 0
    while i < len(req_array):
        tag = req_array[i]
        val = req_array[i + 1] if i + 1 < len(req_array) else None

        if tag == "n":
            # Geralmente Nível ou Atributo Base
            texts.append(f"Valor {val}")
            i += 2
        elif tag == "h":
            # Requisito de Habilidade(s)
            if isinstance(val, list):
                habs = ", ".join(val)
                texts.append(f"Habilidade: {habs}")
            else:
                texts.append(f"Habilidade: {val}")
            i += 2
        elif tag == "a":
            # Atributo
            texts.append(f"Atributo: {val}")
            i += 2
        else:
            # Fallback
            texts.append(str(tag))
            i += 1

    return "; ".join(texts)


def strip_html_tags(text):
    """
    Remove tags HTML e entidades comuns como &emsp;
    """
    if not text or not isinstance(text, str):
        return text

    import re

    # Remove tags HTML
    clean = re.compile("<.*?>")
    text = re.sub(clean, "", text)

    # Remove entidades comuns
    text = text.replace("&emsp;", " ")
    text = text.replace("&nbsp;", " ")

    # Remove espaços duplos resultantes da limpeza
    text = re.sub(" +", " ", text)

    return text.strip()
