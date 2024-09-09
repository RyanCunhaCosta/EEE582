from utils.modulos import print_enunciado, executar_teste


def main(numero_teste):
    print("**************************************")
    print("Aplicação Computacional em Sistemas de Potência - EEE582")
    print("Alunos: Ryan, Ravi, Pedro, Carolina")
    print("Professor: Thiago Masseran")
    print("**************************************\n")

    print(f"Executando o Teste Nº {numero_teste}\n")

    print_enunciado(f"testes/Teste {numero_teste}/enunciado.txt")
    executar_teste(f"testes/Teste {numero_teste}/run.py")


if __name__ == "__main__":
    main(1)  # < --- Ajustar numero do teste
