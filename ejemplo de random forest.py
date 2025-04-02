# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 20:16:14 2025

@author: fenris123
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler



# Cargar el dataset

#WARNING:  CHANGE THE FILE PATH
#WARNING:  CHANGE THE FILE PATH
#WARNING:  CHANGE THE FILE PATH

data_path = "C:\\XXXX\\XXXX.csv"                            
df = pd.read_csv(data_path, sep=';', decimal=',')

# Mantener una copia del dataframe original con fechas para el procesamiento de valores faltantes
df_original = df.copy()
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d', errors='coerce')
df['año'] = df['fecha'].dt.year

# Manejo de valores
df.drop(columns=['indicativo'], inplace=True)

# Reemplazar 'Ip' en la columna 'prec' por 0
df['prec'] = df['prec'].replace('Ip', 0.0)

# Lista de las columnas específicas que quieres modificar para cambiar comas por puntos
cols_to_modify = ['altitud', 'tmed', 'prec', 'tmin',  'tmax',
                  'dir', 'velmedia', 'racha', 'sol', 'presMax', 'presMin', 
                  'hrMedia', 'hrMax', 'hrMin']

# Reemplazar las comas por puntos en las columnas específicas
for col in cols_to_modify:
    df[col] = df[col].apply(lambda x: str(x).replace(',', '.') if isinstance(x, str) else x)

# Convertir a valores numéricos
df[cols_to_modify] = df[cols_to_modify].apply(pd.to_numeric, errors='coerce')

# Verificar que el cambio se haya hecho correctamente
print(df[cols_to_modify].head())

# Convertir 'valor' a variable binaria (SI=1, NO=0)
df['valor'] = df['valor'].str.upper().map({'SI': 1, 'NO': 0})

# Eliminar filas con valores nulos en la variable objetivo
df.dropna(subset=['valor'], inplace=True)

# Eliminar columnas no necesarias
df.drop(columns=['fecha', 'nombre', 'provincia'], inplace=True)

# Función para convertir HH:MM a minutos desde medianoche
def time_to_minutes(time_str):
    if pd.isna(time_str) or time_str == 'Varias':
        return np.nan
    try:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    except:
        return np.nan

# Aplicar la conversión a las columnas horatmin, horatmax y horaracha
df['horatmin_minutes'] = df['horatmin'].apply(time_to_minutes)
df['horatmax_minutes'] = df['horatmax'].apply(time_to_minutes)
df['horaracha_minutes'] = df['horaracha'].apply(time_to_minutes)

# Eliminar las columnas originales de tiempo si ya no las necesitas
df.drop(columns=['horatmin', 'horatmax', 'horaracha'], inplace=True)

# Verificar la conversión
print(df[['horatmin_minutes', 'horatmax_minutes', 'horaracha_minutes']].head())

# Separar datos de entrenamiento (2022-2023) y test (2024 en adelante)
train_data = df[df['año'].isin([2022, 2023])]
test_data = df[df['año'] >= 2024]

# Separar variables predictoras y objetivo
X_train = train_data.drop(columns=['valor','año'])
y_train = train_data['valor']
X_test = test_data.drop(columns=['valor','año'])
y_test = test_data['valor']

# Estandarizar las características
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entrenar el modelo de Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42,class_weight='balanced')
model.fit(X_train_scaled, y_train)

# Obtener las probabilidades de predicción
y_proba = model.predict_proba(X_test_scaled)[:, 1]  # Probabilidades para la clase positiva (1)

# Ajustar el umbral de decisión, por ejemplo, a 0.3
y_pred = (y_proba > 0.5).astype(int)

# Evaluar el rendimiento con el nuevo umbral
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Obtener e imprimir la importancia de las características
feature_importance = model.feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': feature_importance
})

# Ordenar las características por importancia
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
print("\nImportancia de las características:")
print(feature_importance_df)

