import math
import time

from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *

# Configuración del bus I2C en Raspberry Pi
bus = 1  # En Raspberry Pi, normalmente se usa el bus I2C 1

# Crear instancia del sensor
sensor = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68,
    address_mpu_slave=None,
    bus=bus,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ,
)

sensor.configure()  # Configurar el sensor


#sensor.calibrate()

# Variables para el filtro de paso bajo
filtered_magx, filtered_magy = 0, 0
#DECLINATION = -1 * 3.19  # Declinación magnética
DECLINATION = 0.5  # Declinación magnética
heading_angle_in_degrees = 0

# Función de filtro de paso bajo
def low_pass_filter(prev_value, new_value):
    return 0.85 * prev_value + 0.15 * new_value

# Función para obtener la dirección de la brújula
def compass(angle):
    if angle > 337 or angle <= 22:
        direction = 'North'
    elif angle > 22 and angle <= 67:
        direction = 'North East'
    elif angle > 67 and angle <= 112:
        direction = "East"
    elif angle > 112 and angle <= 157:
        direction = "South East"
    elif angle > 157 and angle <= 202:
        direction = "South"
    elif angle > 202 and angle <= 247:
        direction = "South West"
    elif angle > 247 and angle <= 292:
        direction = "West"
    elif angle > 292 and angle <= 337:
        direction = "North West"
    return direction
    

# Calibrar el magnetómetroooooooooooooooooooooooooo????????


# Bucle principal
while True:
    # Obtener los valores magnéticos
    magx_new, magy_new, _ = sensor.readMagnetometerMaster()
    #print(magx_new," ---  " ,magy_new," --- " ,_)
    magx_new = magx_new - (-19.8486328125)
    magy_new = magy_new - (73.828125)
    magz_cal = _ - (1.53)

    
    # Aplicar el filtro de paso bajo
    filtered_magx = low_pass_filter(filtered_magx, magx_new)
    filtered_magy = low_pass_filter(filtered_magy, magy_new)
    
    # Calcular el ángulo de dirección
    heading_angle_in_degrees = math.atan2(filtered_magx, filtered_magy) * (180 / math.pi)
    heading_angle_in_degrees_plus_declination = heading_angle_in_degrees + DECLINATION
    
    if heading_angle_in_degrees_plus_declination < 0:
        heading_angle_in_degrees += 360
        heading_angle_in_degrees_plus_declination += 360
    
    # Imprimir los resultados
    print('### Without Declination ###')
    print(heading_angle_in_degrees)
    #print(compass(heading_angle_in_degrees))
    #print(str(get_value()))
        
    #print('### Plus Declination ###')
    #print(heading_angle_in_degrees_plus_declination)
    #print(compass(heading_angle_in_degrees_plus_declination))
    
    # Esperar un poco antes de la siguiente lectura
    time.sleep(0.1)
