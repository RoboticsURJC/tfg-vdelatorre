import RPi.GPIO as GPIO
import time
import curses
from mpu6050 import mpu6050
import math
import time
import threading
from gyro9 import measure

 
mpu = mpu6050(0x68)


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
		
def move_forward():
	pa.ChangeDutyCycle(100)
	pb.ChangeDutyCycle(100)
	for i in range(550000):
		GPIO.output( out1, GPIO.HIGH )
		GPIO.output( out2, GPIO.LOW )
		GPIO.output( out3, GPIO.HIGH )
		GPIO.output( out4, GPIO.LOW )
		
def move_right_45():
	pa.ChangeDutyCycle(80)
	pb.ChangeDutyCycle(80)
	for i in range(365000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )###
		GPIO.output( out3, GPIO.HIGH )###
		GPIO.output( out4, GPIO.LOW )
		
def move_left_45():
	for i in range(350000):
		GPIO.output( out1, GPIO.HIGH )###
		GPIO.output( out2, GPIO.LOW )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
def stop():
	pa.ChangeDutyCycle(0)
	pb.ChangeDutyCycle(0)
	GPIO.output( out1, GPIO.LOW )
	GPIO.output( out2, GPIO.LOW )
	GPIO.output( out3, GPIO.LOW )
	GPIO.output( out4, GPIO.LOW )
	
def move_360_degrees():
	for i in range(2):
		move_right_45()
		stop()
		time.sleep(2)
		
def move_3_steps():
	for i in range(7):
		move_forward()
		stop()
		time.sleep(2)

def main():
	

	hilo1 = threading.Thread(target=measure)
	hilo1.start()
	
	time.sleep(1)
	
	pa.ChangeDutyCycle(94)
	pb.ChangeDutyCycle(98)
	#move_forward()
	print("moviendoseee----------------------__")
	
	for i in range(1200000):#700000
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
		
	stop()
	time.sleep(2)
	
	#hilo1.join()
	'''
	pa.ChangeDutyCycle(94)
	pb.ChangeDutyCycle(98)
	for i in range(1200000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
		
	stop()
	time.sleep(2)
	
	pa.ChangeDutyCycle(94)
	pb.ChangeDutyCycle(98)
	for i in range(1200000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
		
	stop()
	time.sleep(2)
	
	pa.ChangeDutyCycle(94)
	pb.ChangeDutyCycle(98)
	for i in range(1200000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
		
	stop()
	time.sleep(2)
	
	pa.ChangeDutyCycle(94)
	pb.ChangeDutyCycle(98)
	for i in range(1200000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
		
	stop()
	time.sleep(2)
	'''

	

	
def cleanup():
    #enb??
    pa.stop()
    pb.stop()
    GPIO.output( [out1,out2,out3,out4, ena,enb], GPIO.LOW )
    GPIO.cleanup()

main()        
cleanup()
