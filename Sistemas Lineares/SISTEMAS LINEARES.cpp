#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

double** alocarMatriz(int num) {
    double** matriz = new double*[num];
    for(int i = 0; i < num; i++) {
        matriz[i] = new double[num]();
    }
    return matriz;
}

void liberarMemoria(double** matriz, int num) {
    for(int i = 0; i < num; i++) {
        delete[] matriz[i];
    }
    delete[] matriz;
}

void lerMatriz(double** matriz, double* vetor, int num) {
    cout << "Digite a Matriz A (" << num << "x" << num << "): " << endl;
    for(int i = 0; i < num; i++) {
        for(int j = 0; j < num; j++) {
            cin >> matriz[i][j];
        }
    }
    
    cout << "Digite o vetor b:";
    for(int i = 0; i < num; i++) {
        cin >> vetor[i];
    }
}

void mostrarVetor(double* x, int num) {
    cout << "Solução: " << endl;
    for(int i = 0; i < num; i++) {
        cout << "x[" << i << "] = " << fixed << setprecision(6) << x[i] << endl;
    }
    cout << endl;
}

// funcaao 1:
void gaussSimples(double** matriz, double* vetor, double* solucao, int num) {
    double** A = alocarMatriz(num);
    double* b = new double[num];
    
    for(int i = 0; i < num; i++) {
        b[i] = vetor[i];
        for(int j = 0; j < num; j++) {
            A[i][j] = matriz[i][j];
        }
    }

    for(int k = 0; k < num - 1; k++) {
        for(int i = k + 1; i < num; i++) {
            double m = A[i][k]/A[k][k];
            for(int j = k; j < num; j++) {
                A[i][j] -= m * A[k][j];
            }
            b[i] -= m * b[k];
        }
    }

    for(int i = num - 1; i >= 0; i--) {
        solucao[i] = b[i];
        for(int j = i + 1; j < num; j++) {
            solucao[i] -= A[i][j] * solucao[j];
        }
        solucao[i] /= A[i][i];
    }

    liberarMemoria(A, num);
    delete[] b;
}

//funcao 2:
void gaussPivotParcial(double** matriz, double* vetor, double* solucao, int num) {
    double** A = alocarMatriz(num);
    double* b = new double[num];
    
    for(int i = 0; i < num; i++) {
        b[i] = vetor[i];
        for(int j = 0; j < num; j++) {
            A[i][j] = matriz[i][j];
        }
    }

   
    for(int k = 0; k < num - 1; k++) {
      
        int max = k;
        for(int i = k + 1; i < num; i++) {
            if(fabs(A[i][k]) > fabs(A[max][k])) {
                max = i;
            }
        }
        if(max != k) {
            swap(A[k], A[max]);
            swap(b[k], b[max]);
        }

      
        for(int i = k + 1; i < num; i++) {
            double m = A[i][k]/A[k][k];
            for(int j = k; j < num; j++) {
                A[i][j] -= m * A[k][j];
            }
            b[i] -= m * b[k];
        }
    }

   
    for(int i = num - 1; i >= 0; i--) {
        solucao[i] = b[i];
        for(int j = i + 1; j < num; j++) {
            solucao[i] -= A[i][j] * solucao[j];
        }
        solucao[i] /= A[i][i];
    }

    liberarMemoria(A, num);
    delete[] b;
}

//funcao 3:
void decomposicaoLU(double** matriz, double** L, double** U, double* b, double* x, int num) {
   
    for(int i = 0; i < num; i++) {
        for(int j = 0; j < num; j++) {
            L[i][j] = (i == j) ? 1.0 : 0.0;
            U[i][j] = 0.0;
        }
    }

  
    for(int k = 0; k < num; k++) {
        U[k][k] = matriz[k][k];
        for(int i = k + 1; i < num; i++) {
            L[i][k] = matriz[i][k] / U[k][k];
            U[k][i] = matriz[k][i];
        }
        
        for(int i = k + 1; i < num; i++) {
            for(int j = k + 1; j < num; j++) {
                matriz[i][j] -= L[i][k] * U[k][j];
            }
        }
    }

   
    double* y = new double[num];
    for(int i = 0; i < num; i++) {
        y[i] = b[i];
        for(int j = 0; j < i; j++) {
            y[i] -= L[i][j] * y[j];
        }
    }

    
    for(int i = num - 1; i >= 0; i--) {
        x[i] = y[i];
        for(int j = i + 1; j < num; j++) {
            x[i] -= U[i][j] * x[j];
        }
        x[i] /= U[i][i];
    }

   
    cout << "Matriz L: " << endl;
    for(int i = 0; i < num; i++) {
        for(int j = 0; j < num; j++) {
            cout << setw(10) << L[i][j] << " ";
        }
        cout << endl;
    }
    
    cout << "Matriz U: " << endl;
    for(int i = 0; i < num; i++) {
        for(int j = 0; j < num; j++) {
            cout << setw(10) << U[i][j] << " ";
        }
        cout << endl;
    }

    delete[] y;
}

