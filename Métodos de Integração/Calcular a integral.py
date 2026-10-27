from sympy import symbols, integrate, sympify
from sympy.core.sympify import SympifyError

def resolver_integral():
    print("=== Calculadora de Integrais Definidas ===")
    expr_str = input("Digite a função f(x): ")
    a = float(input("Limite inferior (a): "))
    b = float(input("Limite superior (b): "))

    x = symbols('x')
    try:
        expr = sympify(expr_str)
        resultado = integrate(expr, (x, a, b))
        print(f"\n∫ de {a} até {b} de {expr_str} dx = {resultado.evalf():.8f}")
    except SympifyError:
        print("Erro: expressão inválida.")
    except Exception as e:
        print(f"Erro ao calcular a integral: {e}")

if __name__ == "__main__":
    resolver_integral()
