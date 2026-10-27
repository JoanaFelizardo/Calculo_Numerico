import math

def produto_termos(x, x_vals, n):
    """Calcula o produto dos termos (x - x_i)"""
    prod = 1.0
    for i in range(n + 1):
        prod *= (x - x_vals[i])
    return prod

def fatorial(n):
    """Calcula o fatorial de n"""
    fat = 1
    for i in range(2, n + 1):
        fat *= i
    return fat

def erro_truncamento(x, x_vals, n):
    """Calcula o erro de truncamento"""
    derivada = float(input(f"Digite o valor da derivada de ordem {n + 1} no ponto xi: "))
    
    prod = produto_termos(x, x_vals, n)
    fat = fatorial(n + 1)
    
    return (derivada / fat) * prod

def erro_absoluto(x_real, x_exp):
    """Calcula o erro absoluto"""
    return abs(x_real - x_exp)

def erro_relativo(erro_abs, x_real):
    """Calcula o erro relativo"""
    return erro_abs / abs(x_real)

def erro_percentual(erro_rel):
    """Calcula o erro percentual"""
    return erro_rel * 100.0

def testa_representacao(numero, b, t, e1, e2):
    """Testa se um número pode ser representado no sistema de ponto flutuante"""
    if numero == 0:
        return False  # zero não é representado em forma normalizada
    
    expoente = 0
    mantissa = abs(numero)
    
    # Normaliza o número: transforma em m * b^e com 1 <= m < b
    while mantissa >= b:
        mantissa /= b
        expoente += 1
    while mantissa < 1.0:
        mantissa *= b
        expoente -= 1
    
    # Conta os dígitos significativos da mantissa
    mant_str = f"{mantissa:.{t + 5}f}".replace('.', '')
    
    # Remove zeros à esquerda
    digitos = 0
    for c in mant_str:
        if c != '0':
            digitos += 1
        if digitos > 0 and digitos <= t:
            continue
        if digitos > t:
            break
    
    return (expoente >= e1 and expoente <= e2 and digitos <= t)

def ponto_flutuante():
    """Sistema completo de ponto flutuante"""
    try:
        b = int(input("Digite a base b: "))
        t = int(input("Digite o tamanho da mantissa t: "))
        e1 = int(input("Digite o expoente mínimo e1: "))
        e2 = int(input("Digite o expoente máximo e2: "))
        
        xmin = math.pow(b, e1)
        xmax = (1 - math.pow(b, -t)) * math.pow(b, e2 + 1)
        total = 2 * (b - 1) * math.pow(b, t - 1) * (e2 - e1 + 1) + 1
        
        print(f"\nXmin = {xmin:.10f}")
        print(f"Xmax = {xmax:.10f}")
        print(f"Número total de representações = {int(total)}")
        
        qtd = int(input("\nQuantos números deseja testar? "))
        
        for i in range(qtd):
            numero = float(input(f"Digite o número {i + 1}: "))
            
            if testa_representacao(numero, b, t, e1, e2):
                print(f"✅ O número {numero} é ACEITO pela máquina.")
            else:
                print(f"❌ O número {numero} NÃO é aceito pela máquina.")
                
    except ValueError:
        print("Erro: Por favor, digite valores numéricos válidos.")

def main_erros():
    """Função principal para cálculos de erro"""
    while True:
        print("\n===== MENU =====")
        print("1. Erro de truncamento")
        print("2. Erro absoluto")
        print("3. Erro relativo")
        print("4. Erro percentual")
        print("5. Ponto Flutuante Completo (b, t, e1, e2)")
        print("0. Sair")
        
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida!")
            continue
        
        if opcao == 1:
            try:
                n = int(input("Digite a ordem n: "))
                x_vals = []
                for i in range(n + 1):
                    x_val = float(input(f"Digite x[{i}]: "))
                    x_vals.append(x_val)
                
                x = float(input("Digite o valor de x para avaliar o erro: "))
                erro = erro_truncamento(x, x_vals, n)
                print(f"Erro de truncamento: {erro}")
            except ValueError:
                print("Erro: Digite valores numéricos válidos.")
        
        elif opcao == 2:
            try:
                x_real = float(input("Digite o valor real: "))
                x_exp = float(input("Digite o valor experimental: "))
                print(f"Erro absoluto: {erro_absoluto(x_real, x_exp)}")
            except ValueError:
                print("Erro: Digite valores numéricos válidos.")
        
        elif opcao == 3:
            try:
                erro_abs = float(input("Digite o erro absoluto: "))
                x_real = float(input("Digite o valor real: "))
                print(f"Erro relativo: {erro_relativo(erro_abs, x_real)}")
            except ValueError:
                print("Erro: Digite valores numéricos válidos.")
        
        elif opcao == 4:
            try:
                erro_rel = float(input("Digite o erro relativo: "))
                print(f"Erro percentual: {erro_percentual(erro_rel)}%")
            except ValueError:
                print("Erro: Digite valores numéricos válidos.")
        
        elif opcao == 5:
            ponto_flutuante()
        
        elif opcao == 0:
            print("Saindo...")
            break
        
        else:
            print("Opção inválida!")