from typing import List

from utils.algebra import Derivada, Matriz, Vetor


class SolversLineares:
    def __init__(self):
        self.matrizA = None
        self.vetorB = None
        self.tol = None
        self.lim_iter = None

    def gauss(
        self,
        matrizA: List[List[float]],
        vetorB: List[float],
        tol: float = 1e-5,
    ) -> List[float]:
        """
        Resolve um sistema de equações lineares da forma Ax = B
        utilizando o método de eliminação de Gauss.
        """
        A = Matriz.clone(matrizA)  # Copia a matriz para não modificar a original
        b = vetorB.copy()  # Copia o vetor para não modificar o original
        n = len(A)
        x = Vetor.criar(n)  # Inicializa o vetor solução com zeros

        # Fase 1: Eliminação de Gauss (transforma a A em uma matriz triangular superior).
        for k in range(n - 1):
            for i in range(k + 1, n):
                l_ik = A[i][k] / A[k][k]
                for j in range(k, n):
                    A[i][j] -= l_ik * A[k][j]
                b[i] -= l_ik * b[k]

        # Fase 2: Substituição regressiva (resolve o sistema triangular superior Ux = c).
        for k in range(n - 1, -1, -1):
            x[k] = b[k]
            for i in range(k + 1, n):
                x[k] -= A[k][i] * x[i]
            x[k] /= A[k][k]

        # Fase 3: Verifica se a solução obtida satisfaz a equação A * x = b.
        produto = Matriz.multiplicar(matrizA, x)
        erro = Vetor.subtracao(produto, vetorB)
        erro_max = Vetor.norma_infinita(erro)

        if erro_max <= tol:
            print(f"\n\tA solução converge com erro máximo: {erro_max:.2e}")
        else:
            print(f"\n\tA solução não converge. Erro máximo: {erro_max:.2e}")
        return x

    def decomposicao_lu(
        self,
        matrizA: List[List[float]],
        vetorB: List[float],
        tol: float = 1e-5,
    ) -> List[float]:
        """
        Decomposição LU: Resolve o sistema Ax = B utilizando a decomposição LU,
        onde A = LU e L é uma matriz triangular inferior com 1s na diagonal principal
        e U é uma matriz triangular superior.
        """
        n = len(matrizA)
        matrizL = Matriz.diagonal_principal(n, 1.0)  # Inicializa L com 1s na diagonal
        matrizU = Matriz.clone(matrizA)  # Copia A para U

        b = vetorB.copy()

        # Fase 1: Decomposição LU
        for k in range(n):
            for i in range(k + 1, n):
                l_ik = matrizU[i][k] / matrizU[k][k]
                matrizL[i][k] = l_ik
                for j in range(k, n):
                    matrizU[i][j] -= l_ik * matrizU[k][j]

        # Fase 2: Substituição.
        # Resolver Ly = B
        y = Vetor.criar(n)  # Inicializa y com zeros
        for i in range(n):
            soma = Vetor.produto_escalar(matrizL[i], y[:i])
            y[i] = b[i] - soma

        # Resolver Ux = y
        x = Vetor.criar(n)  # Inicializa x com zeros
        for i in range(n - 1, -1, -1):
            soma = Vetor.produto_escalar(matrizU[i][i + 1 :], x[i + 1 :])
            x[i] = (y[i] - soma) / matrizU[i][i]

        # Fase 3: Verifica se a solução obtida satisfaz a equação A * x = b.
        produto = Matriz.multiplicar(matrizA, x)
        erro = Vetor.subtracao(produto, vetorB)
        erro_max = Vetor.norma_infinita(erro)

        if erro_max < tol:
            print(f"\n\tA solução converge com erro máximo: {erro_max:.2e}")
        else:
            print(f"\n\tA solução não converge. Erro máximo: {erro_max:.2e}")
        return x

    def jacobi(
        self,
        matrizA: List[List[float]],
        vetorB: List[float],
        tol: float = 1e-5,
        lim_iter: int = 50,
    ) -> List[float]:
        """
        Resolve um sistema de equações lineares da forma Ax = B
        utilizando o método iterativo de Jacobi.
        """
        A = Matriz.clone(matrizA)
        b = vetorB.copy()

        n = len(b)
        x = Vetor.criar(n)
        x_novo = x.copy()

        iteracoes = 0
        convergencia = False

        while not convergencia and iteracoes < lim_iter:
            for i in range(n):
                soma = Vetor.produto_escalar(A[i], x) - A[i][i] * x[i]
                x_novo[i] = (b[i] - soma) / A[i][i]

            convergencia = all(abs(x_novo[i] - x[i]) < tol for i in range(n))
            x = x_novo[:]
            iteracoes += 1

        if convergencia:
            print(f"\n\tO método convergiu após {iteracoes} iterações.")
        else:
            print(f"\n\tO método não convergiu após {iteracoes} iterações.")
        return x

    def gauss_seidel(
        self,
        matrizA: List[List[float]],
        vetorB: List[float],
        tol: float = 1e-5,
        lim_iter: int = 50,
    ) -> List[float]:
        """
        Resolve um sistema de equações lineares da forma Ax = B
        utilizando o método iterativo de Gauss-Seidel.
        """
        A = Matriz.clone(matrizA)
        b = vetorB.copy()
        n = len(b)
        x = Vetor.criar(n)  # Vetor inicial (começando em zero)

        iteracoes = 0
        convergencia = False

        while not convergencia and iteracoes < lim_iter:
            convergencia = True  # Assume que convergiu nesta iteração

            for i in range(n):
                soma = Vetor.produto_escalar(A[i][:i], x[:i]) + Vetor.produto_escalar(
                    A[i][i + 1 :], x[i + 1 :]
                )
                x_novo = (b[i] - soma) / A[i][i]

                if abs(x_novo - x[i]) >= tol:
                    convergencia = (
                        False  # Não convergiu se a diferença for maior que a tolerância
                    )

                x[i] = x_novo

            iteracoes += 1

        if convergencia:
            print(f"\n\tO método convergiu após {iteracoes} iterações.")
        else:
            print(f"\n\tO método não convergiu após {iteracoes} iterações.")
        return x


