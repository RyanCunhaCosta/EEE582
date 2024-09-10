import inspect
import math

from utils.benchmark import Timer
from utils.solver import SolversNaoLineares


def executar_teste():
    """Permite ao usuário escolher um sistema e um método para executar, com a opção de voltar ao menu principal."""
    # Opções de funções

    def f1(x):
        return 5 * math.cos(x)**2 - 3 * math.sin(3 * x)

    funcoes = {
        "1": f1,
    }

    print("Escolha o sistema:")
    for chave, func in funcoes.items():
        print(f"{chave} - {inspect.getsource(func)}")

    escolha_sistema = input("Digite o número do sistema desejado: ").strip()

    if escolha_sistema not in funcoes:
        print("Escolha de sistema inválida.")
        return

    # Opções de métodos
    metodos = [
        ("Bisseção", "bissecao"),
        ("Secante", "secante"),
        ("Newton Raphson", "newton_raphson"),
    ]

    x0 = 0  # Limite inferior do intervalo
    x1 = 5  # Limite superior do intervalo
    tol = 1e-9  # Tolerância
    lim_iter = 100 # Limite de iterações

    for metodo_nome, metodo_nome_funcao in metodos:
        print(f"\nSolução pelo método de {metodo_nome}: ")

        # Instanciar a classe a cada iteração
        solvers = SolversNaoLineares()
        metodo_funcao = getattr(solvers, metodo_nome_funcao)

        timer = Timer()
        timer.start()

        resultado = metodo_funcao(funcoes[escolha_sistema], x0, x1, tol, lim_iter)

        print(f"\tX = {resultado}")

        timer.end()


def main():
    while True:
        executar_teste()

        if input("\nDeseja escolher outra função? (s/n): ") not in ["s", "S"]:
            print("Saindo...")
            break


if __name__ == "__main__":
    main()
