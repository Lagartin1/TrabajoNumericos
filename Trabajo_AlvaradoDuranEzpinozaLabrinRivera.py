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

def graficar_resultados(ax, resultados, color_map, title):
    X = [] #inicializamos los array vacios para los valores de los ejes (x,t,w)
    Y = []
    Z = []
    for t, xs, ws in resultados: #llenamos los array con los valores
        for x, w in zip(xs, ws):
            X.append(x)
            Y.append(t)
            Z.append(w)
    
    ax.plot_trisurf(X, Y, Z, cmap=color_map) #se crea la superficie 3d
    ax.set_title(title) #ajuste de titulo y nombre ejes
    ax.set_xlabel('Posición (x)')
    ax.set_ylabel('Tiempo (t)')
    ax.set_zlabel('Temperatura (W)')

def diferencias_regresivas_calor(L, T, alpha, m, N):
    resultados = []
    
    h = L / m
    k = T / N
    lambda_ = alpha**2 * k / h**2
    w = np.zeros(m-1)
    
    for i in range(m-1):
        w[i] = FX((i + 1) * h)  # Condiciones iniciales
    
    l = np.zeros(m - 1)
    u = np.zeros(m - 2)
    
    l[0] = 1 + 2 * lambda_
    u[0] = -lambda_ / l[0]
    
    for i in range(1, m - 2):
        l[i] = 1 + 2 * lambda_ + lambda_ * u[i - 1]
        u[i] = -lambda_ / l[i]
    
    l[m - 2] = 1 + 2 * lambda_ + lambda_ * u[m - 3]
    
    z = np.zeros(m - 1)
    for j in range(1, N + 1):
        t = j * k
        
        z[0] = w[0] / l[0]
        
        for i in range(1, m - 1):
            z[i] = (w[i] + lambda_ * z[i - 1]) / l[i]
        
        w[m - 2] = z[m - 2]
        
        for i in range(m - 3, -1, -1):
            w[i] = z[i] - u[i] * w[i + 1]
        
        xs = [i * h for i in range(1, m)]
        resultados.append((t, xs, w.copy()))
    
    return resultados 

def solucionReal(N):
    UREAL = lambda x,t:2 * np.exp(- (np.pi**2 / 4) * t) * np.sin(2 * np.pi * x) #funcion de la solucion real
    resultados = []
    x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9] #defino los mismos valores que toma en la solucion aproximada
    m= len(x)
    t = np.linspace(0.01, 0.1, num=N)
    for j in range(N):
        xs = []
        ws = []
        for i in range(m):
            xs.append(x[i])
            ws.append(UREAL(x[i],t[j]))
        resultados.append((t[j],xs,ws))
        
    return resultados

def main():
    #valores para las funciones
    L = 1
    T = 0.1
    alpha = 1/4
    m = 10
    N = 10
    resultado = diferencias_regresivas_calor(L, T, alpha, m, N)
    #imprimimos los resultados aproximados
    print("Aproximacion w_ij a u_ij",end="\n")
    for t, xs, ws in resultado:
        print(f"Tiempo t = {t:.2f}")
        for x, w in zip(xs, ws):
            print(f"x = {x:.2f}, w = {w:.4f}")
        print()
    #imprimimos los resultados reales
    resultadoReal = solucionReal(N)
    print("Resultado real",end="\n")
    for t, xs, ws in resultadoReal: 
        print(f"Tiempo t = {t:.2f}")
        for x, w in zip(xs, ws):
            print(f"x = {x:.2f}, w = {w:.4f}")
        print()
    
    #crea la ventana para poner los dos graficos
    fig = plt.figure(figsize=(14, 7))
    
    #crea el primer grafico, de las soluciones aproximadas, le asigna color
    ax1 = fig.add_subplot(121, projection='3d')
    graficar_resultados(ax1, resultado, color_map='viridis', title='Aproximacion w_ij a u_ij')
    
    #crea el de las soluciones reales
    ax2 = fig.add_subplot(122, projection='3d')
    graficar_resultados(ax2, resultadoReal, color_map='plasma', title='Resultado real de u_ij')
    
    
    plt.tight_layout() #ajusta para que no haya solapamiento de los graficos
    plt.show() #muestra el grafico

main() #el programa termina al cerrar la ventana de los graficos
