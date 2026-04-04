# Proyecto Big Data Burnout

Repositorio para el análisis de burnout usando la notebook `TP_Grupo 4_BigData_Burnout.ipynb`.

## Requisitos

- Python 3.10+ recomendado
- `pip` disponible
- `requirements.txt` presente en el repositorio

## Crear y activar un entorno virtual

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## Instalar dependencias

Con el entorno virtual activo:

```bash
pip install -r requirements.txt
```

# Exploración de los datos y entrenamiento del modelo

1. Abre `TP_Grupo 4_BigData_Burnout.ipynb` en tu editor (por ejemplo, VS Code).
2. Selecciona el intérprete/entorno Python del virtual env `venv`.

## Seleccionar el kernel en la notebook

- En VS Code, abre la notebook `TP_Grupo 4_BigData_Burnout.ipynb`.
- En la esquina superior derecha de la notebook, haz clic en el selector de kernel/interprete.
- Elige el kernel asociado a `./venv/bin/python` (o `./venv/Scripts/python.exe` en Windows).
- Si no ves el kernel, selecciona `Python: Seleccionar intérprete` desde la paleta de comandos y elige `venv`, luego vuelve a la notebook.

## Notas

- Asegúrate de activar el entorno virtual antes de ejecutar comandos de Python.

# Gestión de Experimentos y Modelos (MLflow)

Para visualizar la búsqueda de hiperparámetros con Optuna y gestionar las versiones del modelo en el Model Registry:

## Levantar el servidor de MLflow:

Desde la terminal en la raíz del proyecto, ejecuta:

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5001
```

Nota: Se utiliza el puerto 5001 para evitar conflictos con servicios del sistema en macOS (AirPlay).

## Acceder a la UI:

Ingresa a http://localhost:5001 para comparar trials, ver gráficos de importancia de hiperparámetros y revisar el estado del modelo registrado.

# Despliegue de la API (Backend)

La API utiliza FastAPI y carga el PipelineModel de Spark directamente desde el Registry para automatizar el preprocesamiento y la predicción.

Asegúrate de que el servidor de MLflow esté corriendo (Paso 2).

## Ejecutar la API:

En una nueva terminal con el entorno activo (y el servidor de MLFlow corriendo):

```bash
cd src
python api_burnout.py
```

La API estará lista cuando veas el mensaje: Uvicorn running on http://0.0.0.0:8000.

# Interfaz de Usuario (Frontend)

Interfaz web construida con Streamlit que permite a los usuarios finales obtener predicciones cargando archivos CSV.

## Ejecutar la Interfaz:

En una tercera terminal con el entorno activo (y el servidor de MLFlow y la API corriendo):

```bash
cd src
streamlit run interface_burnout.py
```

## Uso:

Se abrirá automáticamente http://localhost:8501.

Sube un archivo CSV con los datos de entrada (asegúrate de que los nombres de columnas coincidan con el dataset original). Se puede utilizar el csv dummy (test_api_dataset.csv) incluído en este proyecto para evaluar el funcionamiento.

Haz clic en "Ejecutar Predicción".