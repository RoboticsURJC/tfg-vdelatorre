import RPi.GPIO as GPIO
import time
import curses
import threading
import subprocess
import math
from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *
from wifi2 import robot_position
from astar import search_path


from pynput.keyboard import Key, Listener
from collections import deque
import sys
import joblib

import numpy as np
import soundfile

import librosa

import joblib
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

# Set GPIO Pins
TRIG = 23
ECHO = 24


# Set GPIO direction (IN / OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)



sensor_deque = deque(maxlen=1)
dist_deque = deque(maxlen=1)



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
    

def distance(dist_deque):
	
	while True:
		# Set TRIG to LOW
		GPIO.output(TRIG, False)
		time.sleep(0.1)

		# Send 10us pulse to TRIG
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		start_time = time.time()
		stop_time = time.time()

		# Save StartTime
		while GPIO.input(ECHO) == 0:
			start_time = time.time()

		# Save Time of Arrival
		while GPIO.input(ECHO) == 1:
			stop_time = time.time()

		# Time difference between start and arrival
		time_elapsed = stop_time - start_time
		# Multiply with speed of sound (34300 cm/s)
		# and divide by 2, because there and back
		distance = (time_elapsed * 34300) / 2
		
		#print("DISTANCEEE: ", distance)
		
		dist_deque.append(distance)
		
		time.sleep(0.1)

    #return distance
    

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
		#print('### Without Declination ###')
		#print(heading_angle_in_degrees)
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
	for i in range(300000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
			
	stop()
	time.sleep(1)
	
def right():
	pa.ChangeDutyCycle(90)
	pb.ChangeDutyCycle(80)
	for i in range(300000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )###
		GPIO.output( out3, GPIO.HIGH)###
		GPIO.output( out4, GPIO.LOW )
		
	stop()
	time.sleep(1)
	
def left():
	pa.ChangeDutyCycle(90)
	pb.ChangeDutyCycle(80)
	for i in range(300000):
		GPIO.output( out1, GPIO.HIGH )
		GPIO.output( out2, GPIO.LOW )###
		GPIO.output( out3, GPIO.LOW )###
		GPIO.output( out4, GPIO.HIGH )
		
		
		
	stop()
	time.sleep(1)
	
def feature_chromagram(waveform, sample_rate):
    # STFT computed here explicitly; mel spectrogram and MFCC functions do this under the hood
    stft_spectrogram=np.abs(librosa.stft(waveform))
    # Produce the chromagram for all STFT frames and get the mean of each column of the resulting matrix to create a feature array
    chromagram=np.mean(librosa.feature.chroma_stft(S=stft_spectrogram, sr=sample_rate).T,axis=0)
    #print(chromagram)
    return chromagram

def feature_melspectrogram(waveform, sample_rate):
    # Produce the mel spectrogram for all STFT frames and get the mean of each column of the resulting matrix to create a feature array
    # Using 8khz as upper frequency bound should be enough for most speech classification tasks
    # 128 features

    melspectrogram=np.mean(librosa.feature.melspectrogram(y=waveform, sr=sample_rate, n_mels=128, fmax=8000).T,axis=0)
    return melspectrogram

def feature_mfcc(waveform, sample_rate):
    # Compute the MFCCs for all STFT frames and get the mean of each column of the resulting matrix to create a feature array
    # 40 filterbanks = 40 coefficients
    # 40 features
    mfc_coefficients=np.mean(librosa.feature.mfcc(y=waveform, sr=sample_rate, n_mfcc=40).T, axis=0)
    return mfc_coefficients

def get_features(file):
    # load an individual soundfile
     with soundfile.SoundFile(file) as audio:
        waveform = audio.read(dtype="float32")
        sample_rate = audio.samplerate
        # compute features of soundfile
        chromagram = feature_chromagram(waveform, sample_rate)
        melspectrogram = feature_melspectrogram(waveform, sample_rate)
        mfc_coefficients = feature_mfcc(waveform, sample_rate)

        feature_matrix=np.array([])

        print("Chromagram shape:", chromagram.shape)
        print("Melspectrogram shape:", melspectrogram.shape)
        print("MFC coefficients shape:", mfc_coefficients.shape)

        # use np.hstack to stack our feature arrays horizontally to create a feature matrix
        feature_matrix = np.hstack((chromagram, melspectrogram, mfc_coefficients))#180 features in total
        #print(feature_matrix)
        return feature_matrix
	
def turn(val1,val2):
	goal = False
	while True:
		actual = sensor_deque[-1]
		if val1 <= actual <= val2:
			print("está alineado oesteeee")
			break
			
		# Calcular la distancia a ambos extremos del rango
		delta_min = (val1 - actual) % 360
		delta_max = (val2 - actual) % 360

		# Ajustar las diferencias al rango [-180, 180]
		if delta_min > 180:
			delta_min -= 360
    
		if delta_max > 180:
			delta_max -= 360

		# Determinar la dirección de giro más corta
		if abs(delta_min) < abs(delta_max):
			if delta_min > 0:
				print(" Girar a la DERECHA")
				right()
			else:
				print("️ Girar a la IZQUIERDA")
				left()
    
		else:
			if delta_max > 0:
				print(" Girar a la DERECHA")
				right()
			else:
				print("️ Girar a la IZQUIERDA")
				left()
		
		
def turn_new():
	while True:
		actual = sensor_deque[-1]
		if ((355 < actual <= 360) or (0 <= actual <= 5)):
			print("está alineado norteee")
			break
			
		# Calcular la distancia a los extremos de ambos rangos
		delta_min1 = (355 - actual) % 360
		delta_max1 = (360 - actual) % 360
		delta_min2 = (0 - actual) % 360
		delta_max2 = (5 - actual) % 360

		# Ajustar las diferencias al rango [-180, 180]
		if delta_min1 > 180:
			delta_min1 -= 360
		if delta_max1 > 180:
			delta_max1 -= 360
		if delta_min2 > 180:
			delta_min2 -= 360
		if delta_max2 > 180:
			delta_max2 -= 360

		# Encontrar la distancia más corta
		distancias = [
			(abs(delta_min1), delta_min1),
			(abs(delta_max1), delta_max1),
			(abs(delta_min2), delta_min2),
			(abs(delta_max2), delta_max2),
		]
		_, mejor_delta = min(distancias)  # Elegimos el giro con menor distancia absoluta

		# Determinar la dirección
		if mejor_delta > 0:
			print("️ Girar a la DERECHA")
			right()
		else:
			print("️ Girar a la IZQUIERDA")
			left() 
			
def move(path,val1,val2):
	
	while True:
		if dist_deque[-1] < 10:
			stop()
		else:
			forward()
			degrees = sensor_deque[-1]

			if val1 < degrees < val2:
				print("está alineado")
			else:
				turn(val1,val2)
			
			
			x,y = robot_position()
			if (x,y) in path:
				index = path.index((x,y))
				return path[index:]
			#return path

		

def main():
	
	stop()

	hilo1 = threading.Thread(target=funcion_hilo, args=(sensor_deque,))
	hilo1.daemon = True
	hilo1.start()
	
	hilo2 = threading.Thread(target=distance, args=(dist_deque,))
	hilo2.daemon = True
	hilo2.start()

	
	time.sleep(2)


	
	comando_arecord = ['/usr/bin/arecord', '-f', 'S16_LE', '-r' ,'44000' ,'-D', 'hw:3,0' ,'-d' ,'2' ,'-f' ,'cd' ,'/home/torre/Desktop/WAV/prueba_fold/dorm.wav' ,'-c' ,'1' ] 

	proceso = subprocess.run(comando_arecord, check=True)


	loaded_model = joblib.load('modelo_final_entrenado.pkl')

	audio_path_prueba = '/home/torre/Desktop/WAV/prueba_fold/dorm.wav'
	audio_prueba = get_features(audio_path_prueba)

	audio_prueba = audio_prueba.reshape(1, -1)

	# Predict with Random Forest
	prediccion = loaded_model.predict(audio_prueba)
	
	#path = [(20,42),(19,42),(18,42),(17,41),(16,40),(15,40),(14,40),(13,40),(12,39),(11,38),(10,37),(10,36)]
	path = search_path(prediccion)
	start = (20,42)
	
	path.pop(0)
	
	
	for pos in range(0,len(path)):
		print(path[pos])
		x_diff = path[pos][0] - start[0]
		y_diff = path[pos][1] - start[1]
	    
		degrees = sensor_deque[-1]
		
		if x_diff == 0 and y_diff < 0:
			print("oeste")
			if 265 < degrees < 275:
				print("está alineado")
			else:
				turn(265,275)
			path = move(path,265,275)
			
		    
		elif x_diff == 0 and y_diff > 0:
			print("este")
			if 85 < degrees < 95:
				print("está alineado")
			else:
				turn(85,95)
			path = move(path,85,95)

		       
		elif y_diff == 0 and x_diff < 0:
			print("norte")
			if ((355 < degrees <= 360) or (0 <= degrees <= 5)):
				print("está alineado")
			else:
				turn_new()			
			path = move(path,355,360)
		  
		elif y_diff == 0 and x_diff > 0:
			print("sur")
			if 175 < degrees < 185:
				print("está alineado")
			else:
				turn(175,185)
			path = move(path,175,185)

			
		    
		if abs(x_diff) == abs(y_diff):
			if x_diff > 0 and y_diff > 0:
				print("sureste")
				if 130 < degrees < 140:
					print("está alineado")
				else:
					turn(130,140)
				path = move(path,130,140)
		    
			elif x_diff > 0 and y_diff < 0:
				print("suroeste")
				if 220 < degrees < 230:
					print("está alineado")
				else:
					turn(220,230)
				path = move(path,220,230)
		   
			elif x_diff < 0 and y_diff > 0:
				print("noreste")
				if 40 < degrees < 50:
					print("está alineado")
				else:
					turn(40,50)
				path = move(path,40,50)
		  
			elif x_diff < 0 and y_diff < 0:
				print("noroeste")		    
				if 310 < degrees < 320:
					print("está alineado")
				else:
					turn(310,320)
				path = move(path,310,320)

		
		start = path[0]#pos
	
	
	hilo1.join()
	hilo2.join()
	

	
def cleanup():
    #enb??
    pa.stop()
    pb.stop()
    GPIO.output( [out1,out2,out3,out4, ena,enb], GPIO.LOW )
    GPIO.cleanup()
    

main()        
cleanup()
