from random import randint, sample, random


def generaIndividuo():


def cruzamiento(indiv1, indiv2, n, valores, pesos, C):


def mutacion():


def seleccion(poblacion, n):


def generaPoblacion():
  

def fitness():
    sumValor = 0
    sumPeso = 0
    for i in range(n):
        if individuo[i] == 1:
            sumValor += valores[i]
            sumPeso += pesos[i]
    if sumPeso > C:
        return 0  
    return sumValor

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

tamPoblacion =          #número de individuos en cada generación
numGeneraciones =       #número de generaciones
tasaMutacion =          #probabilidad de que mute un gen de un individuo
k =                     #número de futuros padres (se escogen los 2 mejores para q lo sean)
conElitismo = 
numElegidos =           #número de elegidos para la siguiente generación (con elitismo)

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




