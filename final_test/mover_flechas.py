import RPi.GPIO as GPIO
import time
import curses
import threading
import subprocess
import math
from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *



from pynput.keyboard import Key, Listener
from collections import deque

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
    

def funcion_hilo(sensor_deque):
	filtered_magx, filtered_magy = 0, 0
	
	#sensor.calibrate()
	sensor.configure()  # Configurar el sensor

	#DECLINATION = -1 * 3.19  # Declinación magnética
	DECLINATION = 0.5  # Declinación magnética
	heading_angle_in_degrees = 0
	while True:
		# Obtener los valores magnéticos
		magx_new, magy_new, _ = sensor.readMagnetometerMaster()
		
		magx_new = (magx_new - (-18.89)) * 1.035070140280561
		magy_new = (magy_new - (24.82)) * 0.9672284644194756
		
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
		
		sensor_deque.append(heading_angle_in_degrees)
		
		time.sleep(0.1)

GPIO.setwarnings(False)

ena = 18
enb = 12
out1 = 20 # right coil MARRON
out2 = 26 # right coil BLANCO
out3 = 19 # left coil NEGRO
out4 = 16 # left coil ROJO

GPIO.setmode( GPIO.BCM )
GPIO.setup( ena, GPIO.OUT )
GPIO.setup( enb, GPIO.OUT )

GPIO.setup( out1, GPIO.OUT )
GPIO.setup( out2, GPIO.OUT )
GPIO.setup( out3, GPIO.OUT )
GPIO.setup( out4, GPIO.OUT )

pa = GPIO.PWM(ena,1000)
pb = GPIO.PWM(enb,1000)

pa.start(0)
pb.start(0)

def move_backward():
	pa.ChangeDutyCycle(100)
	pb.ChangeDutyCycle(100)
	for i in range(800000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
		

def stop():
	pa.ChangeDutyCycle(0)
	pb.ChangeDutyCycle(0)
	GPIO.output( out1, GPIO.LOW )
	GPIO.output( out2, GPIO.LOW )
	GPIO.output( out3, GPIO.LOW )
	GPIO.output( out4, GPIO.LOW )
	

		
		
#------------------------------
def forward():
	pa.ChangeDutyCycle(90)
	pb.ChangeDutyCycle(80)
	for i in range(900000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
			
	stop()
	time.sleep(1)
	
def right():
	pa.ChangeDutyCycle(90)
	pb.ChangeDutyCycle(80)
	for i in range(100000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )###
		GPIO.output( out3, GPIO.HIGH)###
		GPIO.output( out4, GPIO.LOW )
		
	stop()
	time.sleep(1)
	
def left():
	pa.ChangeDutyCycle(90)
	pb.ChangeDutyCycle(80)
	for i in range(100000):
		GPIO.output( out1, GPIO.HIGH )
		GPIO.output( out2, GPIO.LOW )###
		GPIO.output( out3, GPIO.LOW )###
		GPIO.output( out4, GPIO.HIGH )
		
		
		
	stop()
	time.sleep(1)
	
def on_press(key):
    if key == Key.up:
        print("Flecha arriba ")
        forward()
    elif key == Key.down:
        print("Flecha abajo ")
    elif key == Key.left:
        print("Flecha izquierda ")
        left()
    elif key == Key.right:
        print("Flecha derecha ")
        right()
    elif key == Key.esc:
        print("Saliendo del programa...")
        return False  # Detener el listener

def main():
	
	path = [(0,1),(0,2),(0,3)]
	
	
	
	
	
	
	sensor_deque = deque()
	
	hilo1 = threading.Thread(target=funcion_hilo, args=(sensor_deque,))
	hilo1.daemon = True
	hilo1.start()

	
	with Listener(on_press=on_press) as listener:
		listener.join()
	
	print("holaaaaa")
	

	
	
	#valor = sensor_deque[-1]
	#print("VALOR SENSOR EN MAIN: ", valor)
	'''
	
	pa.ChangeDutyCycle(90)
	pb.ChangeDutyCycle(80)
	for i in range(80000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.HIGH )
		GPIO.output( out4, GPIO.LOW )
		
	stop()
	time.sleep(1)
	
	
	'''
	
	#hilo1.join()
	

	
def cleanup():
    #enb??
    pa.stop()
    pb.stop()
    GPIO.output( [out1,out2,out3,out4, ena,enb], GPIO.LOW )
    GPIO.cleanup()
    

main()        
cleanup()
