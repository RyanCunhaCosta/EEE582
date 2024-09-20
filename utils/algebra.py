import math
from typing import List, Tuple, Union


class Angulo:
    @staticmethod
    def r2g(radianos: Union[float, List[float]]) -> Union[float, List[float]]:
        """
        Converte um ângulo de radianos para graus.
        """
        if isinstance(radianos, list):
            return [r * (180.0 / math.pi) for r in radianos]
        return radianos * (180.0 / math.pi)

    @staticmethod
    def g2r(graus: Union[float, List[float]]) -> Union[float, List[float]]:
        """
        Converte um ângulo de graus para radianos.
        """
        if isinstance(graus, list):
            return [g * (math.pi / 180.0) for g in graus]
        return graus * (math.pi / 180.0)

class Vetor:
    @staticmethod
    def criar(n: int, valor: float = 0.0) -> List[float]:
        """
        Cria um vetor de tamanho `n` inicializado com um valor constante.
        """
        return [valor] * n

    @staticmethod
    def soma(vA: List[float], vB: List[float]) -> List[float]:
        """
        Realiza a soma de dois vetores.
        """
        return [a + b for a, b in zip(vA, vB)]

    @staticmethod
    def subtracao(vA: List[float], vB: List[float]) -> List[float]:
        """
        Realiza a subtração de dois vetores.
        """
        return [a - b for a, b in zip(vA, vB)]

    @staticmethod
    def produto_escalar(vA: List[float], vB: List[float]) -> float:
        """
        Calcula o produto escalar de dois vetores.
        """
        return sum(a * b for a, b in zip(vA, vB))

    @staticmethod
    def norma(v: List[float]) -> float:
        """
        Calcula a norma (magnitude) de um vetor.
        """
        return sum(a**2 for a in v) ** 0.5

    @staticmethod
    def multiplicar_por_escalar(v: List[float], escalar: float) -> List[float]:
        """
        Multiplica todos os elementos de um vetor por um escalar.
        """
        return [a * escalar for a in v]

    @staticmethod
    def normalizar(v: List[float]) -> List[float]:
        """
        Normaliza o vetor, fazendo com que sua norma seja igual a 1.
        """
        norma_v = Vetor.norma(v)
        if norma_v == 0:
            raise ValueError("Não é possível normalizar um vetor nulo.")
        return [a / norma_v for a in v]

    @staticmethod
    def norma_infinita(v: List[float]) -> float:
        """
        Calcula a norma infinita (máximo valor absoluto) de um vetor.
        """
        return max(abs(x) for x in v)


