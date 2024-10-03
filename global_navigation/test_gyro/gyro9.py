import RPi.GPIO as GPIO
import time
import curses
from mpu6050 import mpu6050
import math
import time
import matplotlib.pyplot as plt
import threading
 
mpu = mpu6050(0x68)




    
def measure():
        # Abrir el archivo en modo de escritura (añadir 'a' para añadir en lugar de sobrescribir)
        
    start = time.time()
    with open("acelerometro_datos.txt", "w") as f:
        while True:
            accel_data = mpu.get_accel_data()

            # Preparar los datos para escribir
            data_str = f"Acc X: {accel_data['x']}, Acc Y: {accel_data['y']}, Acc Z: {accel_data['z']}\n"
            
            # Escribir los datos en el archivo
            f.write(data_str)

            # También puedes imprimir si lo necesitas
            print(data_str)

            # Esperar un poco para no saturar el archivo de texto con datos
            time.sleep(0.1)
            
            if time.time() - start > 5:
                break
#measure()

   
    

