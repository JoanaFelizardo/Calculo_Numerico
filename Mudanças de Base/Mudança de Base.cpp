#include <iostream>
#include <cmath>
#include <cstring>

using namespace std;

void decimalInteiroParaBinario(int numero) {
    if (numero == 0) {
        cout << "Binário: 0\n";
        return;
    }

    char binario[32];
    int i = 0;

    while (numero > 0) {
        binario[i++] = (numero % 2) + '0';
        numero /= 2;
    }

    cout << "Binário (inteiro): ";
    for (int j = i - 1; j >= 0; j--) {
        cout << binario[j];
    }
    cout << "\n";
}

void decimalComPontoParaBinario(double numero) {
    if (numero < 0) {
        cout << "Número negativo não suportado neste exemplo.\n";
        return;
    }

    int parte_inteira = (int)numero;
    double parte_fracionaria = numero - parte_inteira;

 
    char binario_int[64];
    int i = 0;
    if (parte_inteira == 0) {
        binario_int[i++] = '0';
    } else {
        while (parte_inteira > 0) {
            binario_int[i++] = (parte_inteira % 2) + '0';
            parte_inteira /= 2;
        }
    }

    cout << "Binário (com ponto): ";
    for (int j = i - 1; j >= 0; j--) {
        cout << binario_int[j];
    }

   
    cout << ".";

    int limite = 10;
    while (limite-- && parte_fracionaria > 0.0) {
        parte_fracionaria *= 2;
        int bit = (int)parte_fracionaria;
        cout << bit;
        parte_fracionaria -= bit;
    }

    cout << "\n";
}


double binarioComPontoParaDecimal(const char* binario) {
    double decimal = 0.0;
    int i = 0;

   
    while (binario[i] != '\0' && binario[i] != '.') {
        if (binario[i] != '0' && binario[i] != '1') {
            cout << "Erro: caractere inválido na parte inteira.\n";
            return -1;
        }
        decimal = decimal * 2 + (binario[i] - '0');
        i++;
    }

   
    if (binario[i] == '.') {
        i++;
        double peso = 0.5;
        while (binario[i] != '\0') {
            if (binario[i] != '0' && binario[i] != '1') {
                cout << "Erro: caractere inválido na parte fracionária.\n";
                return -1;
            }
            decimal += (binario[i] - '0') * peso;
            peso /= 2.0;
            i++;
        }
    }

    return decimal;
}


int main() {
    int opcao;

    do {
        cout << "\n==== CONVERSÃO DE BASE ====\n";
        cout << "1. Decimal Inteiro para Binário\n";
        cout << "2. Decimal com Ponto para Binário\n";
        cout << "3. Binário (com ou sem ponto) para Decimal\n";
        cout << "4. Sair\n";
        cout << "Escolha uma opção: ";
        cin >> opcao;

        switch (opcao) {
            case 1: {
                int numero;
                cout << "Digite um número inteiro: ";
                cin >> numero;
                if (numero < 0) {
                    cout << "Somente números inteiros positivos são permitidos.\n";
                } else {
                    decimalInteiroParaBinario(numero);
                }
                break;
            }

            case 2: {
                double numero;
                cout << "Digite um número decimal (ex: 3.75): ";
                cin >> numero;
                if (numero < 0) {
                    cout << "Número negativo não suportado neste exemplo.\n";
                } else {
                    decimalComPontoParaBinario(numero);
                }
                break;
            }

            case 3: {
                char binario[65];
                cout << "Digite um número binário (ex: 101.11): ";
                cin >> binario;
                double resultado = binarioComPontoParaDecimal(binario);
                if (resultado != -1)
                    cout << "Decimal: " << resultado << "\n";
                break;
            }

            case 4:
                cout << "Encerrando o programa...\n";
                break;

            default:
                cout << "Opção inválida. Tente novamente.\n";
        }

    } while (opcao != 4);

    return 0;
}