// funcao 4:
void decomposicaoLUPP(double** matriz, double** L, double** U, double* b, double* x, int num) {
    int* P = new int[num];
    for(int i = 0; i < num; i++) {
        P[i] = i;
    }

  
    for(int k = 0; k < num; k++) {
      
        int max = k;
        for(int i = k + 1; i < num; i++) {
            if(fabs(matriz[i][k]) > fabs(matriz[max][k])) {
                max = i;
            }
        }
        
        if(max != k) {
            swap(matriz[k], matriz[max]);
            swap(P[k], P[max]);
        }

        
        for(int i = k + 1; i < num; i++) {
            matriz[i][k] /= matriz[k][k];
            for(int j = k + 1; j < num; j++) {
                matriz[i][j] -= matriz[i][k] * matriz[k][j];
            }
        }
    }

  
    for(int i = 0; i < num; i++) {
        for(int j = 0; j < num; j++) {
            if(i > j) {
                L[i][j] = matriz[i][j];
                U[i][j] = 0.0;
            } else if(i == j) {
                L[i][j] = 1.0;
                U[i][j] = matriz[i][j];
            } else {
                L[i][j] = 0.0;
                U[i][j] = matriz[i][j];
            }
        }
    }

   
    double* Pb = new double[num];
    for(int i = 0; i < num; i++) {
        Pb[i] = b[P[i]];
    }

    
    double* y = new double[num];
    for(int i = 0; i < num; i++) {
        y[i] = Pb[i];
        for(int j = 0; j < i; j++) {
            y[i] -= L[i][j] * y[j];
        }
    }

    
    for(int i = num - 1; i >= 0; i--) {
        x[i] = y[i];
        for(int j = i + 1; j < num; j++) {
            x[i] -= U[i][j] * x[j];
        }
        x[i] /= U[i][i];
    }

   
    cout << "Matriz L: " << endl;
    for(int i = 0; i < num; i++) {
        for(int j = 0; j < num; j++) {
            cout << setw(10) << L[i][j] << " ";
        }
        cout << endl;
    }
    
    cout << "Matriz U: " << endl;
    for(int i = 0; i < num; i++) {
        for(int j = 0; j < num; j++) {
            cout << setw(10) << U[i][j] << " ";
        }
        cout << endl;
    }

    delete[] P;
    delete[] Pb;
    delete[] y;
}

int main() {
    int num, opcao;
    
    cout << "Digite a ordem da matriz: ";
    cin >> num;
    
    double** matriz = alocarMatriz(num);
    double** L = alocarMatriz(num);
    double** U = alocarMatriz(num);
    double* vetor = new double[num];
    double* solucao = new double[num]();
    
    lerMatriz(matriz, vetor, num);
    
    do {
        cout << "-----------------------------------" << endl;
        cout << "--- MENU ---" << endl;
        cout << "1. Eliminação de Gauss Simples;" << endl;
        cout << "2. Eliminação de Gauss com Pivotação Parcial;" endl;
        cout << "3. Decomposição LU;" << endl;
        cout << "4. Decomposição LU com Pivotação Parcial;" << endl;
        cout << "0. Sair." << endl;
        cout << "Escolha uma opção: ";
        cin >> opcao;
        
        
        fill(solucao, solucao + num, 0.0);
        
        switch(opcao) {
            
            case 1: {
                double** copiaA = alocarMatriz(num);
                double* copiaB = new double[num];
                
                for(int i = 0; i < num; i++) {
                    copiaB[i] = vetor[i];
                    for(int j = 0; j < num; j++) {
                        copiaA[i][j] = matriz[i][j];
                    }
                }
                
                gaussSimples(copiaA, copiaB, solucao, num);
                mostrarVetor(solucao, num);
                
                liberarMemoria(copiaA, num);
                delete[] copiaB;
                break;
            }
                
            case 2: {
                double** copiaA = alocarMatriz(num);
                double* copiaB = new double[num];
                
                for(int i = 0; i < num; i++) {
                    copiaB[i] = vetor[i];
                    for(int j = 0; j < num; j++) {
                        copiaA[i][j] = matriz[i][j];
                    }
                }
                
                gaussPivotParcial(copiaA, copiaB, solucao, num);
                mostrarVetor(solucao, num);
                
                liberarMemoria(copiaA, num);
                delete[] copiaB;
                break;
            }
                
            case 3: {
                double** copiaA = alocarMatriz(num);
                double* copiaB = new double[num];
                
                for(int i = 0; i < num; i++) {
                    copiaB[i] = vetor[i];
                    for(int j = 0; j < num; j++) {
                        copiaA[i][j] = matriz[i][j];
                    }
                }
                
                decomposicaoLU(copiaA, L, U, copiaB, solucao, num);
                mostrarVetor(solucao, num);
                
                liberarMemoria(copiaA, num);
                delete[] copiaB;
                break;
            }
                
            case 4: {
                double** copiaA = alocarMatriz(num);
                double* copiaB = new double[num];
                
                for(int i = 0; i < num; i++) {
                    copiaB[i] = vetor[i];
                    for(int j = 0; j < num; j++) {
                        copiaA[i][j] = matriz[i][j];
                    }
                }
                
                decomposicaoLUPP(copiaA, L, U, copiaB, solucao, num);
                mostrarVetor(solucao, num);
                
                liberarMemoria(copiaA, num);
                delete[] copiaB;
                break;
            }
                
            case 0:
                cout << "Saindo do programa..." << endl;
                break;
                
            default:
                cout << "Opção inválida!" << endl;
        }
        
    } while(opcao != 0);
    
    liberarMemoria(matriz, num);
    liberarMemoria(L, num);
    liberarMemoria(U, num);
    delete[] vetor;
    delete[] solucao;

    return 0;
}