class Matriz:
    """
    Classe utilitária para operações matriciais básicas.
    """

    @staticmethod
    def clone(matriz: List[List[float]]) -> List[List[float]]:
        """
        Retorna uma cópia da matriz fornecida.
        """
        return [linha[:] for linha in matriz]

    @staticmethod
    def constante(linhas: int, colunas: int, valor: float) -> List[List[float]]:
        """
        Cria uma matriz com o mesmo valor em todas as posições.
        """
        matriz = []
        for _ in range(linhas):
            linha = Vetor.criar(colunas, valor)
            matriz.append(linha)
        return matriz

    @staticmethod
    def diagonal_principal(tamanho: int, valor: float) -> List[List[float]]:
        """
        Cria uma matriz quadrada com o valor especificado na diagonal principal e zeros no restante.
        """
        matriz = []
        for i in range(tamanho):
            linha = Vetor.criar(tamanho, 0)
            linha[i] = valor
            matriz.append(linha)
        return matriz

    @staticmethod
    def diagonal_secundaria(tamanho: int, valor: float) -> List[List[float]]:
        """
        Cria uma matriz quadrada com o valor especificado na diagonal secundária e zeros no restante.
        """
        matriz = []
        for i in range(tamanho):
            linha = Vetor.criar(tamanho, 0)
            linha[tamanho - 1 - i] = valor
            matriz.append(linha)
        return matriz

    @staticmethod
    def identidade(tamanho: int) -> List[List[float]]:
        """
        Cria uma matriz identidade (1 na diagonal principal, 0 no restante).
        """
        return Matriz.diagonal_principal(tamanho, 1)

    @staticmethod
    def zeros(linhas: int, colunas: int) -> List[List[float]]:
        """
        Cria uma matriz de zeros.
        """
        return Matriz.constante(linhas, colunas, 0)

    @staticmethod
    def separar_sistema(
        sistema: List[List[float]],
    ) -> Tuple[List[List[float]], List[float]]:
        """
        Separa uma lista de listas em uma matriz A e um vetor b.
        """
        matrizA = [linha[:-1] for linha in sistema]
        vetorB = [linha[-1] for linha in sistema]
        return matrizA, vetorB

    @staticmethod
    def transposta(matriz: List[List[float]]) -> List[List[float]]:
        """
        Calcula a transposta de uma matriz.
        """
        linhas = len(matriz)
        colunas = len(matriz[0])
        matriz_transposta = Matriz.zeros(colunas, linhas)

        for i in range(linhas):
            for j in range(colunas):
                matriz_transposta[j][i] = matriz[i][j]

        return matriz_transposta

    @staticmethod
    def multiplicar(
        matrizA: List[List[float]], matrizB: Union[List[List[float]], List[float]]
    ) -> Union[List[List[float]], List[float]]:
        """
        Multiplica uma matriz por outra matriz ou por um vetor.
        """
        if isinstance(matrizB[0], list):  # Verifica se matrizB é uma matriz
            # Multiplicação de matriz por matriz
            linhas_A = len(matrizA)
            colunas_A = len(matrizA[0])
            linhas_B = len(matrizB)
            colunas_B = len(matrizB[0])

            if colunas_A != linhas_B:
                raise ValueError(
                    "Número de colunas de matrizA deve ser igual ao número de linhas de matrizB."
                )

            resultado = Matriz.zeros(linhas_A, colunas_B)

            for i in range(linhas_A):
                for j in range(colunas_B):
                    soma = 0.0
                    for k in range(colunas_A):
                        soma += matrizA[i][k] * matrizB[k][j]
                    resultado[i][j] = soma

            return resultado

        else:  # Caso contrário, matrizB é um vetor
            # Multiplicação de matriz por vetor
            num_linhas = len(matrizA)
            num_colunas = len(matrizB)
            resultado = [0.0] * num_linhas

            for i in range(num_linhas):
                soma = 0.0
                for j in range(num_colunas):
                    soma += matrizA[i][j] * matrizB[j]
                resultado[i] = soma

            return resultado

    @staticmethod
    def soma(
        matrizA: List[List[float]], matrizB: List[List[float]]
    ) -> List[List[float]]:
        """
        Soma duas matrizes de mesma dimensão.
        """
        linhas = len(matrizA)
        colunas = len(matrizA[0])

        if linhas != len(matrizB) or colunas != len(matrizB[0]):
            raise ValueError("As matrizes devem ter as mesmas dimensões.")

        resultado = Matriz.zeros(linhas, colunas)

        for i in range(linhas):
            for j in range(colunas):
                resultado[i][j] = matrizA[i][j] + matrizB[i][j]

        return resultado

    @staticmethod
    def subtracao(
        matrizA: List[List[float]], matrizB: List[List[float]]
    ) -> List[List[float]]:
        """
        Subtrai a matriz B da matriz A (A - B).
        """
        linhas = len(matrizA)
        colunas = len(matrizA[0])

        if linhas != len(matrizB) or colunas != len(matrizB[0]):
            raise ValueError("As matrizes devem ter as mesmas dimensões.")

        resultado = Matriz.zeros(linhas, colunas)

        for i in range(linhas):
            for j in range(colunas):
                resultado[i][j] = matrizA[i][j] - matrizB[i][j]

        return resultado

    @staticmethod
    def print(matriz: List[List[float]]) -> None:
        """
        Exibe uma matriz de forma formatada no terminal.
        """
        for linha in matriz:
            linha_formatada = " ".join(f"{x:.2f}" for x in linha)
            print("[", linha_formatada, "]")


class Derivada:
    def diferencas_finitas(f, x, h=1e-5):
        """
        Calcula a derivada de primeira ordem usando o método de diferenças finitas.
        """
        return (f(x + h) - f(x - h)) / (2 * h)