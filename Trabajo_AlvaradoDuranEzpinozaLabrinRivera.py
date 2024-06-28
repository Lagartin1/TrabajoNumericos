## BAIN087
# Francisco Labrin
# Matias Rivera
# Ivan Duran
# Luciano Espinoza
# Martin Alvarado

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# u aprox
FX = lambda x: 2 * np.sin(2 * np.pi * x)  

def graficar_resultados(resultados,color_map):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')
    X = []
    Y = []
    Z = []
    for t, xs, ws in resultados:
        for x, w in zip(xs, ws):
            X.append(x)
            Y.append(t)
            Z.append(w)
    
    ax.plot_trisurf(X, Y, Z, cmap=color_map)

    ax.set_xlabel('Posición (x)')
    ax.set_ylabel('Tiempo (t)')
    ax.set_zlabel('Temperatura (W)')

    return fig,ax

## Actividad (1)
def diferencias_regresivas_calor(L, T, alpha, m, N):
    resultados = []
    
    ## Paso 1: Calcular h, k y lambda
    h = L / m
    k = T / N
    lambda_ = alpha**2 * k / h**2
    w = np.zeros(m-1)
    
    ## Paso 2
    for i in range(m):
        w[i] = FX((i + 1) * h)  # Condiciones iniciales
    
    l = np.zeros(m - 1)
    u = np.zeros(m - 2)
    
    ## Paso 3
    l[0] = 1 + 2 * lambda_
    u[0] = -lambda_ / l[0]
    
    ## Paso 4
    for i in range(1, m - 2):
        l[i] = 1 + 2 * lambda_ + lambda_ * u[i - 1]
        u[i] = -lambda_ / l[i]
    
    ## Paso 5
    l[m - 2] = 1 + 2 * lambda_ + lambda_ * u[m - 3]
    
    ## Paso 6
    z = np.zeros(m - 1)
    for j in range(1, N + 1):
        t = j * k
        
        ## Paso 7: Calcular z1
        z[0] = w[0] / l[0]
        
        # Paso 8
        for i in range(1, m - 1):
            z[i] = (w[i] + lambda_ * z[i - 1]) / l[i]
        
        ## Paso 9: Calcular wm-1
        w[m - 2] = z[m - 2]
        
        ## Paso 10
        for i in range(m - 3, -1, -1):
            w[i] = z[i] - u[i] * w[i + 1]
        
        # Paso 11 salida
        xs = [i * h for i in range( (m) )]
        ## en el tiempo t=tj
        # tiene temperaturas aproximadas aproximadas Wi = Wij => posición xi, tiempo xj
        resultados.append((t, xs, w.copy()))
    
    ## salida aproximaciones de Wij en cada tiempo tj en cada posición xi
    ## de la forma tiempo, posiciónes, aproximaciones
    return resultados 


def solucionReal(m, N):
    UREAL = lambda x,t:2 * np.exp(- (np.pi**2 / 4) * t) * np.sin(2 * np.pi * x)
    resultados = []
    x = np.linspace(0, 1, num=10, endpoint=False)
    t = np.linspace(0.01, 0.1, num=10, endpoint=False)
    for j in range(N):
        xs = []
        ws = []
        for i in range(m):
            xs.append(x[i])
            ws.append(UREAL(x[i],t[j]))
        resultados.append((t[j],xs,ws))
        
    return resultados

def main():
    ## Actividad (2)
    L = 1
    T = 0.1
    alpha = 1/4
    m = 10
    N = 10
    resultado = diferencias_regresivas_calor(L, T, alpha, m, N)
    
    # impresion de todos los x,w para cada tj para la aproximacion
    print("Aproximacion w_ij a u_ij",end="\n")
    for t, xs, ws in resultado:
        print(f"Tiempo t = {t:.2f}")
        for x, w in zip(xs, ws):
            print(f"x = {x:.2f}, w = {w:.4f}")
        print()

    ## Actividad (3) 
    fig1, ax1 = graficar_resultados(resultado, color_map='viridis') # grafico 1: aproximacion
    ax1.set_title('Aproximacion w_ij a u_ij  ')
    
    # impresion de todos los x,w para cada tj para la solucion real
    resultadoReal = solucionReal(m, N)
    print("Resultado real",end="\n")
    for t, xs, ws in resultadoReal:
        print(f"Tiempo t = {t:.2f}")
        for x, w in zip(xs, ws):
            print(f"x = {x:.2f}, w = {w:.4f}")
        print()
        
    fig2, ax2 = graficar_resultados(resultadoReal, color_map='plasma') # grafico 2: u real
    ax2.set_title('Resultado real de u_ij ')
    
    # Ajusta la posición de graficos para que no se superpongan
    fig2.tight_layout()
    
    plt.show()
    
    
    
    
main()
