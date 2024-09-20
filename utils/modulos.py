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


def print_table(data_dict):
    comprimentos = []
    for row in data_dict:
        val_lengths = [len(str(item)) for item in row.values()]
        col_lengths = [len(str(item)) for item in row.keys()]
        max_lengths = [
            max(val_len, col_len) for val_len, col_len in zip(val_lengths, col_lengths)
        ]
        comprimentos.append(max_lengths)

    max_comprimentos = [max(col_lengths) for col_lengths in zip(*comprimentos)]

    colunas = list(data_dict[0].keys())

    header_row = " | ".join(
        f"{col:{max_comprimentos[i]}}" for i, col in enumerate(colunas)
    )
    print(header_row)
    print("-" * len(header_row))

    for row in data_dict:
        row_data = " | ".join(
            f"{str(val):{max_comprimentos[i]}}" for i, val in enumerate(row.values())
        )
        print(row_data)
