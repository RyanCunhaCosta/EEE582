from utils.algebra import Angulo, Matriz
from utils.solver import SolversLineares


class Flupot:
    def linearizado(self, dados_barras, dados_linhas):
        P = [barra["PG (PU)"] for barra in dados_barras]
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
        teta = s.gauss_seidel(B, P)
        teta_ref = 0
        teta.append(teta_ref)

        a = Angulo()
        teta_graus = a.r2g(teta)

        for i, barra in enumerate(dados_barras):
            barra["ANGULO (GRAUS)"] = round(teta_graus[i], 2)

        for linha in dados_linhas:
            i = linha["DE"]
            j = linha["PARA"]
            x = linha["x"]

            Pij = (teta[i - 1] - teta[j - 1]) / x

            linha["POTENCIA (PU)"] = round(Pij, 2)

        return {"BARRAS": dados_barras, "LINHAS": dados_linhas}

    def newton_raphson(self, dados_barras, dados_linhas):
        pass
