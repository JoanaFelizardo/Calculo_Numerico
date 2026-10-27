import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math
import time

# Variável global para a expressão da função
f_expr = None

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

def metodo_bissecao(f, a, b, tolerancia):
    """Implementa o método da bisseção"""
    inicio = time.time()
    tabela = []
    iteracoes = 0
    
    # Verifica se há mudança de sinal
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        print(f"\nErro: f({a}) = {fa:.6f}, f({b}) = {fb:.6f}")
        print("A função não muda de sinal no intervalo dado.")
        return None, []

    while (b - a)/2 > tolerancia:
        iteracoes += 1
        c = (a + b)/2
        fc = f(c)
        tabela.append([iteracoes, a, b, c, fc, abs(b - a)/2])
        
        if fc == 0:
            break
        elif fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    raiz = (a + b)/2
    print(f"\nRaiz encontrada: {raiz:.8f}")
    print(f"Iterações: {iteracoes}")
    print(f"Tempo de execução: {time.time() - inicio:.6f} segundos")
    return raiz, tabela

def metodo_newton(f, df, x0, tolerancia):
    """Implementa o método de Newton"""
    inicio = time.time()
    tabela = []
    iteracoes = 0
    
    while True:
        iteracoes += 1
        fx = f(x0)
        dfx = df(x0)
        
        if dfx == 0:
            print("\nErro: derivada zerou. Método falhou.")
            return None, []
            
        x1 = x0 - fx/dfx
        erro = abs(x1 - x0)
        tabela.append([iteracoes, x0, fx, erro])
        
        if erro < tolerancia:
            break
            
        x0 = x1
    
    print(f"\nRaiz encontrada: {x1:.8f}")
    print(f"Iterações: {iteracoes}")
    print(f"Tempo de execução: {time.time() - inicio:.6f} segundos")    
    return x1, tabela

def metodo_secante(f, x0, x1, tolerancia):
    """Implementa o método da secante"""
    inicio = time.time()
    tabela = []
    iteracoes = 0
    
    while True:
        iteracoes += 1
        fx0 = f(x0)
        fx1 = f(x1)
        
        if abs(fx1 - fx0) < 1e-12:
            break
            
        x2 = x1 - fx1 * (x1 - x0)/(fx1 - fx0)
        erro = abs(x2 - x1)
        tabela.append([iteracoes, x1, fx1, erro])
        
        if erro < tolerancia:
            break
            
        x0, x1 = x1, x2
    
    print(f"\nRaiz encontrada: {x2:.8f}")
    print(f"Iterações: {iteracoes}")
    print(f"Tempo de execução: {time.time() - inicio:.6f} segundos")
    return x2, tabela

