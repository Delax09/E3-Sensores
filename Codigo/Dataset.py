"""
Este archivo es de prueba para el modelo de  datos que vamos a utilizar
"""

interseccion11 = {
    "ID": "11",
    "Corrdenadas": (1,1),
    "Tipo_zona": 1,
    "Tipo_congestion": 3,
    "Tipo_contaminacion": 2,
    "Demanda_estacionamiento": 3,
    "Sensor_trafico": True,
    "Sensor_aire": True,
    "Sensor_estacionamiento": False,
    "Datos": {
        "Flujo_vehicular": 120,
        "PM2.5": 35,
        "NO2": 22,
        "Ocupacion_estacionamiento": None
        }
}

'''
Eliminar la variable "Costo_sensor" y "Cobertura"
'''

#insterseccion11["Costo_sensor"] = 1500 #Actualizando un valor

mapa_ciudad = [[interseccion00, interseccion01, interseccion02], 
               [interseccion10, interseccion11, interseccion12],
               [interseccion20, interseccion21, interseccion22]]

#Asi hay que recorrer el diccionario
for clave, valor in interseccion11.items():
    #Diccionario anidado
    if clave == "Datos":
        print(clave)
        for clave2, valor2 in valor.items():
            print("  ", clave2, valor2)
    else:
        print(clave, valor)

#Esto es para que sea m�s intuitivo para el algoritmo
#para nosotros tener una idea de los datos y el modelado
zonas = {
    "Comercial" : 1,
    "Residencial": 2,
    "Empresarial": 3
    }

congestion = {
    "Baja": 1,
    "Media": 2,
    "Alta": 3
    }

contaminacion = {
    "Baja": 1,
    "Media": 2,
    "Alta": 3
    }

demanda_estacionamiento = {
    "Baja": 1,
    "Media": 2,
    "Alta": 3
    }