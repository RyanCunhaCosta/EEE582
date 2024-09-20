from utils.arquivos import ler_json
from utils.benchmark import Timer
from utils.flupot import Flupot
from utils.modulos import print_table


def executar_teste():
    """Permite ao usuário escolher um sistema e um método para executar, com a opção de voltar ao menu principal."""
    # Opções de sistemas
    sistemas = {
        "1": "testes/Teste 3/sistema1.json",
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
    sistema = ler_json(sistema_path)

    dados_barras = sistema["BARRAS"]
    print("\nDados das barras: ")
    print_table(dados_barras)

    dados_linhas = sistema["LINHAS"]
    print("\nDados das linhas: ")
    print_table(dados_linhas)

    # Opções de métodos
    metodos = [
        ("Linearizado", "linearizado"),
        # ("Newton Raphson", "newton_raphson"),
    ]

    for metodo_nome, metodo_nome_funcao in metodos:
        print(f"\nSolução pelo método de {metodo_nome}: ")

        # Instanciar a classe a cada iteração
        flupot = Flupot()
        metodo_funcao = getattr(flupot, metodo_nome_funcao)

        timer = Timer()
        timer.start()

        resultado = metodo_funcao(dados_barras, dados_linhas)

        print("\nResultado das barras: ")
        print_table(resultado["BARRAS"])

        print("\nResultado das linhas: ")
        print_table(resultado["LINHAS"])

        timer.end()


def main():
    while True:
        executar_teste()

        if input("\nDeseja escolher outra função? (s/n): ") not in ["s", "S"]:
            print("Saindo...")
            break


if __name__ == "__main__":
    main()
