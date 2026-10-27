import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math
import time

def criar_grafico_base(f, intervalo, raiz=None):
    """Cria o gráfico base da função e retorna como imagem em base64"""
    x_vals = np.linspace(intervalo[0], intervalo[1], 400)
    y_vals = [f(x) for x in x_vals]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label='f(x)')
    plt.axhline(0, color='black', linewidth=0.5)
    
    if raiz is not None:
        plt.scatter([raiz], [0], color='red', label='Raiz aproximada')
    
    plt.title('Gráfico da Função')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    
    # Salva a imagem em memória
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    
    # Converte para base64
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return img_base64

def gerar_html_grafico(f, intervalo, nome_arquivo="grafico_funcao.html"):
    """Gera o HTML com o gráfico da função"""
    img_base64 = criar_grafico_base(f, intervalo)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gráfico da Função</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            img {{ max-width: 100%; height: auto; }}
            .info {{ margin-top: 20px; padding: 15px; background-color: #f0f0f0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Gráfico da Função</h1>
            <img src="data:image/png;base64,{img_base64}" alt="Gráfico da função">
            <div class="info">
                <p>Função: {str(f_expr)}</p>
                <p>Intervalo: [{intervalo[0]}, {intervalo[1]}]</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(nome_arquivo, 'w') as file:
        file.write(html)
    
    print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")

def bissecao(funcao, a, b, tolerancia):
    """Implementação do método da bisseção"""
    inicio_tempo = time.time()

    # Função anônima para avaliação
    f = lambda x: eval(funcao, {"__builtins__": None}, {
        "x": x,
        "e": math.e,
        "pi": math.pi,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "sqrt": math.sqrt
    })

    # Verifica se há mudança de sinal no intervalo
    if f(a) * f(b) > 0:
        print("Erro: a função não muda de sinal no intervalo dado.")
        return None

    iteracoes = 0
    while abs(b - a) / 2 > tolerancia:
        iteracoes += 1
        meio = (a + b) / 2
        if f(meio) == 0:
            a = b = meio
            break
        elif f(a) * f(meio) < 0:
            b = meio
        else:
            a = meio

    raiz = (a + b) / 2
    fim_tempo = time.time()
    tempo_execucao = fim_tempo - inicio_tempo

    print("\n=== Resultado ===")
    print(f"Raiz aproximada: {raiz:.15f}")
    print(f"Interações: {iteracoes}")
    print(f"Tolerância: {tolerancia}")
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")

    return raiz

def metodo_newton(f, df, x0, tol):
    """Implementação do método de Newton"""
    tabela = []
    iteracoes = 0
    x = x0
    
    while True:
        fx = f(x)
        dfx = df(x)
        delta_x = -fx / dfx
        x += delta_x
        iteracoes += 1
        
        tabela.append([iteracoes, x, fx, abs(delta_x)])
        
        if abs(delta_x) < tol and abs(fx) < tol:
            break
    
    return x, iteracoes, tabela

def metodo_secante(f, x0, x1, tol):
    """Implementação do método da secante"""
    tabela = []
    iteracoes = 0
    fx0 = f(x0)
    
    while True:
        fx1 = f(x1)
        if abs(fx1 - fx0) < 1e-12:
            break
            
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        iteracoes += 1
        
        tabela.append([iteracoes, x1, fx1, abs(x1 - x0)])
        
        if abs(x2 - x1) < tol and abs(fx1) < tol:
            break
            
        x0, x1 = x1, x2
        fx0 = fx1
    
    return x2, iteracoes, tabela

def gerar_html_metodo(f, raiz, iteracoes, tabela, metodo, intervalo, nome_arquivo):
    """Gera o HTML específico para cada método"""
    img_base64 = criar_grafico_base(f, intervalo, raiz)
    
    # Cria a tabela HTML
    tabela_html = "<table border='1'><tr>"
    
    if metodo == "Bisseção":
        headers = ["Iteração", "a", "b", "x", "f(x)", "Erro"]
    elif metodo == "Newton":
        headers = ["Iteração", "x", "f(x)", "Erro"]
    else:
        headers = ["Iteração", "x", "f(x)", "Erro"]
    
    for header in headers:
        tabela_html += f"<th>{header}</th>"
    tabela_html += "</tr>"
    
    for linha in tabela:
        tabela_html += "<tr>"
        for item in linha:
            tabela_html += f"<td>{item:.6f}</td>" if isinstance(item, (float, int)) else f"<td>{item}</td>"
        tabela_html += "</tr>"
    tabela_html += "</table>"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Método {metodo}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            img {{ max-width: 100%; height: auto; }}
            .info {{ margin: 20px 0; padding: 15px; background-color: #f0f0f0; border-radius: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 8px; text-align: center; border: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Método {metodo}</h1>
            
            <div class="info">
                <h2>Resultados</h2>
                <p>Função: {str(f_expr)}</p>
                <p>Raiz aproximada: {raiz:.8f}</p>
                <p>Número de iterações: {iteracoes}</p>
            </div>
            
            <h2>Gráfico com Raiz Encontrada</h2>
            <img src="data:image/png;base64,{img_base64}" alt="Gráfico com raiz">
            
            <h2>Tabela de Iterações</h2>
            {tabela_html}
            
            <div class="info">
                <h3>Sobre o Método {metodo}</h3>
                <p>{"O método da bisseção divide o intervalo ao meio repetidamente até encontrar a raiz." if metodo == "Bisseção" else ""}</p>
                <p>{"O método de Newton usa a derivada da função para convergir mais rapidamente para a raiz." if metodo == "Newton" else ""}</p>
                <p>{"O método da secante é uma variação do método de Newton que não requer o cálculo da derivada." if metodo == "Secante" else ""}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(nome_arquivo, 'w') as file:
        file.write(html)
    
    print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")

# Programa principal
print("ANÁLISE DE RAÍZES DE FUNÇÕES")
print("----------------------------")

# Entrada da função
expr_str = input("Digite a função em x (ex: x**3 - x - 2): ")
x = sp.symbols('x')
try:
    f_expr = sp.sympify(expr_str)
    f = sp.lambdify(x, f_expr, 'numpy')
except:
    print("Expressão inválida. Por favor, execute novamente.")
    exit()

# Determinar intervalo automaticamente
intervalo = [-5, 5]  # Intervalo padrão
gerar_html_grafico(f, intervalo)

# Menu de métodos
print("\nEscolha o método para encontrar a raiz:")
print("1 - Método da Bisseção")
print("2 - Método de Newton")
print("3 - Método da Secante")

while True:
    escolha = input("Digite sua escolha (1-3): ")
    
    if escolha == '1':
        # Método da Bisseção
        a = float(input("Digite o limite inferior do intervalo (a): "))
        b = float(input("Digite o limite superior do intervalo (b): "))
        tol = float(input("Digite a tolerância (ex: 1e-5): "))
        
        try:
            raiz = bissecao(expr_str, a, b, tol)
            gerar_html_metodo(f, raiz, None, None, "Bisseção", [a, b], "resultado_bissecao.html")
        except ValueError as e:
            print(f"Erro: {e}")
        break
        
    elif escolha == '2':
        # Método de Newton
        x0 = float(input("Digite o valor inicial (x0): "))
        tol = float(input("Digite a tolerância (ex: 1e-5): "))
        
        df_expr = sp.diff(f_expr, x)
        df = sp.lambdify(x, df_expr, 'numpy')
        
        raiz, iteracoes, tabela = metodo_newton(f, df, x0, tol)
        gerar_html_metodo(f, raiz, iteracoes, tabela, "Newton", [x0-3, x0+3], "resultado_newton.html")
        break
        
    elif escolha == '3':
        # Método da Secante
        x0 = float(input("Digite o primeiro valor inicial (x0): "))
        x1 = float(input("Digite o segundo valor inicial (x1): "))
        tol = float(input("Digite a tolerância (ex: 1e-5): "))
        
        raiz, iteracoes, tabela = metodo_secante(f, x0, x1, tol)
        gerar_html_metodo(f, raiz, iteracoes, tabela, "Secante", [min(x0,x1)-2, max(x0,x1)+2], "resultado_secante.html")
        break
        
    else:
        print("Opção inválida. Por favor, escolha 1, 2 ou 3.")
