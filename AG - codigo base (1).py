from random import randint, sample, random


def generaIndividuo(n, valores, pesos, C):
    individuo = []
    for i in range(n):
        individuo.append(randint(0,n))
    individuo.append(fitness(individuo,n, valores, pesos, C))
    return individuo

def fitness(individuo, n, valores, pesos, C):
    sumValor = 0
    sumPeso = 0
    for i in range(n):
        if individuo[i] == 1:
            sumValor += valores[i]
            sumPeso += pesos[i]
        if sumPeso > C:
            return 0
        return sumValor

def cruzamiento(indiv1, indiv2, n, valores, pesos, C):
    puntoCruce = randint(1, n-1)
    hijo = indiv1[:puntoCruce] + indiv2[puntoCruce:]
    hijo.append(fitness(hijo, n, valores, pesos, C))
    return hijo

def mutacion(individuo, n, valores, pesos, C):
    for i in range(n):
        if random() < tasaMutacion:
            individuo[i] = 1 - individuo[i]
    individuo[n] = fitness(individuo, n, valores, pesos, C)

def seleccion(poblacion, n):
    posibles = sample(poblacion, k)
    posibles.sort(key=lambda x: x[n], reverse = True)
    pololos = [posibles[0], posibles[1]]
    return pololos

def generaPoblacion(n, valores, pesos, C):
    P = []
    for i in range(tamPoblacion):
        P.append(generaIndividuo())
    return P

def AlgoritmoGenetico():
    
    poblacion = generaPoblacion()
    
    for _ in range(numGeneraciones):
        poblacion.sort(key=lambda x: x[n], reverse=True)
        
        if (conElitismo):
            nuevaPoblacion = poblacion[0:numElegidos]
        else:
            nuevaPoblacion = []
            
        for _ in range(tamPoblacion//2):
            padre1, padre2 = seleccion(poblacion,n)
            hijo1 = cruzamiento(padre1,padre2,n,valores,pesos,C)
            hijo2 = cruzamiento(padre2,padre1,n,valores,pesos,C)
            mutacion(hijo1,n,valores,pesos,C)
            mutacion(hijo2,n,valores,pesos,C)
            nuevaPoblacion.append(hijo1)
            nuevaPoblacion.append(hijo2)
            
        poblacion = sorted(nuevaPoblacion, key=lambda x: x[n], reverse=True)[:tamPoblacion]
        #print(f"\ntamaño: {len(poblacion)}\nPoblación: \n{poblacion}")
    return poblacion[0][:n], poblacion[0][n]


########################
### BLOQUE PRINCIPAL ###
########################

##Parámetros del AG: (Constantes del programa)

tamPoblacion = 100       #número de individuos en cada generación
numGeneraciones = 1000      #número de generaciones
tasaMutacion =  0.01        #probabilidad de que mute un gen de un individuo
k = 10                     #número de futuros padres (se escogen los 2 mejores para q lo sean)
conElitismo = False
numElegidos = 2        #número de elegidos para la siguiente generación (con elitismo)

##Datos del problema: mochila 0-1 (Parámetros de entrada al algoritmo AG)

##CASO 1:
##n = 3
##valores = [60, 100, 120]
##pesos = [10, 20, 30]
##C = 50

##Solución: [0, 1, 1]
##Llevar: Objeto2 Objeto3 
##Beneficio: 220
##Peso total: 50

##CASO 2:
##n = 10
##valores = [60,100,120,70,50,80,40,30,20,10]
##pesos = [10,20,30,15,10,15,5,5,2,1]
##C = 50

##Solución: [1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
##Llevar: Objeto1 Objeto5 Objeto6 Objeto7 Objeto8 Objeto9 Objeto10 
##Beneficio: 290
##Peso total: 48

solucion, beneficio = AlgoritmoGenetico()
print(f"SOLUCION: {solucion}")
print(f"BENEFICIO TOTAL: {beneficio}")




