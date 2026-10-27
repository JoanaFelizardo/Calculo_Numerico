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

def mostrar_vetor(x):
    """Exibe o vetor solução"""
    print("Solução:")
    for i in range(len(x)):
        print(f"x[{i}] = {x[i]:.6f}")
    print()

def gauss_simples(matriz, vetor):
    """Eliminação de Gauss Simples"""
    num = len(matriz)
    A = matriz.copy()
    b = vetor.copy()
    
    # Eliminação
    for k in range(num - 1):
        for i in range(k + 1, num):
            m = A[i][k] / A[k][k]
            for j in range(k, num):
                A[i][j] -= m * A[k][j]
            b[i] -= m * b[k]
    
    # Substituição regressiva
    x = np.zeros(num)
    for i in range(num - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, num):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def gauss_pivot_parcial(matriz, vetor):
    """Eliminação de Gauss com Pivotação Parcial"""
    num = len(matriz)
    A = matriz.copy()
    b = vetor.copy()
    
    # Eliminação com pivotação
    for k in range(num - 1):
        # Pivotação parcial
        max_index = k
        for i in range(k + 1, num):
            if abs(A[i][k]) > abs(A[max_index][k]):
                max_index = i
        
        if max_index != k:
            # Troca linhas
            A[[k, max_index]] = A[[max_index, k]]
            b[k], b[max_index] = b[max_index], b[k]
        
        # Eliminação
        for i in range(k + 1, num):
            m = A[i][k] / A[k][k]
            for j in range(k, num):
                A[i][j] -= m * A[k][j]
            b[i] -= m * b[k]
    
    # Substituição regressiva
    x = np.zeros(num)
    for i in range(num - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, num):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def decomposicao_lu(matriz, vetor):
    """Decomposição LU"""
    num = len(matriz)
    A = matriz.copy()
    b = vetor.copy()
    
    # Inicializa L e U
    L = np.eye(num)  # Matriz identidade
    U = np.zeros((num, num))
    
    # Decomposição LU
    for k in range(num):
        U[k][k] = A[k][k]
        for i in range(k + 1, num):
            L[i][k] = A[i][k] / U[k][k]
            U[k][i] = A[k][i]
        
        for i in range(k + 1, num):
            for j in range(k + 1, num):
                A[i][j] -= L[i][k] * U[k][j]
    
    # Resolve Ly = b
    y = np.zeros(num)
    for i in range(num):
        y[i] = b[i]
        for j in range(i):
            y[i] -= L[i][j] * y[j]
    
    # Resolve Ux = y
    x = np.zeros(num)
    for i in range(num - 1, -1, -1):
        x[i] = y[i]
        for j in range(i + 1, num):
            x[i] -= U[i][j] * x[j]
        x[i] /= U[i][i]
    
    print("Matriz L:")
    print(L)
    print("\nMatriz U:")
    print(U)
    
    return x

def decomposicao_lu_pp(matriz, vetor):
    """Decomposição LU com Pivotação Parcial"""
    num = len(matriz)
    A = matriz.copy()
    b = vetor.copy()
    
    # Vetor de permutação
    P = np.arange(num)
    
    # Decomposição com pivotação
    for k in range(num):
        # Pivotação parcial
        max_index = k
        for i in range(k + 1, num):
            if abs(A[i][k]) > abs(A[max_index][k]):
                max_index = i
        
        if max_index != k:
            # Troca linhas
            A[[k, max_index]] = A[[max_index, k]]
            P[k], P[max_index] = P[max_index], P[k]
        
        # Eliminação
        for i in range(k + 1, num):
            A[i][k] /= A[k][k]
            for j in range(k + 1, num):
                A[i][j] -= A[i][k] * A[k][j]
    
    # Extrai L e U
    L = np.eye(num)
    U = np.zeros((num, num))
    
    for i in range(num):
        for j in range(num):
            if i > j:
                L[i][j] = A[i][j]
            else:
                U[i][j] = A[i][j]
    
    # Aplica permutação no vetor b
    Pb = b[P]
    
    # Resolve Ly = Pb
    y = np.zeros(num)
    for i in range(num):
        y[i] = Pb[i]
        for j in range(i):
            y[i] -= L[i][j] * y[j]
    
    # Resolve Ux = y
    x = np.zeros(num)
    for i in range(num - 1, -1, -1):
        x[i] = y[i]
        for j in range(i + 1, num):
            x[i] -= U[i][j] * x[j]
        x[i] /= U[i][i]
    
    print("Matriz L:")
    print(L)
    print("\nMatriz U:")
    print(U)
    
    return x

def main():
    """Função principal"""
    print("Digite a ordem da matriz: ", end="")
    num = int(input())
    
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
    main()