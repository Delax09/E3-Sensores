"""
Este archivo es de prueba para el modelo de  datos que vamos a utilizar
"""

interseccion11 = {
    "ID": "11",
    "Corrdenadas": (1,1),
    "Tipo_zona": "Comercial",
    "Congestion": "Alta",
    "Contaminacion": "Media",
    "Demanda_estacionamiento": "Alta",
    "Sensor_trafico": True,
    "Sensor_aire": True,
    "Sensor_estacionamiento": False,
    "Datos": {
        "Flujo_vehicular": 120,
        "PM2.5": 35,
        "NO2": 22,
        "Ocupacion_estacionamiento": None
        },
    "Costo_sensor": 1800,
    "Cobertura": 1.5  # en km²
}

for clave, valor in interseccion11.items():
    if clave == "Datos":
        print(clave)
        for clave2, valor2 in valor.items():
            print("  ", clave2, valor2)
    else:
        print(clave, valor)