import RPi.GPIO as GPIO
import time
import curses

GPIO.setwarnings(False)

ena = 18
enb = 12
out1 = 20 #right coil MARRON
out2 = 26 #right coil BLANCO
out3 = 19 # left coil NEGRO
out4 = 16 # left coil ROJO

GPIO.setmode( GPIO.BCM )
GPIO.setup( ena, GPIO.OUT )
GPIO.setup( enb, GPIO.OUT )

GPIO.setup( out1, GPIO.OUT )
GPIO.setup( out2, GPIO.OUT )
GPIO.setup( out3, GPIO.OUT )
GPIO.setup( out4, GPIO.OUT )

pa = GPIO.PWM(ena,500)
pb = GPIO.PWM(enb,500)

pa.start(100)
pb.start(100)

def move_forward():
	for i in range(300000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
		
def move_backward():
	for i in range(300000):
		GPIO.output( out1, GPIO.HIGH )
		GPIO.output( out2, GPIO.LOW )
		GPIO.output( out3, GPIO.HIGH )
		GPIO.output( out4, GPIO.LOW )
		
def move_left():
	for i in range(200000):
		GPIO.output( out1, GPIO.LOW )
		GPIO.output( out2, GPIO.HIGH )
		GPIO.output( out3, GPIO.HIGH )
		GPIO.output( out4, GPIO.LOW )
		
def move_right():
	for i in range(200000):
		GPIO.output( out1, GPIO.HIGH )
		GPIO.output( out2, GPIO.LOW )
		GPIO.output( out3, GPIO.LOW )
		GPIO.output( out4, GPIO.HIGH )
def stop():
	GPIO.output( out1, GPIO.LOW )
	GPIO.output( out2, GPIO.LOW )
	GPIO.output( out3, GPIO.LOW )
	GPIO.output( out4, GPIO.LOW )

def main():
	move_forward()
	stop()
	time.sleep(2)
	move_backward()
	#move_left()
	#move_right()

	


main()        
GPIO.cleanup()
