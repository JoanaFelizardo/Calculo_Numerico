import numpy as np

def alocar_matriz(num):
    """Aloca uma matriz quadrada de zeros"""
    return np.zeros((num, num))

def ler_matriz(num):
    """Lê a matriz e o vetor do usuário"""
    print(f"Digite a Matriz A ({num}x{num}):")
    matriz = np.zeros((num, num))
    for i in range(num):
        for j in range(num):
            matriz[i][j] = float(input(f"A[{i}][{j}]: "))
    
    print("Digite o vetor b:")
    vetor = np.zeros(num)
    for i in range(num):
        vetor[i] = float(input(f"b[{i}]: "))
    
    return matriz, vetor

def ler_matriz_arquivo(num, nome_arquivo):
    """Lê a matriz e o vetor de um arquivo"""
    try:
        with open(nome_arquivo, 'r') as arquivo:
            matriz = np.zeros((num, num))
            for i in range(num):
                linha = arquivo.readline().split()
                for j in range(num):
                    matriz[i][j] = float(linha[j])
            
            vetor = np.zeros(num)
            linha = arquivo.readline().split()
            for i in range(num):
                vetor[i] = float(linha[i])
            
            return matriz, vetor
    except FileNotFoundError:
        print(f"ERRO AO ABRIR O ARQUIVO {nome_arquivo}")
        return None, None
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None, None

def mostrar_vetor(x):
    """Exibe o vetor solução"""
    print("Solução:")
    for i in range(len(x)):
        print(f"x[{i}] = {x[i]:.6f}")
    print()

# As funções gauss_simples, gauss_pivot_parcial, decomposicao_lu, decomposicao_lu_pp 
# são as mesmas da versão anterior

def main_arquivo():
    """Função principal com opção de leitura de arquivo"""
    print("Digite a ordem da matriz: ", end="")
    num = int(input())
    
    print("Deseja ler do arquivo (A) ou digitar manualmente (M)? ", end="")
    escolha_entrada = input().strip().upper()
    
    matriz, vetor = None, None
    
    if escolha_entrada == 'A':
        print("Digite o nome do arquivo: ", end="")
        nome_arquivo = input()
        matriz, vetor = ler_matriz_arquivo(num, nome_arquivo)
        if matriz is None:
            return
    else:
        matriz, vetor = ler_matriz(num)
    
    while True:
        print("\n" + "-" * 35)
        print("--- MENU ---")
        print("1. Eliminação de Gauss Simples")
        print("2. Eliminação de Gauss com Pivotação Parcial")
        print("3. Decomposição LU")
        print("4. Decomposição LU com Pivotação Parcial")
        print("0. Sair")
        print("Escolha uma opção: ", end="")
        
        opcao = int(input())
        
        if opcao == 0:
            print("Saindo do programa...")
            break
        
        solucao = None
        
        if opcao == 1:
            solucao = gauss_simples(matriz, vetor)
        elif opcao == 2:
            solucao = gauss_pivot_parcial(matriz, vetor)
        elif opcao == 3:
            solucao = decomposicao_lu(matriz, vetor)
        elif opcao == 4:
            solucao = decomposicao_lu_pp(matriz, vetor)
        else:
            print("Opção inválida!")
            continue
        
        if solucao is not None:
            mostrar_vetor(solucao)

if __name__ == "__main__":
    # Para usar a versão com arquivo, chame main_arquivo()
    # Para usar a versão básica, chame main()
    main_arquivo()