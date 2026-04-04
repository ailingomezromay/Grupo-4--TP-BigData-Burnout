import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Burnout Detector", page_icon="🧠")

st.title("🧠 Predicción de Riesgo de Burnout")
st.markdown("""
Esta interfaz permite cargar datos de empleados en formato CSV y obtener una predicción 
basada en el modelo de **Regresión Logística / Random Forest** optimizado.
""")

# Selector de archivo
uploaded_file = st.file_uploader("Subir archivo CSV con datos de empleados", type=["csv"])

if uploaded_file is not None:
    # Mostrar datos cargados
    df_preview = pd.read_csv(uploaded_file)
    st.subheader("Vista previa de los datos")
    st.dataframe(df_preview.head())

    if st.button("🚀 Ejecutar Predicción"):
        # Resetear el archivo para enviarlo desde el principio
        uploaded_file.seek(0)
        
        with st.spinner('Procesando datos en la API de Spark...'):
            try:
                # Enviar archivo a la API (FastAPI)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                response = requests.post("http://localhost:8000/predict", files=files)
                
                if response.status_code == 200:
                    predictions = response.json()
                    
                    # Convertir respuesta a DataFrame para mostrar
                    res_df = pd.DataFrame(predictions)
                    
                    # Unir con el dataframe original para ver quién es quién
                    final_display = pd.concat([df_preview.reset_index(drop=True), res_df], axis=1)
                    
                    st.success("¡Predicciones generadas con éxito!")
                    st.subheader("Resultados finales")
                    st.dataframe(final_display)
                    
                    # Resumen estadístico
                    count_riesgo = res_df[res_df['burnout_risk_label'] == "En riesgo"].shape[0]
                    st.metric("Empleados en riesgo detectados", count_riesgo)
                    
                else:
                    st.error(f"Error en la API (Status {response.status_code}): {response.text}")
            
            except Exception as e:
                st.error(f"No se pudo conectar con la API. Asegúrate de que api_burnout.py esté corriendo. Error: {e}")

st.info("Nota: El CSV debe contener las columnas originales utilizadas durante el entrenamiento.")