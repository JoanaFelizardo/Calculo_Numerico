def decimal_inteiro_para_binario(numero):
    """Converte número decimal inteiro para binário"""
    if numero == 0:
        print("Binário: 0")
        return
    
    binario = []
    num = numero
    
    while num > 0:
        binario.append(str(num % 2))
        num //= 2
    
    print("Binário (inteiro):", ''.join(reversed(binario)))

def decimal_com_ponto_para_binario(numero):
    """Converte número decimal com ponto para binário"""
    if numero < 0:
        print("Número negativo não suportado neste exemplo.")
        return
    
    parte_inteira = int(numero)
    parte_fracionaria = numero - parte_inteira
    
    # Parte inteira
    binario_int = []
    if parte_inteira == 0:
        binario_int.append('0')
    else:
        num_int = parte_inteira
        while num_int > 0:
            binario_int.append(str(num_int % 2))
            num_int //= 2
        binario_int.reverse()
    
    print("Binário (com ponto):", ''.join(binario_int), end=".")
    
    # Parte fracionária
    limite = 10
    while limite > 0 and parte_fracionaria > 0.0:
        parte_fracionaria *= 2
        bit = int(parte_fracionaria)
        print(bit, end="")
        parte_fracionaria -= bit
        limite -= 1
    
    print()

def binario_com_ponto_para_decimal(binario):
    """Converte número binário (com ou sem ponto) para decimal"""
    decimal = 0.0
    i = 0
    
    # Parte inteira
    while i < len(binario) and binario[i] != '.':
        if binario[i] not in ['0', '1']:
            print("Erro: caractere inválido na parte inteira.")
            return -1
        decimal = decimal * 2 + int(binario[i])
        i += 1
    
    # Parte fracionária
    if i < len(binario) and binario[i] == '.':
        i += 1
        peso = 0.5
        while i < len(binario):
            if binario[i] not in ['0', '1']:
                print("Erro: caractere inválido na parte fracionária.")
                return -1
            decimal += int(binario[i]) * peso
            peso /= 2.0
            i += 1
    
    return decimal

def main_mudanca_base():
    """Função principal para conversão de base"""
    while True:
        print("\n==== CONVERSÃO DE BASE ====")
        print("1. Decimal Inteiro para Binário")
        print("2. Decimal com Ponto para Binário")
        print("3. Binário (com ou sem ponto) para Decimal")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")
        
        try:
            opcao = int(opcao)
        except ValueError:
            print("Opção inválida. Tente novamente.")
            continue
        
        if opcao == 1:
            try:
                numero = int(input("Digite um número inteiro: "))
                if numero < 0:
                    print("Somente números inteiros positivos são permitidos.")
                else:
                    decimal_inteiro_para_binario(numero)
            except ValueError:
                print("Por favor, digite um número inteiro válido.")
        
        elif opcao == 2:
            try:
                numero = float(input("Digite um número decimal (ex: 3.75): "))
                if numero < 0:
                    print("Número negativo não suportado neste exemplo.")
                else:
                    decimal_com_ponto_para_binario(numero)
            except ValueError:
                print("Por favor, digite um número decimal válido.")
        
        elif opcao == 3:
            binario = input("Digite um número binário (ex: 101.11): ")
            resultado = binario_com_ponto_para_decimal(binario)
            if resultado != -1:
                print(f"Decimal: {resultado}")
        
        elif opcao == 4:
            print("Encerrando o programa...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")