import os
from string import Template


def ajuste_por_extremos_com_residuos(x, y):
    x0, y0 = x[0], y[0]
    x1, y1 = x[-1], y[-1]
    
    if x1 == x0:
        raise ValueError("Divisão por zero: x0 e x1 são iguais.")
    
    b1 = (y1 - y0) / (x1 - x0)
    b0 = y0 - b1 * x0

    b0 = round(b0, 6)
    b1 = round(b1, 6)

    y_pred = [round(b0 + b1 * xi, 6) for xi in x]

    residuos = []
    soma_di = 0.0
    soma_di2 = 0.0

    for i, (xi, yi, ypi) in enumerate(zip(x, y, y_pred)):
        di = round(yi - ypi, 6)
        di2 = round(di ** 2, 6)
        soma_di += di
        soma_di2 += di2
        residuos.append({'i': i, 'x_i': xi, 'y_i': yi, 'P(x_i)': ypi, 'd_i': di, 'd_i^2': di2})

    return b0, b1, residuos, round(soma_di, 6), round(soma_di2, 6), y_pred


def minimos_quadrados_alternativo(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)

    numerador_b1 = (sum_y * sum_x) - n * sum_xy
    denominador_b1 = (sum_x ** 2) - n * sum_x2

    if denominador_b1 == 0:
        raise ValueError("Divisão por zero ao calcular b1")

    b1 = numerador_b1 / denominador_b1
    b0 = (sum_y - b1 * sum_x) / n

    b0 = round(b0, 6)
    b1 = round(b1, 6)

    y_pred = [round(b0 + b1 * xi, 6) for xi in x]

    residuos = []
    soma_di = 0.0
    soma_di2 = 0.0

    for i, (xi, yi, ypi) in enumerate(zip(x, y, y_pred)):
        di = round(yi - ypi, 6)
        di2 = round(di ** 2, 6)
        soma_di += di
        soma_di2 += di2
        residuos.append({'i': i, 'x_i': xi, 'y_i': yi, 'U(x_i)': ypi, 'd_i': di, 'd_i^2': di2})

    return b0, b1, residuos, round(soma_di, 6), round(soma_di2, 6), y_pred


def calcular_qualidade_ajuste(y, D):
    n = len(y)
    p = 2

    sum_y = sum(y)
    sum_y2 = sum(yi ** 2 for yi in y)

    denominador_r2 = sum_y2 - (1 / n) * (sum_y ** 2)
    if denominador_r2 == 0:
        raise ValueError("Divisão por zero ao calcular R²")

    R2 = 1 - (D / denominador_r2)
    variancia_residual = D / (n - p)

    return round(R2, 6), round(variancia_residual, 6)


def formatar_tabela_html(residuos, soma_di, soma_di2):
    cabecalhos = residuos[0].keys()
    html = '<table border="1" style="border-collapse: collapse;"><tr>'
    for h in cabecalhos:
        html += f'<th>{h}</th>'
    html += '</tr>'
    for linha in residuos:
        html += '<tr>' + ''.join(f'<td>{v}</td>' for v in linha.values()) + '</tr>'
   # html += f'</table><p><strong>Soma d_i:</strong> {soma_di}</p>'
    html += f'<p><strong>Soma d_i² (D):</strong> {soma_di2}</p>'
    return html


