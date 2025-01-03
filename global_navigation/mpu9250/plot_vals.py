#!/usr/local/bin/python3

import sys
import csv
import matplotlib.pyplot as plt

'''
reader = csv.reader(iter(sys.stdin.readline, ""), delimiter=",")
data = list(reader)


# Asumimos que cada fila tiene 3 valores para las coordenadas (x, y, z)
x = [float(row[0]) for row in data]
y = [float(row[1]) for row in data]
#z = [float(row[2]) for row in data]

# Calcular los deltas promedio de cada dimensión
avg_delta_x = (max(x) - min(x)) / 2
avg_delta_y = (max(y) - min(y)) / 2
#avg_delta_z = (max(z) - min(z)) / 2

# Promedio de los deltas
avg_delta = (avg_delta_x + avg_delta_y) / 2

# Calcular los factores de escala
scale_x = avg_delta / avg_delta_x
scale_y = avg_delta / avg_delta_y
#scale_z = avg_delta / avg_delta_z
print(scale_x)
print(scale_y)


# Aplicar la corrección de soft iron y guardar los resultados
for row in data:
    corrected_x = float(row[0]) * scale_x
    corrected_y = float(row[1]) * scale_y  # Corregir usando scale_y
    #corrected_z = float(row[2]) * scale_z  # Corregir usando scale_z

    # Imprimir los resultados corregidos con 15 decimales
    print(",".join(format(value, ".15f") for value in [corrected_x, corrected_y]))
'''
# Lee el archivo CSV con los datos corregidos
filename = 'soft.csv'

x = []
y = []

# Abre el archivo CSV y lee las columnas
with open(filename, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Si hay encabezado, lo salta
    for row in reader:
        # Convierte los valores en flotantes
        x.append(float(row[0]))
        y.append(float(row[1]))

# Crea el gráfico
plt.figure(figsize=(8, 6))
plt.xlim(-150,150)
plt.ylim(-100,100)

plt.scatter(x, y, c='blue', label='Datos corregidos')  # Usa scatter para puntos individuales
plt.title('Gráfico de valores corregidos')
plt.xlabel('MagX Corregido')
plt.ylabel('MagY Corregido')
plt.grid(True)
plt.legend()
plt.show()
'''
