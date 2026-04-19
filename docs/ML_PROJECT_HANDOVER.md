# Contexto de Transferencia: Proyecto 3 - Crypto ML Predictor

Este documento sirve como puente técnico para iniciar el desarrollo del **Proyecto 3** de forma independiente, consumiendo datos de la plataforma actual.

---

## 1. Estado Actual (Data Source)
- **Proyecto:** `gcp-data-plataform-hub`
- **Data Warehouse:** BigQuery
- **Datasets Clave:**
    - `raw_data_bronze.historical_raw`: Datos crudos de CoinGecko.
    - `staging_data_silver.crypto_historical_prices`: Datos limpios y deduplicados.
    - `analytics_data_gold.crypto_historical_trends`: Datos con promedios móviles y variación diaria.

---

## 2. Hipótesis Matemática a Corroborar
**Hipótesis:** Existe una correlación negativa entre los picos de volumen inusuales (Volume Shocks) y el retorno del precio en las siguientes 24-48 horas.
- **Métrica de Anomalía:** Z-Score de Volumen > 2.0.
- **Target:** Caída de precio > 2% en ventana T+1.

---

## 3. Plan de Ingeniería de Características (Features)
Para el nuevo proyecto `crypto-ml-predictor`, el modelo debe recibir:
1. **Lags Temporales:** Precios y volúmenes de 1, 3 y 7 días atrás.
2. **Indicadores Técnicos:** RSI, Momentum (distancia a la media móvil) y Volatilidad.
3. **Volume Shock:** Ratio Volumen Actual / Media Móvil 7d.

---

## 4. Arquitectura Propuesta para el Proyecto 3
- **Lenguaje:** Python (Scikit-learn / XGBoost).
- **Entorno:** Notebooks para validación estadística y Scripts para inferencia.
- **Infraestructura:** Desacoplada, con permisos de lectura vía IAM sobre el proyecto Hub.

---

## 5. Próximos Pasos Técnicos
1. Crear repositorio `crypto-ml-predictor`.
2. Establecer conexión Python -> BigQuery.
3. Ejecutar análisis de correlación de Pearson para validar la hipótesis inicial.
4. Entrenar Clasificador XGBoost.
