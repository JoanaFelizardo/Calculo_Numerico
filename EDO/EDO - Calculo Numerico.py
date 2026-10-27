import math

def euler(f, x0, y0, h, n):
    xs, ys = [x0], [y0]
    x, y = x0, y0
    for _ in range(n):
        k1 = f(x, y)
        y = y + h * k1
        x = x + h
        xs.append(x)
        ys.append(y)
    return xs, ys

def rk2(f, x0, y0, h, n):
    xs, ys = [x0], [y0]
    x, y = x0, y0
    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h, y + h * k1)
        y = y + h * (k1 + k2) / 2
        x = x + h
        xs.append(x)
        ys.append(y)
    return xs, ys

def rk4(f, x0, y0, h, n):
    xs, ys = [x0], [y0]
    x, y = x0, y0
    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h/2, y + h * k1/2)
        k3 = f(x + h/2, y + h * k2/2)
        k4 = f(x + h, y + h * k3)
        y = y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x = x + h
        xs.append(x)
        ys.append(y)
    return xs, ys

if __name__ == "__main__":
    print("=== Solução de Equacoes Diferenciais Ordinarias ===")
    
    raw_expr = input("Digite f(x,y): ").strip()
    if not raw_expr:
        print("INVALIDO!")
        exit()
    
    expr = raw_expr.replace('^', '**')
    def f_user(x, y):
        local_vars = {
            'x': x, 'y': y, 
            'e': math.e, 'pi': math.pi,
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'log': math.log, 'exp': math.exp, 'sqrt': math.sqrt
        }
       
        return eval(expr, {"__builtins__": None}, local_vars)

    try:
        x0 = float(input("Digite o valor inicial de x (x0): "))
        y0 = float(input("Digite o valor inicial de y (y(x0)): "))
        xf = float(input("Digite o valor final de x (x_final): "))
    except ValueError:
        print("ERRO. SAINDO.")
        exit()

    if xf < x0:
        # X final deve ser maior ou igual a x0
        print("ERRO. SAINDO.")
        exit()

    print("\nDefinição do passo:")
    print("1 - Usar número de passos (n)")
    print("2 - Usar tamanho do passo (h)")
    step_option = input("Escolha uma opcao: ")

    n_steps = 0
    h_step = 0.0

    if step_option == '1':
        try:
            n_steps = int(input("Digite o número de passos (n, inteiro >= 1): "))
            if n_steps < 1:
                print("ERRO. SAINDO.")
                exit()
        except ValueError:
            print("ERRO. SAINDO.")
            exit()
        h_step = (xf - x0) / n_steps
    elif step_option == '2':
        try:
            h_input = float(input("Digite o tamanho do passo (h): "))
            if h_input <= 0:
                print("ERRO. SAINDO.")
                exit()
        except ValueError:
            print("ERRO. SAINDO.")
            exit()
        
        n_steps = int((xf - x0) / h_input)
        if n_steps < 1 and xf > x0: 
            n_steps = 1
        elif xf == x0: 
            n_steps = 0
        h_step = (xf - x0) / n_steps if n_steps > 0 else 0.0 
        
        print(f"Número de passos (n) ajustado para: {n_steps}, Tamanho do passo (h) ajustado para: {h_step:.6f}")
    else:
        print("Opção de passo inválida. Saindo.")
        exit()

    print("\nEscolha o método de resolução:")
    print("1 - Euler (RK1)")
    print("2 - Runge-Kutta de 2ª Ordem")
    print("3 - Runge-Kutta de 4ª Ordem")
    method_choice = input("Método (1/2/3): ")

    results_xs = []
    results_ys = []

    if method_choice == '1':
        results_xs, results_ys = euler(f_user, x0, y0, h_step, n_steps)
    elif method_choice == '2':
        results_xs, results_ys = rk2(f_user, x0, y0, h_step, n_steps)
    elif method_choice == '3':
        results_xs, results_ys = rk4(f_user, x0, y0, h_step, n_steps)
    else:
        print("Opção de método inválida. Saindo.")
        exit()

    print("\n--- Resultados ---")
    print(" i |    x_i     |    y_i")
    print("---+------------+------------")
    for i, (xi, yi) in enumerate(zip(results_xs, results_ys)):
        print(f"{i:2d} | {xi:10.6f} | {yi:10.6f}")

    if results_ys: 
        print(f"\nValor final: Linha {n_steps} ==> y = {results_ys[-1]:.10f}")
    else:
        print("\nNenhum cálculo realizado.")