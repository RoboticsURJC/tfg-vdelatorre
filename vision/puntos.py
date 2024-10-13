import matplotlib.pyplot as plt

# Coordenadas de los puntos en azul
puntos_azules = [(1, 1), (0, 1), (-1, 1), (0, 2), (0, 0), (-1, 0), (1, 0)]

# Coordenadas de los puntos en rojo
puntos_rojos = [(0.856, 1.061), (-0.031, 0.945), (-0.8, 1.132), 
                (0.039, 1.825), (0.139, 0.131), (-0.7, 0.1), (0.9, 0.2)]

# Separar las coordenadas en listas de X y Y
x_azul, y_azul = zip(*puntos_azules)
x_rojo, y_rojo = zip(*puntos_rojos)

# Crear el gráfico para los puntos azules
plt.scatter(x_azul, y_azul, color='blue', label='Coordenadas mapa fijas')

# Crear el gráfico para los puntos rojos
plt.scatter(x_rojo, y_rojo, color='red', label='Coordenadas aproximadas por visión')



# Configurar límites de los ejes
plt.xlim(-2, 2)
plt.ylim(-1, 3)

# Añadir las líneas del eje X y Y
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)

# Añadir título, etiquetas de los ejes y leyenda
plt.title("Representación de coordenadas del mapa")
plt.xlabel("Eje X")
plt.ylabel("Eje Y")
plt.legend()

# Mostrar la cuadrícula
plt.grid(True)

# Guardar el gráfico como una imagen
plt.savefig("Coordenadas_aproximadas_por_vision.png")

