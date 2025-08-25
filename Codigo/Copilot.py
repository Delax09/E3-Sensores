import random


"""
Este codidgo es de base para generado por COPILOT para tener una 
idea de como modelar y entender el codigo y el modelado
"""


# -------------------------------
# 1. Parámetros del problema
# -------------------------------

GRID_SIZE = 6  # Ciudad modelada como cuadrícula 6x6
BUDGET = 20000  # Presupuesto total disponible

# Costos y cobertura por tipo de sensor
SENSORS = {
    "trafico": {"cost": 1000, "coverage": 0.5},
    "aire": {"cost": 1200, "coverage": 0.7},
    "estacionamiento": {"cost": 800, "coverage": 0.4}
}

# -------------------------------
# 2. Generación de intersecciones
# -------------------------------

def generate_grid():
    """Genera todas las intersecciones posibles en la cuadrícula."""
    return [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]

INTERSECTIONS = generate_grid()

# -------------------------------
# 3. Generación de solución candidata
# -------------------------------

def generate_candidate():
    """
    Crea una configuración aleatoria de sensores en intersecciones.
    Cada intersección puede tener 0 a 3 sensores.
    """
    candidate = {}
    total_cost = 0

    for i in INTERSECTIONS:
        sensors_installed = []
        for sensor_type in SENSORS:
            # Probabilidad de instalar cada sensor (ajustable)
            if random.random() < 0.2:
                cost = SENSORS[sensor_type]["cost"]
                if total_cost + cost <= BUDGET:
                    sensors_installed.append(sensor_type)
                    total_cost += cost
        candidate[i] = sensors_installed

    return candidate

# -------------------------------
# 4. Evaluación de cobertura
# -------------------------------

def evaluate(candidate):
    """
    Calcula la cobertura total de la ciudad según los sensores instalados.
    Penaliza si se excede el presupuesto.
    """
    total_coverage = 0
    total_cost = 0

    for sensors in candidate.values():
        for s in sensors:
            total_coverage += SENSORS[s]["coverage"]
            total_cost += SENSORS[s]["cost"]

    # Penalización si se excede el presupuesto
    if total_cost > BUDGET:
        total_coverage *= 0.5

    return total_coverage, total_cost

# -------------------------------
# 5. Simulación principal
# -------------------------------

def simulate(n_iterations=1000):
    """Simula múltiples configuraciones y selecciona la mejor."""
    best_candidate = None
    best_coverage = 0
    best_cost = 0

    for _ in range(n_iterations):
        candidate = generate_candidate()
        coverage, cost = evaluate(candidate)

        if coverage > best_coverage and cost <= BUDGET:
            best_candidate = candidate
            best_coverage = coverage
            best_cost = cost

    return best_candidate, best_coverage, best_cost

# -------------------------------
# 6. Ejecución
# -------------------------------

solution, coverage, cost = simulate()

print(f"✅ Cobertura total: {coverage:.2f} km²")
print(f"💰 Costo total: ${cost}")
print("📍 Intersecciones con sensores instalados:")

for loc, sensors in solution.items():
    if sensors:
        print(f"  - {loc}: {', '.join(sensors)}")