import importlib.util
import os
import textwrap


def importar_modulo(caminho: str):
    """Importa um módulo a partir de um caminho de arquivo."""
    spec = importlib.util.spec_from_file_location("run", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def executar_teste(caminho_teste: str):
    """Executa o teste especificado pelo módulo run.py."""
    if os.path.isfile(caminho_teste):
        modulo_teste = importar_modulo(caminho_teste)

        if hasattr(modulo_teste, "main"):
            modulo_teste.main()


def print_enunciado(caminho_enunciado: str):
    with open(caminho_enunciado, "r", encoding="utf-8") as file:
        conteudo = file.read()

    print(textwrap.fill(conteudo, width=80), "\n")
