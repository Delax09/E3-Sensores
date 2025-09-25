from random import randint, random, choice

decision = input("Aleatorio? Y/N: ")
if decision.upper() == "Y":
    from Dataset_Aleatorio import calles
else:
    from Dataset_Predefinido import calles

presupuesto_total = 100000 #Presupesto total disponible va cambiando
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
    # Itera sobre cada calle/intersección del dataset
    for calle in calles:
        sensores = {
            "Id": calle["Id"], 
            # Asigna aleatoriamente si hay sensor de tráfico
            "Sensor_trafico": choice([True, False]),
            # Asigna aleatoriamente si hay sensor de aire
            "Sensor_aire": choice([True, False]),
            # Asigna aleatoriamente si hay sensor de estacionamiento
            "Sensor_estacionamiento": choice([True, False])
        }
        individuo.append(sensores)  # Agrega la configuración de sensores para la intersección
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
        # Sensor de tráfico en zona de alta congestión suma más puntos
        if inter["Sensor_trafico"]:
            if calle["Tipo_congestion"] == 3:
                puntuacion += 3
            elif calle["Tipo_congestion"] == 2:
                puntuacion += 2
            elif calle["Tipo_congestion"] == 1:
                puntuacion += 1
        # Sensor de aire en zona de alta contaminación suma más puntos
        if inter["Sensor_aire"]:
            if calle["Tipo_contaminacion"] == 3:
                puntuacion += 3
            elif calle["Tipo_contaminacion"] == 2:
                puntuacion += 2
            elif calle["Tipo_contaminacion"] == 1:
                puntuacion += 1
        # Sensor de estacionamiento en zona de alta demanda suma más puntos
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
        # Itera sobre cada tipo de sensor para aplicar posible mutación
        for sensor in ["Sensor_trafico", "Sensor_aire", "Sensor_estacionamiento"]:
            # Mutación usando el parámetro prob_mutacion
            if random() < prob_mutacion:
                sensores[sensor] = not sensores[sensor]
        nuevo.append(sensores)  # Agrega la intersección mutada a la nueva lista
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

def reparar(individuo):
    """
    Repara un individuo que excede el presupuesto apagando sensores
    hasta cumplir el presupuesto. Se apagan primero los sensores con
    menor beneficio relativo (beneficio / costo).
    """
    nuevo = [inter.copy() for inter in individuo]
    # Mientras el costo supere el presupuesto, apagar el sensor menos eficiente
    while calcular_costo(nuevo) > presupuesto_total:
        candidatos = []
        for idx, inter in enumerate(nuevo):
            calle = calles[idx]
            # Para cada sensor encendido, calcular su "beneficio" y ratio beneficio/costo
            if inter.get("Sensor_trafico"):
                beneficio = calle.get("Tipo_congestion", 0) or 0
                candidatos.append((beneficio / c_sensor_trafico if c_sensor_trafico else 0, idx, "Sensor_trafico"))
            if inter.get("Sensor_aire"):
                beneficio = calle.get("Tipo_contaminacion", 0) or 0
                candidatos.append((beneficio / c_sensor_aire if c_sensor_aire else 0, idx, "Sensor_aire"))
            if inter.get("Sensor_estacionamiento"):
                beneficio = calle.get("Demanda_estacionamiento", 0) or 0
                candidatos.append((beneficio / c_sensor_estacionamiento if c_sensor_estacionamiento else 0, idx, "Sensor_estacionamiento"))
        if not candidatos:
            # No hay sensores encendidos para apagar -> no se puede reparar
            break
        # Ordenar por ratio ascendente (menor beneficio por coste primero)
        candidatos.sort(key=lambda x: x[0])
        _, idx_sel, sensor_sel = candidatos[0]
        nuevo[idx_sel][sensor_sel] = False
    return nuevo

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

    # Seleccionar la mejor solución que cumpla el presupuesto
    viables = [ind for ind in poblacion if calcular_costo(ind) <= presupuesto_total]
    if viables:
        mejor = max(viables, key=fitness)
    else:
        # Si no hay soluciones viables, reparar la mejor candidata por fitness
        candidato = max(poblacion, key=fitness)
        mejor = reparar(candidato)
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