def criar_html_grafico(x, y, y_pred, metodo, resultados):
    pontos = [{'x': float(xi), 'y': float(yi)} for xi, yi in zip(x, y)]
    linha_ajuste = [{'x': float(xi), 'y': float(ypi)} for xi, ypi in zip(x, y_pred)]

    html_template = Template('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ajuste - $metodo</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .equacao { font-size: 1.2em; margin-bottom: 10px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #aaa; padding: 6px; text-align: center; }
            th { background-color: #eee; }
        </style>
    </head>
    <body>
        <h1>Ajuste por $metodo</h1>
        <div class="equacao">$equacao</div>
        $resultados
        <div id="grafico" style="height: 500px;"></div>

        <script>
            const pontos = $pontos;
            const linha = $linha_ajuste;

            const trace1 = {
                x: pontos.map(p => p.x),
                y: pontos.map(p => p.y),
                mode: 'markers',
                type: 'scatter',
                name: 'Pontos',
                marker: { color: 'red', size: 8 }
            };

            const trace2 = {
                x: linha.map(p => p.x),
                y: linha.map(p => p.y),
                mode: 'lines',
                type: 'scatter',
                name: 'Reta Ajustada',
                line: { color: 'blue', width: 3 }
            };

            const layout = {
                title: '$metodo',
                xaxis: { title: 'x' },
                yaxis: { title: 'y' }
            };

            Plotly.newPlot('grafico', [trace1, trace2], layout);
        </script>
    </body>
    </html>
    ''')

    html = html_template.substitute({
        'metodo': metodo,
        'equacao': resultados['equacao'],
        'resultados': resultados['detalhes'],
        'pontos': str(pontos).replace("'x'", 'x').replace("'y'", 'y'),
        'linha_ajuste': str(linha_ajuste).replace("'x'", 'x').replace("'y'", 'y')
    })

    os.makedirs("graficos", exist_ok=True)
    caminho = f"graficos/{metodo.lower().replace(' ', '_')}.html"
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(html)

    return caminho


def main():
    print("======= AJUSTE DE CURVAS =======")

    while True:
        try:
            n = int(input("Quantidade de pontos (mínimo 2, 0 para sair): "))
            if n == 0:
                print("Encerrando...")
                return
            if n < 2:
                print("Insira pelo menos 2 pontos.")
                continue
            break
        except ValueError:
            print("Digite um número inteiro válido.")

    x = []
    y = []
    print("Digite os pontos (x y):")
    for i in range(n):
        while True:
            try:
                entrada = input(f"Ponto {i+1}: ").split()
                xi, yi = map(float, entrada)
                x.append(xi)
                y.append(yi)
                break
            except:
                print("Entrada inválida. Digite dois números separados por espaço.")

    while True:
        print("\n===== MENU =====")
        print("1. Mínimos Quadrados (com fórmula personalizada)")
        print("2. Ajuste por Extremos (1º grau)")
        print("3. Qualidade do Ajuste (R² e Variância Residual)")
        print("4. Sair")

        opcao = input("Escolha (1-4): ").strip()

        if opcao == '1':
            b0, b1, residuos, soma_di, soma_di2, y_pred = minimos_quadrados_alternativo(x, y)
            print(f"\nEquação ajustada: U(x) = {b0} + {b1}x")
            print(f"Soma dos quadrados dos resíduos: D = {soma_di2}")
            html = formatar_tabela_html(residuos, soma_di, soma_di2)

            resultados = {
                'equacao': f"U(x) = {b0} + {b1}x",
                'detalhes': html
            }
            caminho = criar_html_grafico(x, y, y_pred, "Minimos Quadrados", resultados)
            print(f"Arquivo HTML gerado: {caminho}")

        elif opcao == '2':
            b0, b1, residuos, soma_di, soma_di2, y_pred = ajuste_por_extremos_com_residuos(x, y)
            print(f"\nEquação ajustada: P(x) = {b1}x + {b0}")
            print(f"Soma dos quadrados dos resíduos: D = {soma_di2}")
            html = formatar_tabela_html(residuos, soma_di, soma_di2)

            resultados = {
                'equacao': f"P(x) = {b1}x + {b0}",
                'detalhes': html
            }
            caminho = criar_html_grafico(x, y, y_pred, "Ajuste por Extremos", resultados)
            print(f"Arquivo HTML gerado: {caminho}")

        elif opcao == '3':
            b0, b1, _, _, D, y_pred = minimos_quadrados_alternativo(x, y)
            R2, var = calcular_qualidade_ajuste(y, D)
            print(f"\nR² = {R2}")
            print(f"Variância Residual = {var}")

        elif opcao == '4':
            print("Encerrando...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()