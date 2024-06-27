import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

FX = lambda x: 2 * np.sin(2 * np.pi * x)  

def graficar_resultados(resultados, color_map):
        # Preparar los datos para la gráfica 3D
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

    return fig, ax

def diferencias_regresivas_calor(L, T, alpha, m, N):
    resultados = []
    ##paso1
    h = L / m
    k = T / N
    lambda_ = alpha**2 * k / h**2
    x = np.linspace(h, L-h, m+1)
    w = np.zeros(m)
    ##paso2
    for i in range(0,m):
        w[i] = FX((i+1)*h) # Condiciones iniciales
    l = np.zeros(m)
    u = np.zeros(m-1)
    ##paso 3
    l[0] = 1 + 2 * lambda_
    u[0] = -lambda_ / l[0]
    ##paso 4
    for i in range(1, m-1):
        l[i] = 1 + 2 * lambda_ + lambda_ * u[i-1]
        u[i] = -lambda_ / l[i]
    
    ##paso 5
    l[m-1] = 1 + 2 * lambda_ + lambda_ * u[m-3]
    ##paso 6
    z = np.zeros(m)
    for j in range(0, N):
        xs = []
        ##paso 7
        t = j * k
        z[0] = w[0] / l[0] #define z1
        ##paso 8
        for i in range(1, m):
            z[i] = (w[i] + lambda_ * z[i-1]) / l[i] #rellena z
        ###paso 9
        w[m-1] = z[m-1] 
        ##paso 10
        for i in range(m-2, -1, -1):
            w[i] = z[i-1] - u[i-1] * w[i+1]
        ##paso 11
        for i in range(0,m):
            x = i * h
            xs.append(x)
        ## en el tiempo t=tj
        # tiene temperaturas aproximadas aproximadas Wi = Wij => posición xi, tiempo xj
        resultados.append((t,xs,w))
    ## salida aproximaciones de Wij en cada tiempo tj en cada posición xi
    ## de la forma tiempo, posiciónes, aproximaciones
    return resultados 
def solucionReal(m, N):
    u_real = 0
    resultados = []
    x = np.linspace(0, 1, num=10, endpoint=False)
    t = np.linspace(0.01, 0.1, num=10, endpoint=False)
    
    for j in range(N):
        xs = []
        ws = []
        for i in range(m):
            u_real = 2 * np.exp(- (np.pi**2 / 4) * t[j]) * np.sin(2 * np.pi * x[i])
            xs.append(x[i])
            ws.append(u_real)
            
        resultados.append((t[j],xs,ws))
    return resultados

def main():
    L = 1
    T = 0.1
    alpha = 1/4
    m = 10
    N = 10
    resultado = diferencias_regresivas_calor(L, T, alpha, m, N)
    fig1, ax1 = graficar_resultados(resultado, color_map='viridis')
    
    resultadoReal = solucionReal(m, N)
    fig2, ax2 = graficar_resultados(resultadoReal, color_map='plasma')
    
    # Ajustar la posición de los subplots para que no se superpongan
    fig2.tight_layout()
    
    # Mostrar ambas figuras
    plt.show()

main()