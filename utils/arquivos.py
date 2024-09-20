import json
from typing import List, Union


def ler_matriz_csv(
    nome_arquivo: str, delimitador: str = ",", pular_cabecalho: int = 1
) -> List[List[Union[str, float]]]:
    """
    Lê um arquivo CSV e retorna uma matriz.
    """
    dados = []

    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        linhas = linhas[pular_cabecalho:]

        for linha in linhas:
            valores = linha.strip().split(delimitador)
            valores_convertidos = []

            for valor in valores:
                if valor.replace(".", "", 1).isdigit():
                    try:
                        valor_convertido = float(valor)
                    except ValueError:
                        valor_convertido = valor
                else:
                    valor_convertido = valor
                valores_convertidos.append(valor_convertido)
            dados.append(valores_convertidos)

    return dados


def ler_json(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        dict = json.load(file)
    return dict