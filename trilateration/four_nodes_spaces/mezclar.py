import csv
import random

# Leer el archivo CSV
with open('muestras (otra copia).txt', mode='r') as file:
    reader = list(csv.reader(file))  # Convertimos el archivo en una lista de listas
    header = reader[0]  # Guardamos el encabezado por separado
    rows = reader[1:]  # Guardamos las filas de datos

# Mezclar solo las filas de datos
random.shuffle(rows)

# Guardar el archivo de salida con las filas mezcladas
with open('salida.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # Escribir el encabezado
    writer.writerows(rows)  # Escribir las filas mezcladas