class SolversNaoLineares:
    def __init__(self):
        self.f = None
        self.df = None
        self.x0 = None
        self.x1 = None
        self.tol = None
        self.lim_iter = None


    def bissecao(self, f, x0, x1, tol, lim_iter):
        """
        Encontra raízes de uma função f dentro de um intervalo [x1, x2]
        utilizando o método da bisseção.
        """

        # Verifica se a função f(x) muda de sinal no intervalo, caso contrário, o método da bisseção não pode ser aplicado.
        if f(x0) * f(x1) > 0:
            print("Nenhuma raiz encontrada no intervalo fornecido.")
            return None

        # Itera enquanto o erro for maior que a tolerância ou o número máximo de iterações não for atingido
        iteracoes = 0
        convergencia = False
        while iteracoes < lim_iter:
            x = (x0 + x1) / 2.0

            if f(x) == 0:
                continue

            # Atualiza os valores
            elif f(x0) * f(x) < 0:
                x1 = x
            else:
                x0 = x

            iteracoes += 1

            # Verifica a condição de convergência
            if abs(f(x1) - f(x0)) < tol:
                convergencia = True
                break
        
        if convergencia:
            print(f"\n\tO método convergiu após {iteracoes} iterações.")
        else:
            print(f"\n\tO método não convergiu após {iteracoes} iterações.")

        return x


    def secante(self, f, x0, x1, tol, lim_iter):
        """
        Encontra raízes de uma função f dentro de um intervalo [x1, x2]
        utilizando o método da secante.
        """

        # Calcula o valor inicial de f(x) para os pontos iniciais
        if f(x0) == 0:
            return f"Raiz: {x0}, Iterações: 0"

        if f(x1) == 0:
            return f"Raiz: {x1}, Iterações: 1"

        iteracoes = 0
        convergencia = False
        while iteracoes < lim_iter:

            # Calcula a nova aproximação utilizando a fórmula do método da secante
            try:
                x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
            except ZeroDivisionError:
                return "Divisão por zero!"

            # Atualiza os valores
            x0, x1 = x1, x2
            iteracoes += 1

            # Verifica a condição de convergência
            if abs(f(x1)) < tol:
                convergencia = True
                break
        
        if convergencia:
            print(f"\n\tO método convergiu após {iteracoes} iterações.")
        else:
            print(f"\n\tO método não convergiu após {iteracoes} iterações.")

        return x1
    
    def newton_raphson(self, f, x0, x1, tol, lim_iter):
        """
        Encontra raízes de uma função f dentro de um intervalo [x1, x2]
        utilizando o método Newton-Raphson.
        """
        # Chute inicial usando a bisseção
        x = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        
        d = Derivada

        if d.diferencas_finitas(f, x) == 0:
            print("Derivada é zero no ponto inicial. O método de Newton-Raphson não pode ser aplicado.")
            return None

        iteracoes = 1
        convergencia = False
        while iteracoes <= lim_iter:
            x_i = x - f(x) / d.diferencas_finitas(f, x)

            # Verifica a condição de convergência
            if abs(f(x_i)) < tol:
                convergencia = True
                break

            if d.diferencas_finitas(f, x_i) == 0:
                print("Derivada é zero durante a iteração. O método de Newton-Raphson não pode ser aplicado.")
                return None

            # Atualiza os valores
            x = x_i
            iteracoes += 1

        if convergencia:
            print(f"\n\tO método convergiu após {iteracoes} iterações.")
        else:
            print(f"\n\tO método não convergiu após {iteracoes} iterações.")

        return x
