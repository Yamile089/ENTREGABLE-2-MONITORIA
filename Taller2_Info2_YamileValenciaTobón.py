# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 22:44:48 2023

@author: Yami
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import io

# Cargar el archivo .mat
mat_data = io.loadmat(r"C:\Users\Yami\OneDrive - Universidad de Antioquia\BIOINGENIERÍA\SEMESTRE 4\INFORMATICA 2\ENTREGABLE 2 MONITORIA\r01_edfm (1).mat") 

# Extraer las llaves individualmente
header = mat_data['__header__']
version = mat_data['__version__']
globals_var = mat_data['__globals__']
val = mat_data['val']

# Cargar datos CSV con pandas y manejar cadenas vacías
csv_data = pd.read_csv(
    r"C:\Users\Yami\OneDrive - Universidad de Antioquia\BIOINGENIERÍA\SEMESTRE 4\INFORMATICA 2\ENTREGABLE 2 MONITORIA\csv_data.csv",  # Reemplaza con la ruta correcta
    delimiter=';', skiprows=1,
    converters={4: lambda x: float(x.replace(',', '.')) if x else np.nan},
)

# Eliminar filas con valores nulos (NaN)
csv_data = csv_data.dropna()

def calcular_estadisticas(fragmento):
    minimo_valor = np.min(fragmento)
    maximo_valor = np.max(fragmento)
    media_valor = np.mean(fragmento)
    return minimo_valor, maximo_valor, media_valor

# Función para graficar unicamente los datos pares, los demás, definir como 0 en grafica de puntos
def graficar_datos_pares(columna):
    plt.scatter(np.arange(0, len(columna), 2), columna[::2], label="Datos Pares")
    plt.xlabel("Índice")
    plt.ylabel("Valor")
    plt.title("Gráfica de Datos Pares - Yamile Valencia")
    plt.legend()
    plt.show()

# Función para graficar una función seno utilizando numpy
def graficar_funcion_seno(columna):
    x = columna
    y = np.sin(x)
    plt.plot(x, y, label="Función Seno")
    plt.xlabel("Valor de la Columna")
    plt.ylabel("sin(Columna)")
    plt.title("Gráfica de Función Seno - Yamile Valencia")
    plt.legend()
    plt.show()

# Bucle principal
while True:
    # Obtener el número de columna del usuario
    try:
        column_number = int(input("Por favor, ingrese el número de columna que desea ver (1-5): "))
        if not (1 <= column_number <= 5):
            raise ValueError("Número de columna fuera de rango.")
    except ValueError as ve:
        print(f"Error: {ve}")
        continue

    columna = val[:, column_number-1]  # Ajustar el índice de la columna

    # Gráfica 1: Longitud de la columna
    plt.plot(np.arange(len(columna)), columna, label=f"Columna {column_number} (Longitud)")
    plt.xlabel("Longitud")
    plt.ylabel(f"Columna {column_number}")
    plt.title(f"Longitud de la Columna {column_number} - Yamile Valencia")
    plt.legend()
    plt.show()

    # Obtener el input del usuario para el fragmento
    try:
        min_value = float(input("Por favor, ingrese el valor mínimo del fragmento: "))
        max_value = float(input("Por favor, ingrese el valor máximo del fragmento: "))
    except ValueError:
        print("Ingrese valores numéricos válidos.")
        continue

    # Recortar los datos según los valores ingresados por el usuario
    fragmento = columna[(columna >= min_value) & (columna <= max_value)]

    if len(fragmento) == 0:
        print("El fragmento seleccionado es de tamaño cero. No se pueden realizar cálculos.")
        continue

    # Calcular estadísticas y mostrar
    minimo, maximo, media = calcular_estadisticas(fragmento)
    print(f"\nMínimo: {minimo}\nMáximo: {maximo}\nMedia: {media}")

    # Gráfica 2: Puntos del fragmento
    plt.scatter(np.arange(len(fragmento)), fragmento, label=f"Columna {column_number} (Fragmento)")
    plt.xlabel("Índice")
    plt.ylabel(f"Columna {column_number}")
    plt.title(f"Puntos del Fragmento de la Columna {column_number} - Yamile Valencia")
    plt.legend()
    plt.show()

    # Gráfica 3: Datos pares
    graficar_datos_pares(columna)

    # Gráfica 4: Función seno
    graficar_funcion_seno(columna)

    # Continuar el bucle hasta que el usuario ingrese 'exit'
    continue_loop = input("Desea continuar? (Ingrese 'exit' para salir): ")
    if continue_loop.lower() != "exit":
        continue
    else:
        break