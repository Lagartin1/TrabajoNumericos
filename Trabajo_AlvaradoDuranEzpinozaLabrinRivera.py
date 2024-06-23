import numpy as np

FX = lambda x: 2 * np.sin(2 * np.pi * x)  


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


print(diferencias_regresivas_calor(1, 0.1, 1/4, 10, 10))
