from Dataset import calles

def GeneraPoblacion(poblacion):
    ciudad = []
    idx = 0
    for i in range(poblacion):
        calle2 = []
        for j in range(poblacion):
            calle2.append(calles[idx % len(calles)])
            idx += 1
        ciudad.append(calle2)
    return ciudad

mapa = GeneraPoblacion(3)

for i, fila in enumerate(mapa):
    print(f"Fila {i}:")
    for j, calle in enumerate(fila):
        print(f"  Columna {j}: {calle}")
    print()