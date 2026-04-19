# Plan Maestro: Crypto ML Predictor 📈

Este documento define la estrategia técnica para validar la hipótesis de los **Volume Shocks** y construir un sistema de predicción robusto, partiendo de la exploración hasta la producción.

---

## 1. Visión del Proyecto
Construir un motor de inferencia que consuma datos de la arquitectura Medallion (GCP BigQuery) y prediga movimientos de precio basados en anomalías de volumen.

### Estrategia de Desarrollo
*   **Fase de Descubrimiento (Notebooks):** Uso de Jupyter/Colab para visualización de datos, limpieza y validación estadística rápida.
*   **Fase de Producción (Scripts .py):** Refactorización del código validado en módulos limpios dentro de `src/`.

---

## 2. Metodología de Ciencia de Datos (Senior DS)
*   **Hipótesis:** Un pico inusual de volumen (Volume Shock) precede a una reversión o aceleración del precio en las siguientes 24-48 horas.
*   **Validación Estadística:** Uso de correlación de Spearman para medir la fuerza de la relación Volumen -> Precio.
*   **Ingeniería de Características:** 
    *   **Lags:** Precios y volúmenes de los últimos 1, 3 y 7 días.
    *   **Momentum:** RSI y medias móviles simples.
    *   **Z-Score de Volumen:** Cuántas desviaciones estándar se aleja el volumen actual del promedio móvil de 30 días.

---

## 3. Estándares de Ingeniería (Senior ML Engineer / MLOps)
*   **Validación Temporal:** Uso de `TimeSeriesSplit`. Siempre entrenaremos con el pasado para predecir el "futuro" relativo, evitando trampas en el modelo.
*   **Seguimiento de Experimentos:** Uso de **MLflow** para registrar cada prueba (qué modelo usamos, qué tan preciso fue y qué datos consumió).
*   **Calidad de Datos:** Verificación básica de nulos y outliers antes del entrenamiento.

---

## 4. Arquitectura de Datos (Senior Architect)
1.  **Ingesta:** BigQuery (`analytics_data_gold`) -> Pandas DataFrame.
2.  **Procesamiento:** Transformación de series temporales.
3.  **Modelado:** Entrenamiento de modelos de gradiente (XGBoost/LightGBM).
4.  **Inferencia:** Generación de señales de predicción.
