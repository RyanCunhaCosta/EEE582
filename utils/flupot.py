from utils.algebra import Angulo, Matriz
from utils.solver import SolversLineares
import numpy as np


class Flupot:
    def linearizado(self, dados_barras, dados_linhas):
        from utils.arquivos import ler_json

        sistema = ler_json("testes/Teste 3/sistema1.json")

        dados_barras = sistema["BARRAS"]
        dados_linhas = sistema["LINHAS"]
        ##############################################################################################################

        P = [barra["P (PU)"] for barra in dados_barras]
        num_barras = len(P)

        m = Matriz()
        B = m.zeros(num_barras, num_barras)

        for linha in dados_linhas:
            i = linha["DE"]
            j = linha["PARA"]
            x = linha["x"]

            susceptancia = 1 / x

            B[i - 1][j - 1] -= susceptancia  # Elemento fora da diagonal
            B[j - 1][i - 1] -= susceptancia  # Matriz simétrica
            B[i - 1][i - 1] += susceptancia  # Soma na diagonal
            B[j - 1][j - 1] += susceptancia  # Soma na diagonal da outra barra

        B, _ = m.separar_sistema(B)
        P = P[:-1]

        s = SolversLineares()
        theta = s.gauss_seidel(B, P)
        theta_ref = next(
            barra["θ (graus)"] for barra in dados_barras if barra["TIPO"] == "SLACK"
        )
        theta.append(theta_ref)

        a = Angulo()
        teta_graus = a.r2g(theta)

        for i, barra in enumerate(dados_barras):
            barra["θ (graus)"] = round(teta_graus[i], 2)

        for linha in dados_linhas:
            i = linha["DE"] - 1
            j = linha["PARA"] - 1
            x = linha["x"]

            Pij = (theta[i] - theta[j]) / x

            linha["POTENCIA (PU)"] = round(Pij, 2)

        return {"BARRAS": dados_barras, "LINHAS": dados_linhas}

    def newton_raphson(self, dados_barras, dados_linhas):
        P = np.array(
            [
                barra["P (PU)"] if barra["P (PU)"] is not None else 0.0
                for barra in dados_barras
            ]
        )
        Q = np.array(
            [
                barra["Q (PU)"] if barra["Q (PU)"] is not None else 0.0
                for barra in dados_barras
            ]
        )
        V = np.array(
            [
                barra["V (PU)"] if barra["V (PU)"] is not None else 0.0
                for barra in dados_barras
            ]
        )
        theta = np.array(
            [
                barra["θ (graus)"] if barra["θ (graus)"] is not None else 0.0
                for barra in dados_barras
            ]
        )

        # Encontrando o ângulo de referência
        theta_ref = next(
            barra["θ (graus)"] for barra in dados_barras if barra["TIPO"] == "SLACK"
        )
        theta = np.append(theta, theta_ref)

        num_barras = len(P)

        # Inicializando a matriz Y
        Y = np.zeros((num_barras, num_barras), dtype=complex)

        # Construindo a matriz de admitância
        for linha in dados_linhas:
            i = linha["DE"] - 1
            j = linha["PARA"] - 1
            r = linha["r"]
            x = linha["x"]
            b = linha["b"]

            z = complex(r, x)
            y = 1 / z
            b_shunt = complex(0, b / 2)

            Y[i, j] -= y
            Y[j, i] -= y
            Y[i, i] += y + b_shunt
            Y[j, j] += y + b_shunt

        # Separando G e B
        G = np.real(Y)
        B = np.imag(Y)

        def mismatch(P, Q, V, theta, num_barras, G, B):
            P_calc = np.zeros(num_barras)
            Q_calc = np.zeros(num_barras)

            for i in range(num_barras):
                for j in range(num_barras):
                    P_calc[i] += (
                        V[i]
                        * V[j]
                        * (
                            G[i, j] * np.cos(theta[i] - theta[j])
                            + B[i, j] * np.sin(theta[i] - theta[j])
                        )
                    )
                    Q_calc[i] += (
                        V[i]
                        * V[j]
                        * (
                            G[i, j] * np.sin(theta[i] - theta[j])
                            - B[i, j] * np.cos(theta[i] - theta[j])
                        )
                    )

            deltaP = P - P_calc
            deltaQ = Q - Q_calc
            return deltaP, deltaQ

        def jacobiano(V, theta, G, B):
            n = len(V)
            H = np.zeros((n, n))
            N = np.zeros((n, n))
            M = np.zeros((n, n))
            L = np.zeros((n, n))

            for i in range(n):
                for j in range(n):
                    if i == j:
                        for k in range(n):
                            if k != i:
                                H[i, i] += (
                                    V[i]
                                    * V[k]
                                    * (
                                        -G[i, k] * np.sin(theta[i] - theta[k])
                                        + B[i, k] * np.cos(theta[i] - theta[k])
                                    )
                                )
                                N[i, i] += V[k] * (
                                    G[i, k] * np.cos(theta[i] - theta[k])
                                    + B[i, k] * np.sin(theta[i] - theta[k])
                                )
                                M[i, i] -= (
                                    V[i]
                                    * V[k]
                                    * (
                                        G[i, k] * np.cos(theta[i] - theta[k])
                                        + B[i, k] * np.sin(theta[i] - theta[k])
                                    )
                                )
                                L[i, i] -= V[k] * (
                                    G[i, k] * np.sin(theta[i] - theta[k])
                                    - B[i, k] * np.cos(theta[i] - theta[k])
                                )
                        H[i, i] += V[i] ** 2 * B[i, i]
                        L[i, i] += V[i] ** 2 * B[i, i]
                    else:
                        H[i, j] = (
                            V[i]
                            * V[j]
                            * (
                                G[i, j] * np.sin(theta[i] - theta[j])
                                - B[i, j] * np.cos(theta[i] - theta[j])
                            )
                        )
                        N[i, j] = V[i] * (
                            G[i, j] * np.cos(theta[i] - theta[j])
                            + B[i, j] * np.sin(theta[i] - theta[j])
                        )
                        M[i, j] = (
                            -V[i]
                            * V[j]
                            * (
                                G[i, j] * np.cos(theta[i] - theta[j])
                                + B[i, j] * np.sin(theta[i] - theta[j])
                            )
                        )
                        L[i, j] = V[i] * (
                            G[i, j] * np.sin(theta[i] - theta[j])
                            - B[i, j] * np.cos(theta[i] - theta[j])
                        )

            # Construir a matriz Jacobiana
            J = np.block([[H, N], [M, L]])

            return J

        tol = 1e-3
        converge = False
        while not converge:
            deltaP, deltaQ = mismatch(P, Q, V, theta, num_barras, G, B)

            if np.max(np.abs(deltaP)) < tol and np.max(np.abs(deltaQ)) < tol:
                converge = True

            J = jacobiano(V, theta, G, B)

            delta_theta, delta_V = np.linalg.solve(J, np.concatenate([deltaP, deltaQ]))

            theta[:num_barras] += delta_theta
            V[:num_barras] += delta_V

            if np.max(np.abs(delta_theta)) < tol and np.max(np.abs(delta_V)) < tol:
                converge = True

        for i, barra in enumerate(dados_barras):
            barra["V (PU)"] = round(V[i], 2)
            barra["θ (graus)"] = round(theta[i], 2)

        for linha in dados_linhas:
            i = linha["DE"] - 1
            j = linha["PARA"] - 1

            Vi = V[i] * np.exp(1j * np.radians(theta[i]))
            Vj = V[j] * np.exp(1j * np.radians(theta[j]))

            Iij = (Vi - Vj) * Y[i, j]
            Sij = Vi * np.conj(Iij)

            linha["POTENCIA (PU)"] = round(Sij.real, 2) + round(Sij.imag, 2) * 1j

        return {"BARRAS": dados_barras, "LINHAS": dados_linhas}