def gerar_html_resultado(f, resultado, metodo, nome_arquivo):
    """Gera HTML com os resultados do método numérico"""
    raiz, tabela = resultado if resultado else (None, [])
    intervalo = [min([linha[1] for linha in tabela] or [0]),
                max([linha[2] for linha in tabela] or [1])] if metodo == "Bisseção" else (
                [min([linha[1] for linha in tabela] or [0])-1,
                 max([linha[1] for linha in tabela] or [0])+1])
    
    img_base64 = criar_grafico_base(f, intervalo, raiz)
    
    cabecalhos = {
        "Bisseção": ["Iteração", "a", "b", "x", "f(x)", "Erro"],
        "Newton": ["Iteração", "x", "f(x)", "Erro"],
        "Secante": ["Iteração", "x", "f(x)", "Erro"]
    }
    
    tabela_html = ""
    if tabela:
        tabela_html = "<table><tr>" + "".join(f"<th>{h}</th>" for h in cabecalhos[metodo]) + "</tr>"
        for linha in tabela:
            tabela_html += "<tr>" + "".join(f"<td>{item:.6f}</td>" if isinstance(item, (float, int)) else f"<td>{item}</td>" for item in linha) + "</tr>"
        tabela_html += "</table>"
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Resultado - Método {metodo}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        img {{ max-width: 100%; height: auto; }}
        .info {{ margin: 20px 0; padding: 15px; background-color: #f0f0f0; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 8px; text-align: center; border: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; }}
        .error {{ color: red; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Método {metodo}</h1>
        
        <div class="info">
            <h2>Resultados</h2>
            <p>Função: {str(f_expr)}</p>
            {"<p>Raiz aproximada: " + f"{raiz:.8f}</p>" if raiz is not None else '<p class="error">Não foi possível encontrar a raiz</p>'}
        </div>
        
        <h2>Gráfico com Raiz Encontrada</h2>
        <img src="data:image/png;base64,{img_base64}" alt="Gráfico com raiz">
        
        {"<h2>Tabela de Iterações</h2>" + tabela_html if tabela else ""}
        
        <div class="info">
            <h3>Sobre o Método</h3>
            <p>{"Divide o intervalo ao meio até convergir para a raiz." if metodo == "Bisseção" 
                else "Usa derivadas para convergência mais rápida." if metodo == "Newton" 
                else "Aproxima a derivada usando quocientes."}</p>
        </div>
    </div>
</body>
</html>
"""
    with open(nome_arquivo, 'w') as file:
        file.write(html)
    print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")

def main():
    global f_expr
    
    print("\nANÁLISE DE RAÍZES DE FUNÇÕES")
    print("---------------------------")
    
    # Entrada da função
    expr_str = input("Digite a função em x (use x como variável, ex: x**2 - 2): ").replace('^', '**')
    try:
        x = sp.symbols('x')
        f_expr = sp.sympify(expr_str)
        f = sp.lambdify(x, f_expr, 'numpy')
    except:
        print("\nExpressão inválida! Use x como variável e operadores matemáticos padrão.")
        return

    # Gera gráfico inicial
    print("\nGráfico inicial (-5 a 5)")
    try:
        gerar_html_grafico(f, [-5, 5])
    except:
        print("Não foi possível gerar o gráfico para o intervalo padrão.")
        return

    while True:
        print("\nEscolha o método:")
        print("1. Método da Bisseção")
        print("2. Método de Newton")
        print("3. Método da Secante")
        print("4. Sair")
        
        opcao = input("Sua escolha (1-4): ")
        
        if opcao == '4':
            break
            
        try:
            if opcao == '1':
                print("\nMétodo da Bisseção")
                a = float(input("Limite inferior (a): "))
                b = float(input("Limite superior (b): "))
                tol = float(input("Tolerância (ex: 0.0001): "))
                
                resultado = metodo_bissecao(f, a, b, tol)
                gerar_html_resultado(f, resultado, "Bisseção", "resultado_bissecao.html")
                
            elif opcao == '2':
                print("\nMétodo de Newton")
                x0 = float(input("Valor inicial (x0): "))
                tol = float(input("Tolerância (ex: 0.0001): "))
                
                # Calcula derivada
                df_expr = sp.diff(f_expr, x)
                df = sp.lambdify(x, df_expr, 'numpy')
                
                resultado = metodo_newton(f, df, x0, tol)
                gerar_html_resultado(f, resultado, "Newton", "resultado_newton.html")
                
            elif opcao == '3':
                print("\nMétodo da Secante")
                x0 = float(input("Primeiro valor inicial (x0): "))
                x1 = float(input("Segundo valor inicial (x1): "))
                tol = float(input("Tolerância (ex: 0.0001): "))
                
                resultado = metodo_secante(f, x0, x1, tol)
                gerar_html_resultado(f, resultado, "Secante", "resultado_secante.html")
                
            else:
                print("\nOpção inválida! Escolha 1, 2, 3 ou 4.")
        except Exception as e:
            print(f"\nErro: {str(e)}")

if __name__ == "__main__":
    main()
