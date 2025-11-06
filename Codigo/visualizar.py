#en consola:
#Pip install Streamlit 
#streamlit run Visualizar.py
import streamlit as st
import pandas as pd
import Algoritmo
st.set_page_config(page_title="Optimizador de Sensores", layout="wide")
st.title("Optimizador de Sensores con Algoritmo Genético")

# --- Panel lateral: parámetros ---
dataset = st.sidebar.selectbox("Dataset", ("Predefinido", "Aleatorio"))
presupuesto = st.sidebar.number_input("Presupuesto total", value=100000, step=1000)
generaciones = st.sidebar.slider("Generaciones", 10, 500, 50, step=10)
poblacion_size = st.sidebar.slider("Tamanio poblacion", 10, 200, 30, step=5)
prob_mutacion = st.sidebar.slider("Prob mutacion", 0.0, 0.5, 0.1, step=0.01)

if st.sidebar.button("Ejecutar algoritmo"):
    Algoritmo.set_dataset(dataset == "Aleatorio")
    Algoritmo.set_presupuesto(int(presupuesto))
    with st.spinner("Ejecutando..."):
        mejor, historial = Algoritmo.algoritmo_genetico(generaciones, poblacion_size, prob_mutacion, record_history=True)
    st.success("Ejecucion completada")

    # Mostrar tabla resultado
    df_sol = pd.DataFrame(mejor)
    try:
        # añadir columnas del dataset para contexto
        from Codigo.Dataset_Predefinido import calles as _cp
        mapa = {c["Id"]: c for c in _cp}
        df_extra = df_sol["Id"].map(lambda i: mapa.get(i, {}))
        df_detalle = pd.concat([df_sol, pd.json_normalize(df_extra)], axis=1)
    except Exception:
        df_detalle = df_sol

    # Calcular costo por intersección usando los costes definidos en Algoritmo
    def _costo_interseccion(row):
        total = 0
        if row.get("Sensor_trafico"):
            total += getattr(Algoritmo, "c_sensor_trafico", 10000)
        if row.get("Sensor_aire"):
            total += getattr(Algoritmo, "c_sensor_aire", 9000)
        if row.get("Demanda_estacionamiento"):
            total += getattr(Algoritmo, "c_sensor_estacionamiento", 4000)
        return total

    df_detalle["Costo Interseccion"] = df_detalle.apply(_costo_interseccion, axis=1)

    df_detalle = df_detalle.rename(columns={
        "Sensor_trafico": "Sensor Trafico",
        "Sensor_aire": "Sensor Aire",
        "Demanda_estacionamiento": "Demanda Estacionamiento"
    })
    for col in ["Sensor Trafico", "Sensor Aire", "Demanda Estacionamiento"]:
        if col in df_detalle.columns:
            df_detalle[col] = df_detalle[col].apply(lambda x: "Si" if x else "No")

    st.subheader("Mejor solucion (por interseccion)")
    # Mostrar también el costo por intersección
    display_cols = [
        "Id", "Sensor Trafico", "Sensor Aire", "Demanda Estacionamiento",
        "Prioridad Congestion", "Prioridad Contaminacion", "Prioridad Estacionamiento",
        "Costo Interseccion"
    ]
    # Filtrar columnas existentes para evitar KeyError
    display_cols = [c for c in display_cols if c in df_detalle.columns]
    st.dataframe(df_detalle[display_cols], use_container_width=True)

    st.metric("Costo total", f"${Algoritmo.calcular_costo(mejor):,.0f}")
    st.metric("Puntuacion (fitness)", f"{Algoritmo.fitness(mejor):.0f}")

    st.subheader("Convergencia")
    df_hist = pd.DataFrame(historial)
    st.line_chart(df_hist.set_index("generacion"))
else:
    st.info("Ajusta parametros y pulsa 'Ejecutar algoritmo' en la barra lateral.")