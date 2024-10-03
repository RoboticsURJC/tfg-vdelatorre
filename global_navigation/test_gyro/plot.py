import matplotlib.pyplot as plt

# Inicializamos listas vacías para almacenar los valores de X, Y, Z
accel_x = []
accel_y = []
accel_z = []

# Leer los datos del archivo de texto
with open("acelerometro_datos.txt", "r") as f:
    for line in f:
        # Eliminar cualquier espacio en blanco o salto de línea
        line = line.strip()
        
        # Dividir la línea en componentes separadas por comas
        if line:
            parts = line.split(",")
            # Extraer los valores de X, Y, Z
            x = float(parts[0].split(":")[1].strip())
            y = float(parts[1].split(":")[1].strip())
            z = float(parts[2].split(":")[1].strip())
            
            # Agregar los valores a las listas correspondientes
            accel_x.append(x)
            accel_y.append(y)
            accel_z.append(z)

# Crear un eje de tiempo para la gráfica (suponiendo que los datos se toman en intervalos regulares)
time_axis = range(len(accel_x))

# Graficar los datos
plt.figure(figsize=(10, 6))

plt.plot(time_axis, accel_x, label='Acc X', color='r', linewidth=1)
plt.plot(time_axis, accel_y, label='Acc Y', color='g', linewidth=1)
plt.plot(time_axis, accel_z, label='Acc Z', color='b', linewidth=1)

# Añadir títulos y etiquetas
plt.title("Datos del acelerómetro")
plt.xlabel("Tiempo (muestras)")
plt.ylabel("Aceleración (g)")

# Mostrar leyenda
plt.legend()

# Mostrar la gráfica
plt.show()
