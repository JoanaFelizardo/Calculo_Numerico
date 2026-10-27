#include <iostream>
#include <cmath>
#include <iomanip>
#include <sstream>
#include <algorithm>  

using namespace std;


double produto_termos(double x, double x_vals[], int n) {
    double prod = 1.0;
    for (int i = 0; i <= n; i++) {
        prod *= (x - x_vals[i]);
    }
    return prod;
}

long long fatorial(int n) {
    long long fat = 1;
    for (int i = 2; i <= n; i++) fat *= i;
    return fat;
}

// 1. Erro de truncamento
double erro_truncamento(double x, double x_vals[], int n) {
    double derivada;
    cout << "Digite o valor da derivada de ordem " << n + 1 << " no ponto xi: ";
    cin >> derivada;

    double prod = produto_termos(x, x_vals, n);
    long long fat = fatorial(n + 1);

    return (derivada / fat) * prod;
}

// 2. Erro absoluto
double erro_absoluto(double x_real, double x_exp) {
    return fabs(x_real - x_exp);
}

// 3. Erro relativo
double erro_relativo(double erro_abs, double x_real) {
    return erro_abs / fabs(x_real);
}

// 4. Erro percentual
double erro_percentual(double erro_rel) {
    return erro_rel * 100.0;
}
bool testa_representacao(double numero, int b, int t, int e1, int e2) {
    if (numero == 0) return false; // zero não é representado em forma normalizada

    int expoente = 0;
    double mantissa = fabs(numero);

    // Normaliza o número: transforma em m * b^e com 1 <= m < b
    while (mantissa >= b) {
        mantissa /= b;
        expoente++;
    }
    while (mantissa < 1.0) {
        mantissa *= b;
        expoente--;
    }

    // Conta os dígitos significativos da mantissa (sem ponto)
    ostringstream oss;
    oss << fixed << setprecision(t + 5) << mantissa;
    string mant_str = oss.str();
    mant_str.erase(remove(mant_str.begin(), mant_str.end(), '.'), mant_str.end());

    // Remove zeros à esquerda
    int digitos = 0;
    for (char c : mant_str) {
        if (c != '0') digitos++;
        if (digitos > 0 && digitos <= t) continue;
        if (digitos > t) break;
    }

    return (expoente >= e1 && expoente <= e2 && digitos <= t);
}

// 5. Representação em ponto flutuante
void ponto_flutuante() {
    int b, t, e1, e2;
    cout << "Digite a base b: ";
    cin >> b;
    cout << "Digite o tamanho da mantissa t: ";
    cin >> t;
    cout << "Digite o expoente mínimo e1: ";
    cin >> e1;
    cout << "Digite o expoente máximo e2: ";
    cin >> e2;

    double xmin = pow(b, e1);
    double xmax = (1 - pow(b, -t)) * pow(b, e2 + 1);
    long long total = 2 * (b - 1) * pow(b, t - 1) * (e2 - e1 + 1) + 1;

    cout << fixed << setprecision(10);
    cout << "\nXmin = " << xmin << endl;
    cout << "Xmax = " << xmax << endl;
    cout << "Numero total de representacoes = " << total << endl;

    int qtd;
    cout << "\nQuantos números deseja testar? ";
    cin >> qtd;

    for (int i = 0; i < qtd; i++) {
        double numero;
        cout << "Digite o número " << (i + 1) << ": ";
        cin >> numero;

        if (testa_representacao(numero, b, t, e1, e2)) {
            cout << "✅ O número " << numero << " é ACEITO pela máquina.\n";
        } else {
            cout << "❌ O número " << numero << " NÃO é aceito pela máquina.\n";
        }
    }
}

int main() {
    int opcao;

    do {
        cout << "\n===== MENU =====\n";
        cout << "1. Erro de truncamento\n";
        cout << "2. Erro absoluto\n";
        cout << "3. Erro relativo\n";
        cout << "4. Erro percentual\n";
        cout << "5. Ponto Flutuante Completo (b, t, e1, e2)\n";
        cout << "0. Sair\n";
        cout << "Escolha uma opcao: ";
        cin >> opcao;

        switch(opcao) {
            case 1: {
                int n;
                double x;
                cout << "Digite a ordem n: ";
                cin >> n;
            
                double x_vals[20];
                for (int i = 0; i <= n; i++) {
                    cout << "Digite x[" << i << "]: ";
                    cin >> x_vals[i];
                }
            
                cout << "Digite o valor de x para avaliar o erro: ";
                cin >> x;
            
                double erro = erro_truncamento(x, x_vals, n);
                cout << "Erro de truncamento: " << erro << endl;
                break;
            }
            case 2: {
                double x_real, x_exp;
                cout << "Digite o valor real: ";
                cin >> x_real;
                cout << "Digite o valor experimental: ";
                cin >> x_exp;
                cout << "Erro absoluto: " << erro_absoluto(x_real, x_exp) << endl;
                break;
            }
            case 3: {
                double erro_abs, x_real;
                cout << "Digite o erro absoluto: ";
                cin >> erro_abs;
                cout << "Digite o valor real: ";
                cin >> x_real;
                cout << "Erro relativo: " << erro_relativo(erro_abs, x_real) << endl;
                break;
            }
            case 4: {
                double erro_rel;
                cout << "Digite o erro relativo: ";
                cin >> erro_rel;
                cout << "Erro percentual: " << erro_percentual(erro_rel) << "%" << endl;
                break;
            }
            
            case 5:
                ponto_flutuante();
                break;
            case 0:
                cout << "Saindo...\n";
                break;
            default:
                cout << "Opcao invalida!\n";
        }
    } while(opcao != 0);

    return 0;
}
