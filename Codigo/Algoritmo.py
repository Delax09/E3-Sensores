from random import random, choice
from copy import deepcopy

# --- Parámetros por defecto (ajustables desde la vista) ---
presupuesto_total = 100000
c_sensor_estacionamiento = 4000
c_sensor_trafico = 10000
c_sensor_aire = 9000

# Dataset activo (se debe setear antes de ejecutar)
calles = None

def set_dataset(aleatorio: bool):
    """Selecciona dataset: True -> Dataset_Aleatorio, False -> Dataset_Predefinido"""
    global calles
    if aleatorio:
        from Dataset_Aleatorio import calles as _calles
    else:
        from Dataset_Predefinido import calles as _calles
    calles = _calles

def set_presupuesto(valor: int):
    """Ajusta el presupuesto total (entero)."""
    global presupuesto_total
    presupuesto_total = int(valor)

def crear_individuo():
    """Genera un individuo aleatorio usando el dataset activo."""
    if calles is None:
        raise RuntimeError("Dataset no seleccionado. Llama a set_dataset(True/False).")
    individuo = []
    for calle in calles:
        sensores = {
            "Id": calle["Id"],
            "Sensor_trafico": choice([True, False]),
            "Sensor_aire": choice([True, False]),
            "Demanda_estacionamiento": choice([True, False])
        }
        individuo.append(sensores)
    return individuo

def calcular_costo(individuo):
    costo = 0
    for inter in individuo:
        if inter.get("Sensor_trafico"):
            costo += c_sensor_trafico
        if inter.get("Sensor_aire"):
            costo += c_sensor_aire
        if inter.get("Demanda_estacionamiento"):
            costo += c_sensor_estacionamiento
    return costo

def fitness(individuo):
    """Calcula puntuación; devuelve 0 si supera presupuesto."""
    if calles is None:
        raise RuntimeError("Dataset no seleccionado. Llama a set_dataset(True/False).")
    costo = calcular_costo(individuo)
    if costo > presupuesto_total:
        return 0
    puntuacion = 0
    for idx, inter in enumerate(individuo):
        calle = calles[idx]
        if inter.get("Sensor_trafico"):
            puntuacion += calle.get("Tipo_congestion", 0)
        if inter.get("Sensor_aire"):
            puntuacion += calle.get("Tipo_contaminacion", 0)
        if inter.get("Demanda_estacionamiento"):
            puntuacion += calle.get("Demanda_estacionamiento", 0)
    return puntuacion

def mutar(individuo, prob_mutacion):
    nuevo = []
    for inter in individuo:
        sensores = inter.copy()
        for sensor in ["Sensor_trafico", "Sensor_aire", "Demanda_estacionamiento"]:
            if random() < prob_mutacion:
                sensores[sensor] = not sensores[sensor]
        nuevo.append(sensores)
    return nuevo

def cruzar(padre1, padre2):
    hijo = []
    for i in range(len(padre1)):
        sensores = {}
        for sensor in ["Sensor_trafico", "Sensor_aire", "Demanda_estacionamiento"]:
            sensores[sensor] = padre1[i][sensor] if random() < 0.5 else padre2[i][sensor]
        sensores["Id"] = padre1[i]["Id"]
        hijo.append(sensores)
    return hijo

def reparar(individuo):
    """Apaga sensores hasta cumplir presupuesto; apaga los que menos puntos aportan primero."""
    if calles is None:
        raise RuntimeError("Dataset no seleccionado. Llama a set_dataset(True/False).")
    nuevo = deepcopy(individuo)
    while calcular_costo(nuevo) > presupuesto_total:
        candidatos = []
        for idx, inter in enumerate(nuevo):
            calle = calles[idx]
            if inter.get("Sensor_trafico"):
                perdida = calle.get("Tipo_congestion", 0)
                candidatos.append((perdida, idx, "Sensor_trafico"))
            if inter.get("Sensor_aire"):
                perdida = calle.get("Tipo_contaminacion", 0)
                candidatos.append((perdida, idx, "Sensor_aire"))
            if inter.get("Demanda_estacionamiento"):
                perdida = calle.get("Demanda_estacionamiento", 0)
                candidatos.append((perdida, idx, "Demanda_estacionamiento"))
        if not candidatos:
            break
        candidatos.sort(key=lambda x: x[0])  # menor pérdida primero
        _, idx_sel, sensor_sel = candidatos[0]
        nuevo[idx_sel][sensor_sel] = False
    return nuevo

def algoritmo_genetico(generaciones, poblacion_size, prob_mutacion, record_history=False):
    """Ejecuta el algoritmo; devuelve mejor individuo y opcionalmente historial."""
    if calles is None:
        raise RuntimeError("Dataset no seleccionado. Llama a set_dataset(True/False).")
    poblacion = [crear_individuo() for _ in range(poblacion_size)]
    history = {"generacion": [], "best_fitness": [], "best_cost": []}
    for gen in range(generaciones):
        poblacion = sorted(poblacion, key=fitness, reverse=True)
        mejor_actual = max(poblacion, key=fitness)
        history["generacion"].append(gen)
        history["best_fitness"].append(fitness(mejor_actual))
        history["best_cost"].append(calcular_costo(mejor_actual))
        elite = poblacion[:max(1, poblacion_size // 6)]
        nueva_poblacion = elite[:]
        while len(nueva_poblacion) < poblacion_size:
            padre1 = choice(poblacion[:max(1, poblacion_size // 2)])
            padre2 = choice(poblacion[:max(1, poblacion_size // 2)])
            hijo = cruzar(padre1, padre2)
            hijo = mutar(hijo, prob_mutacion)
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion

    viables = [ind for ind in poblacion if calcular_costo(ind) <= presupuesto_total]
    if viables:
        mejor = max(viables, key=fitness)
    else:
        candidato = max(poblacion, key=fitness)
        mejor = reparar(candidato)

    if record_history:
        return mejor, history
    return mejor

# Bloque CLI protegido (no se ejecuta al importar)
if __name__ == "__main__":
    print("Este archivo está pensado para usarse desde una vista (Streamlit/Flask).")