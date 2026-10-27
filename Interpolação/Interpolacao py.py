import math

MAX_PONTOS = 20

def P_lagrange(n, x, y, xp):
    """Polinômio de Lagrange"""
    yp = 0.0
    for i in range(n):
        p = 1.0
        for j in range(n):
            if i != j:
                p *= (xp - x[j]) / (x[i] - x[j])
        yp += y[i] * p
    return yp

def D_lagrange(n, x, y, xp):
    """Dispositivo de Lagrange"""
    print("\nDispositivo de Lagrange:")
    print("P(x) = ", end="")
    
    Gd = 1.0
    for j in range(n):
        Gd *= (xp - x[j])
    
    soma = 0.0
    for i in range(n):
        Gi = 1.0
        for j in range(n):
            if j != i:
                Gi *= (x[i] - x[j])
        soma += y[i] / ((xp - x[i]) * Gi)
    
    return Gd * soma

def P_newton(n, x, y, xp):
    """Método de Newton com diferenças divididas"""
    coef = y.copy()
    
    # Calcula diferenças divididas
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            coef[i] = (coef[i] - coef[i-1]) / (x[i] - x[i-j])
    
    # Avalia o polinômio
    yp = coef[n-1]
    for i in range(n-2, -1, -1):
        yp = yp * (xp - x[i]) + coef[i]
    
    return yp

def G_newton(n, x, y, xp):
    """Polinômio de Gregory-Newton (para pontos igualmente espaçados)"""
    # Matriz de diferenças
    diff = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        diff[i][0] = y[i]
    
    # Calcula diferenças finitas
    for j in range(1, n):
        for i in range(n - j):
            diff[i][j] = diff[i+1][j-1] - diff[i][j-1]
    
    # Verifica se os pontos são igualmente espaçados
    h = x[1] - x[0]
    for i in range(2, n):
        if abs((x[i] - x[i-1]) - h) > 1e-10:
            print("Aviso: Pontos não são igualmente espaçados! Resultado pode ser impreciso.")
            break
    
    p = (xp - x[0]) / h
    yp = y[0]
    fact = 1.0
    p_term = 1.0
    
    for i in range(1, n):
        p_term *= (p - (i - 1))
        fact *= i
        yp += (p_term * diff[0][i]) / fact
    
    return yp

def truncamento(y, grau):
    """Estima erro de truncamento"""
    if grau + 2 >= MAX_PONTOS:
        print("Dados insuficientes para estimar erro.")
        return
    
    if grau + 1 < len(y):
        erro = abs(y[grau + 1] - y[grau])
        print(f"Erro estimado de truncamento: {erro}")
    else:
        print("Grau muito alto para os dados disponíveis.")

def main_interpolacao():
    """Função principal com menu interativo"""
    while True:
        print("\n--- INTERPOLAÇÃO ---")
        print("1. Polinômio de Lagrange")
        print("2. Dispositivo de Lagrange")
        print("3. Método de Newton")
        print("4. Polinômio de Gregory-Newton")
        print("5. Estimar erro de truncamento")
        print("0. Sair")
        
        try:
            opcao = int(input("Escolha a opção: "))
        except ValueError:
            print("Opção inválida!")
            continue
        
        if opcao == 0:
            print("Saindo...")
            break
        
        if opcao < 1 or opcao > 5:
            print("Opção inválida!")
            continue
        
        try:
            n = int(input(f"Digite o número de pontos (máx. {MAX_PONTOS}): "))
            
            if n > MAX_PONTOS:
                print("Número máximo de pontos excedido!")
                continue
            
            if n <= 0:
                print("Número inválido de pontos!")
                continue
            
            x = []
            y = []
            
            for i in range(n):
                x_val = float(input(f"x[{i}]: "))
                y_val = float(input(f"y[{i}]: "))
                x.append(x_val)
                y.append(y_val)
            
            # Verifica se os valores de x são distintos (para Lagrange/Newton)
            if opcao in [1, 2, 3]:
                distinct = True
                for i in range(n):
                    for j in range(i+1, n):
                        if x[i] == x[j]:
                            print("Aviso: Valores de x não são distintos!")
                            distinct = False
                            break
                    if not distinct:
                        break
            
            if opcao in [1, 2, 3, 4]:
                xp = float(input("Digite o valor de x para interpolar: "))
            
            if opcao == 1:
                resultado = P_lagrange(n, x, y, xp)
                print(f"Resultado (Lagrange): {resultado:.6f}")
            
            elif opcao == 2:
                resultado = D_lagrange(n, x, y, xp)
                print(f"Valor aproximado de P({xp}) = {resultado:.6f}")
            
            elif opcao == 3:
                resultado = P_newton(n, x, y, xp)
                print(f"Resultado (Newton): {resultado:.6f}")
            
            elif opcao == 4:
                resultado = G_newton(n, x, y, xp)
                print(f"Resultado (Gregory-Newton): {resultado:.6f}")
            
            elif opcao == 5:
                grau = int(input("Digite o grau usado para interpolação: "))
                truncamento(y, grau)
        
        except ValueError:
            print("Erro: Digite valores numéricos válidos!")
        except ZeroDivisionError:
            print("Erro: Divisão por zero! Verifique os dados de entrada.")
        except IndexError:
            print("Erro: Índice fora dos limites!")
        except Exception as e:
            print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main_interpolacao()