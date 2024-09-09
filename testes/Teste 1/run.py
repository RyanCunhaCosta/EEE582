from utils.algebra import Matriz
from utils.solver import SolversLineares
from utils.benchmark import Timer
from utils.arquivos import ler_matriz_csv


def executar_teste():
    """Permite ao usuário escolher um sistema e um método para executar, com a opção de voltar ao menu principal."""
    # Opções de sistemas
    sistemas = {
        "1": "testes/Teste 1/lin_sist_1.txt",
        "2": "testes/Teste 1/lin_sist_2.txt",
        # Adicione outros sistemas aqui se necessário
    }

    print("Escolha o sistema:")
    for chave, caminho in sistemas.items():
        print(f"{chave} - {caminho.split('/')[-1]}")

    escolha_sistema = input("Digite o número do sistema desejado: ").strip()

    if escolha_sistema not in sistemas:
        print("Escolha de sistema inválida.")
        return

    sistema_path = sistemas[escolha_sistema]
    sistema = ler_matriz_csv(sistema_path)
    A, b = Matriz.separar_sistema(sistema)

    # Opções de métodos
    metodos = [
        ("Gauss", "gauss"),
        ("Decomposição LU", "decomposicao_lu"),
        ("Jacobi", "jacobi"),
        ("Gauss Seidel", "gauss_seidel"),
    ]

    for metodo_nome, metodo_nome_funcao in metodos:
        print(f"\nSolução pelo método de {metodo_nome}: ")

        # Instanciar a classe a cada iteração
        solvers = SolversLineares()
        metodo_funcao = getattr(solvers, metodo_nome_funcao)

        timer = Timer()
        timer.start()

        resultado = metodo_funcao(A, b)

        if resultado:
            for i, valor in enumerate(resultado):
                print(f"\tX{i+1} = {valor}")

        timer.end()


def main():
    while True:
        executar_teste()

        if input("\nDeseja escolher outro sistema? (s/n): ") not in ["s", "S"]:
            print("Saindo...")
            break


if __name__ == "__main__":
    main()
