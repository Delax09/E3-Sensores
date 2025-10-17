# app.py
import streamlit as st
import pandas as pd
import Algoritmo as core 

# --- Configuracion de la Pagina ---
st.set_page_config(
    page_title="Optimizador de Sensores Urbanos",
    layout="wide"
)

# --- Titulo y Descripcion ---
st.title("Optimizador de Sensores con Algoritmo Genetico")
st.markdown("Esta aplicacion encuentra la distribucion optima de sensores en una ciudad, maximizando la cobertura sin exceder el presupuesto.")

# --- Barra Lateral de Parametros (Inputs del Usuario) ---
st.sidebar.header("Configuracion del Algoritmo")

dataset_option = st.sidebar.selectbox("Selecciona el Dataset", ("Predefinido", "Aleatorio"))

if dataset_option == "Predefinido":
    from Dataset_Predefinido import calles
    st.sidebar.info("Dataset con valores fijos.")
else:
    from Dataset_Aleatorio import calles
    st.sidebar.warning("Dataset con valores aleatorios. Los resultados variaran.")

presupuesto = st.sidebar.number_input("Presupuesto Total ($)", min_value=10000, value=100000, step=1000)
generaciones = st.sidebar.slider("Generaciones", 10, 500, 50, step=10)
poblacion_size = st.sidebar.slider("Tamanio de Poblacion", 10, 200, 30, step=5)
prob_mutacion = st.sidebar.slider("Prob. de Mutacion", 0.01, 0.5, 0.1, step=0.01)

# --- Boton de Ejecucion y Logica Principal ---
if st.sidebar.button("Ejecutar Optimizacion"):
    with st.spinner("El algoritmo esta trabajando..."):
        # La llamada a las funciones ahora usa "core" que es el alias de tu archivo "Algoritmo"
        mejor_solucion, historial = core.algoritmo_genetico(
            generaciones=generaciones,
            poblacion_size=poblacion_size,
            prob_mutacion=prob_mutacion,
            presupuesto_total=presupuesto,
            calles=calles,
            record_history=True
        )
    
    st.success("Optimizacion completada")

    # --- Visualizacion de Resultados ---
    costo_total = core.calcular_costo(mejor_solucion)
    puntuacion_fitness = core.fitness(mejor_solucion, calles, presupuesto)

    st.subheader("Resultados Generales")
    col1, col2, col3 = st.columns(3)
    col1.metric("Costo Total", f"${costo_total:,.0f}", f"${presupuesto - costo_total:,.0f} restante")
    col2.metric("Puntuacion (Fitness)", f"{puntuacion_fitness} pts")
    col3.metric("Presupuesto Limite", f"${presupuesto:,.0f}")

    # --- Tabla de la Mejor Solucion ---
    st.subheader("Distribucion Optima de Sensores Sugerida")
    
    df_solucion = pd.DataFrame(mejor_solucion)
    df_calles = pd.DataFrame(calles)
    df_resultado = pd.merge(df_solucion, df_calles, on="Id")
    
    df_resultado = df_resultado.rename(columns={
        "Sensor_trafico": "Sensor Trafico",
        "Sensor_aire": "Sensor Aire",
        "Sensor_estacionamiento": "Sensor Estacionamiento",
        "Tipo_congestion": "Prioridad Congestion",
        "Tipo_contaminacion": "Prioridad Contaminacion",
        "Demanda_estacionamiento": "Prioridad Estacionamiento"
    })
    
    for col in ["Sensor Trafico", "Sensor Aire", "Sensor Estacionamiento"]:
        df_resultado[col] = df_resultado[col].apply(lambda x: "Si" if x else "No")
        
    st.dataframe(df_resultado[[
        "Id", "Sensor Trafico", "Sensor Aire", "Sensor Estacionamiento",
        "Prioridad Congestion", "Prioridad Contaminacion", "Prioridad Estacionamiento"
    ]], use_container_width=True)

    # --- Grafico de Convergencia ---
    st.subheader("Convergencia del Algoritmo (Fitness por Generacion)")
    if historial:
        df_historial = pd.DataFrame(historial)
        st.line_chart(df_historial, x="generacion", y="best_fitness")
    else:
        st.warning("No se registro el historial para graficar.")

else:
    st.info("Ajusta los parametros en la barra lateral y haz clic en 'Ejecutar Optimizacion'.")