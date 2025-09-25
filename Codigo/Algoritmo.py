from random import randint, random, choice

decision = input("Aleatorio? Y/N: ")
if decision.upper() == "Y":
    from Dataset_Aleatorio import calles
else:
    from Dataset_Predefinido import calles

presupuesto_total = 30000 #Presupesto total disponible va cambiando
c_sensor_estacionamiento = 4000
c_sensor_trafico = 10000
c_sensor_aire = 9000

"""# Mostrar toda la matriz del dataset
print("Matriz de intersecciones del dataset:\n")
for idx, calle in enumerate(calles):
    print(f"Interseccin {idx}:")
    for clave, valor in calle.items():
        print(f"  {clave}: {valor}")
    print("-" * 40)
print("\n")"""

def crear_individuo():
    individuo = []
    # Itera sobre cada calle/intersecci�n del dataset
    for calle in calles:
        sensores = {
            "Id": calle["Id"], 
            # Asigna aleatoriamente si hay sensor de tr�fico
            "Sensor_trafico": choice([True, False]),
            # Asigna aleatoriamente si hay sensor de aire
            "Sensor_aire": choice([True, False]),
            # Asigna aleatoriamente si hay sensor de estacionamiento
            "Sensor_estacionamiento": choice([True, False])
        }
        individuo.append(sensores)  # Agrega la configuraci�n de sensores para la intersecci�n
    return individuo  # Devuelve el individuo generado (lista de intersecciones con sensores)

def calcular_costo(individuo):
    costo = 0
    for inter in individuo:
        if inter["Sensor_trafico"]:
            costo += c_sensor_trafico
        if inter["Sensor_aire"]:
            costo += c_sensor_aire
        if inter["Sensor_estacionamiento"]:
            costo += c_sensor_estacionamiento
    return costo

def fitness(individuo):
    costo = calcular_costo(individuo)
    if costo > presupuesto_total:
        return 0  # Penaliza si excede el presupuesto

    puntuacion = 0
    for idx, inter in enumerate(individuo):
        calle = calles[idx]
        # Sensor de tr�fico en zona de alta congesti�n suma m�s puntos
        if inter["Sensor_trafico"]:
            if calle["Tipo_congestion"] == 3:
                puntuacion += 3
            elif calle["Tipo_congestion"] == 2:
                puntuacion += 2
            elif calle["Tipo_congestion"] == 1:
                puntuacion += 1
        # Sensor de aire en zona de alta contaminaci�n suma m�s puntos
        if inter["Sensor_aire"]:
            if calle["Tipo_contaminacion"] == 3:
                puntuacion += 3
            elif calle["Tipo_contaminacion"] == 2:
                puntuacion += 2
            elif calle["Tipo_contaminacion"] == 1:
                puntuacion += 1
        # Sensor de estacionamiento en zona de alta demanda suma m�s puntos
        if inter["Sensor_estacionamiento"]:
            if calle["Demanda_estacionamiento"] == 3:
                puntuacion += 3
            elif calle["Demanda_estacionamiento"] == 2:
                puntuacion += 2
            elif calle["Demanda_estacionamiento"] == 1:
                puntuacion += 1
    return puntuacion

def mutar(individuo, prob_mutacion):
    # Crea una nueva lista para el individuo mutado
    nuevo = []
    for inter in individuo:
        sensores = inter.copy() 
        # Itera sobre cada tipo de sensor para aplicar posible mutaci�n
        for sensor in ["Sensor_trafico", "Sensor_aire", "Sensor_estacionamiento"]:
            # Mutaci�n usando el par�metro prob_mutacion
            if random() < prob_mutacion:
                sensores[sensor] = not sensores[sensor]
        nuevo.append(sensores)  # Agrega la intersecci�n mutada a la nueva lista
    return nuevo  # Devuelve el individuo mutado

def cruzar(padre1, padre2):
    hijo = []
    for i in range(len(padre1)):
        sensores = {}
        for sensor in ["Sensor_trafico", "Sensor_aire", "Sensor_estacionamiento"]:
            sensores[sensor] = padre1[i][sensor] if random() < 0.5 else padre2[i][sensor]
        sensores["Id"] = padre1[i]["Id"]
        hijo.append(sensores)
    return hijo

def algoritmo_genetico(generaciones, poblacion_size, prob_mutacion):
    poblacion = [crear_individuo() for _ in range(poblacion_size)]
    for gen in range(generaciones):
        poblacion = sorted(poblacion, key=fitness, reverse=True)
        nueva_poblacion = poblacion[:5]
        while len(nueva_poblacion) < poblacion_size:
            padre1, padre2 = choice(poblacion[:15]), choice(poblacion[:15])
            hijo = cruzar(padre1, padre2)
            hijo = mutar(hijo, prob_mutacion)  # Se pasa la probabilidad como argumento
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion
    mejor = max(poblacion, key=fitness)
    return mejor

probabilidad = 0.1 #Probabilida de mutacion puede ser variable controlada por nosotros
generaciones = 50
poblacion_size = 30

# Ejecutar el algoritmo
mejor_solucion = algoritmo_genetico(generaciones,poblacion_size,probabilidad)
print("Mejor solucion encontrada:\n")
print(f"{'Id':<5} {'Congestion':<12} {'Contaminacion':<15} {'Demanda Est.':<15} {'Trafico':<8} {'Aire':<6} {'Estacionamiento':<15} {'Costo':<7}")
print("-" * 80)
for idx, inter in enumerate(mejor_solucion):
    calle = calles[idx]
    costo = calcular_costo([inter])
    print(f"{inter['Id']:<5} {calle['Tipo_congestion']:<12} {calle['Tipo_contaminacion']:<15} {calle['Demanda_estacionamiento']:<15} "
          f"{'Si' if inter['Sensor_trafico'] else 'No':<8} {'Si' if inter['Sensor_aire'] else 'No':<6} {'Si' if inter['Sensor_estacionamiento'] else 'No':<15} {costo:<7}")
print("-" * 80)
print(f"Presupuesto: {presupuesto_total}")
print("Costo total:", calcular_costo(mejor_solucion))