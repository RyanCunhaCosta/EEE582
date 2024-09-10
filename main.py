from utils.modulos import executar_teste, print_enunciado


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
    main(2)  # < --- Ajustar numero do teste
