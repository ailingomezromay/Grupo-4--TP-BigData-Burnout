from fastapi import FastAPI, UploadFile, File
from pyspark.sql import SparkSession
import mlflow.spark
import mlflow
mlflow.set_tracking_uri("http://localhost:5001") # Apunta al servidor que levantaste en el paso 1
import pandas as pd
import io
import uvicorn

app = FastAPI(title="Burnout Prediction API - Grupo 4")

# 1. Inicializar Spark (necesario para que el PipelineModel funcione)
spark = SparkSession.builder \
    .appName("API_Prediction") \
    .getOrCreate()

# 2. Cargar el PIPELINE completo desde MLflow Model Registry
# Asegúrate de usar el nombre exacto que pusimos en el registro
MODEL_URI = "models:/Burnout_Production_Model_Final/latest"
try:
    model = mlflow.spark.load_model(MODEL_URI)
    print("Modelo de producción cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Leer el archivo CSV recibido
    contents = await file.read()
    df_pandas = pd.read_csv(io.BytesIO(contents))
    
    # Convertir Pandas a Spark DataFrame (el modelo de Spark requiere esto)
    # El CSV debe tener las mismas columnas originales (gender, age, etc.)
    df_spark = spark.createDataFrame(df_pandas)
    
    # El PipelineModel aplica automáticamente: StringIndexer -> OHE -> Assembler -> Model
    predictions = model.transform(df_spark)
    
    # Seleccionar columnas de interés y convertir a Pandas para la respuesta
    # 'prediction' es el resultado (0 o 1)
    # 'probability' es el vector de probabilidad [p_0, p_1]
    results_pd = predictions.select("prediction").toPandas()
    
    # Mapear resultado numérico a etiqueta legible
    results_pd['burnout_risk_label'] = results_pd['prediction'].apply(
        lambda x: "En riesgo" if x == 1.0 else "Sin riesgo"
    )
    
    return results_pd[['burnout_risk_label']].to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)