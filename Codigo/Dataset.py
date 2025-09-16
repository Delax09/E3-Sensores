from random import randint

interseccion00 = {
    "Tipo_congestion": randint(1,3),
    "Tipo_contaminacion": randint(1,3),
    "Demanda_estacionamiento": randint(1,3)
}
interserccion01 = {
    "Tipo_congestion": randint(1,3),
    "Tipo_contaminacion": randint(1,3),
    "Demanda_estacionamiento": randint(1,3)
    }

interseccion10 ={
    "Tipo_congestion": randint(1,3),
    "Tipo_contaminacion": randint(1,3),
    "Demanda_estacionamiento": randint(1,3)
    }

interseccion11 = {
    "Tipo_congestion": randint(1,3),
    "Tipo_contaminacion": randint(1,3),
    "Demanda_estacionamiento": randint(1,3)
    }

calles = [interseccion00, interserccion01,
          interseccion10, interseccion11]
"""
Sensor_Trafico, Aire, Estacionamiento = que lo decida el algoritmo
Costos definida por el usuario
"""


