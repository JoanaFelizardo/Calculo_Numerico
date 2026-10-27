import math
from sympy import symbols, integrate, sympify, log as sympy_log
from sympy.core.sympify import SympifyError

def f_expr(expr):
    expr = expr.replace("ln(", "math.log(")
    return lambda x: eval(expr, {"x": x, "math": math})

def trap_composto(f, a, b, n):
    h = (b - a) / n
    soma = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        soma += f(a + i * h)
    return soma * h

def simpson_1_3(f, a, b, n):
    if n % 2 != 0 or n < 2:
        raise ValueError("n deve ser par e ≥ 2.")
    h = (b - a) / n
    soma = f(a) + f(b)
    for i in range(1, n):
        peso = 4 if i % 2 != 0 else 2
        soma += peso * f(a + i * h)
    return soma * h / 3

def simpson_3_8(f, a, b, n):
    if n % 3 != 0 or n < 3:
        raise ValueError("n deve ser múltiplo de 3 e ≥ 3.")
    h = (b - a) / n
    soma = f(a) + f(b)
    for i in range(1, n):
        peso = 2 if i % 3 == 0 else 3
        soma += peso * f(a + i * h)
    return soma * 3 * h / 8

def calcular_erros(valor_aproximado, valor_exato):
    erro_absoluto = abs(valor_exato - valor_aproximado)
    erro_relativo = erro_absoluto / abs(valor_exato) if valor_exato != 0 else float('inf')
    return erro_absoluto, erro_relativo

def calcular_integral_analitica(expr_str, a, b):
    x = symbols('x')
    try:
        expr_str_sympy = expr_str.replace("math.log(", "log(").replace("ln(", "log(")
        expr = sympify(expr_str_sympy)
        resultado = integrate(expr, (x, a, b))
        return resultado.evalf()
    except SympifyError:
        print("Erro: expressão inválida.")
        return None
    except Exception as e:
        print(f"Erro ao calcular a integral: {e}")
        return None

def aplicar_metodo_funcao():
    expr = input("Digite f(x) (ex: math.sin(x)+x**2 ou ln(x)): ")
    f = f_expr(expr)
    a = float(input("Limite inferior a: "))
    b = float(input("Limite superior b: "))

    valor_exato = calcular_integral_analitica(expr, a, b)
    if valor_exato is not None:
        print(f"\nValor exato da integral: {float(valor_exato):.8f}")

    print("\n1 - Trapézio\n2 - Simpson 1/3\n3 - Simpson 3/8")
    metodo = input("Escolha o método: ")

    print("\nVocê tem:\n1 - Número de subintervalos (n)\n2 - Tamanho do passo (h)")
    escolha = input("Escolha 1 ou 2: ")

    if escolha == '1':
        n = int(input("Digite o valor de n: "))
        h = (b - a) / n
    elif escolha == '2':
        h = float(input("Digite o valor de h: "))
        n = int((b - a) / h)
        if metodo == '2' and n % 2 != 0:
            n += 1
            print(f"n ajustado para {n} (par para Simpson 1/3).")
        elif metodo == '3' and n % 3 != 0:
            n += 3 - (n % 3)
            print(f"n ajustado para {n} (múltiplo de 3 para Simpson 3/8).")
        h = (b - a) / n
    else:
        print("Opção inválida.")
        return

    try:
        if metodo == '1':
            res = trap_composto(f, a, b, n)
        elif metodo == '2':
            res = simpson_1_3(f, a, b, n)
        elif metodo == '3':
            res = simpson_3_8(f, a, b, n)
        else:
            print("Método inválido.")
            return

        print(f"\nResultado numérico: ∫ f(x) dx ≈ {res:.8f} (n = {n}, h = {h:.6f})")

        if valor_exato is not None:
            erro_abs, erro_rel = calcular_erros(res, float(valor_exato))
            print(f"\nAnálise de erros:")
            print(f"Valor exato:   {float(valor_exato):.8f}")
            print(f"Erro absoluto: {erro_abs:.4e}")
            print(f"Erro relativo: {erro_rel:.4e}")

    except Exception as e:
        print("Erro:", e)

def aplicar_metodo_pontos():
    m = int(input("Quantos pontos x_i/y_i? "))
    xs, ys = [], []
    for i in range(m):
        xs.append(float(input(f"x[{i}] = ")))
        ys.append(float(input(f"y[{i}] = ")))

    n = len(xs) - 1
    if n < 1:
        print("É necessário pelo menos dois pontos.")
        return

    h = xs[1] - xs[0]
    for i in range(2, len(xs)):
        if abs((xs[i] - xs[i-1]) - h) > 1e-9:
            print("Erro: os pontos não têm espaçamento uniforme.")
            return

    print("\n1 - Trapézio\n2 - Simpson 1/3\n3 - Simpson 3/8")
    metodo = input("Escolha o método: ")

    try:
        if metodo == '1':
            soma = 0.5 * (ys[0] + ys[-1]) + sum(ys[1:-1])
            res = soma * h
        elif metodo == '2':
            if n % 2 != 0:
                raise ValueError("n deve ser par para Simpson 1/3.")
            soma = ys[0] + ys[-1]
            for i in range(1, n):
                soma += ys[i] * (4 if i % 2 != 0 else 2)
            res = soma * h / 3
        elif metodo == '3':
            if n % 3 != 0:
                raise ValueError("n deve ser múltiplo de 3 para Simpson 3/8.")
            soma = ys[0] + ys[-1]
            for i in range(1, n):
                soma += ys[i] * (2 if i % 3 == 0 else 3)
            res = soma * 3 * h / 8
        else:
            print("Método inválido.")
            return

        print(f"\nResultado pela tabela: ∫ ≈ {res:.8f} (n = {n}, h = {h:.6f})")

        tem_exato = input("\nVocê conhece o valor exato da integral? (s/n): ").lower()
        if tem_exato == 's':
            valor_exato = float(input("Digite o valor exato da integral: "))
            erro_abs, erro_rel = calcular_erros(res, valor_exato)
            print(f"\nAnálise de erros:")
            print(f"Valor exato:   {valor_exato:.8f}")
            print(f"Erro absoluto: {erro_abs:.4e}")
            print(f"Erro relativo: {erro_rel:.4e}")

    except Exception as e:
        print("Erro:", e)

def calcular_integral_analitica_menu():
    print("\n=== Calculadora de Integrais Definidas ===")
    expr_str = input("Digite a função f(x): ")
    a = float(input("Limite inferior (a): "))
    b = float(input("Limite superior (b): "))

    resultado = calcular_integral_analitica(expr_str, a, b)
    if resultado is not None:
        print(f"\n∫ de {a} até {b} de {expr_str} dx = {resultado:.8f}")

def menu_principal():
    while True:
        print("\n=== INTEGRAÇÃO NUMÉRICA ===")
        print("0 - Sair")
        print("1 - Calcular por função f(x)")
        print("2 - Calcular por tabela de pontos (x e y)")
        print("3 - Calcular integral analiticamente")
        op = input("Escolha uma opção: ")

        if op == '0':
            print("Encerrando...")
            break
        elif op == '1':
            aplicar_metodo_funcao()
        elif op == '2':
            aplicar_metodo_pontos()
        elif op == '3':
            calcular_integral_analitica_menu()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()