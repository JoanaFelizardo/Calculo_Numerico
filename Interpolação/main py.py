import math

def produto_lagrange(x, xi, n, pontos, excluir):
    """Calcula o produto para o método de Lagrange"""
    prod = 1.0
    for j in range(n):
        if j != excluir:
            prod *= (x - pontos[j][0]) / (xi - pontos[j][0])
    return prod

def lagrange(x, n, pontos):
    """Método de Lagrange para interpolação"""
    resultado = 0.0
    for i in range(n):
        resultado += pontos[i][1] * produto_lagrange(x, pontos[i][0], n, pontos, i)
    return resultado

def calcular_diferencas_divididas(n, pontos, diferencas):
    """Calcula as diferenças divididas para Newton"""
    # Inicializa com os valores de y
    for i in range(n):
        diferencas[i] = pontos[i][1]
    
    # Calcula diferenças divididas
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            diferencas[i] = (diferencas[i] - diferencas[i-1]) / (pontos[i][0] - pontos[i-j][0])

def newton(x, n, pontos, diferencas):
    """Método de Newton para interpolação"""
    resultado = diferencas[0]
    produto = 1.0
    
    for i in range(1, n):
        produto *= (x - pontos[i-1][0])
        resultado += diferencas[i] * produto
    
    return resultado

def main():
    print("=== MÉTODOS DE INTERPOLAÇÃO POLINOMIAL ===")
    
    try:
        n = int(input("\nQuantos pontos de dados você tem? "))
        
        if n <= 0:
            print("Número inválido de pontos!")
            return
        
        pontos = []
        diferencas = [0.0] * n
        
        print("Digite os pontos (x y), um por linha:")
        for i in range(n):
            x_val, y_val = map(float, input(f"Ponto {i+1}: ").split())
            pontos.append([x_val, y_val])
        
        # Verifica se os valores de x são distintos
        for i in range(n):
            for j in range(i+1, n):
                if pontos[i][0] == pontos[j][0]:
                    print("Erro: Valores de x devem ser distintos!")
                    return
        
        x = float(input("Digite o valor de x para interpolar: "))
        
        # Método de Lagrange
        resultado_lagrange = lagrange(x, n, pontos)
        print(f"\nResultado pelo método de Lagrange: {resultado_lagrange:.6f}")
        
        # Método de Newton
        calcular_diferencas_divididas(n, pontos, diferencas)
        resultado_newton = newton(x, n, pontos, diferencas)
        print(f"Resultado pelo método de Newton: {resultado_newton:.6f}")
        
        # Verifica consistência entre métodos
        if abs(resultado_lagrange - resultado_newton) > 1e-6:
            print("Aviso: Os métodos produziram resultados diferentes!")
    
    except ValueError:
        print("Erro: Digite valores numéricos válidos!")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()