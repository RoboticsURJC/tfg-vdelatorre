#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

enb = 25
out1 = 8 #right coil MARRON
out2 = 7 #right coil BLANCO
out3 = 11 # left coil NEGRO
out4 = 5 # left coil ROJO
 
DEG_PER_STEP = 0.9
STEP_PER_REVOLUTION = int(360 / DEG_PER_STEP)

#delay btw steps
delay = 0.0032

#500 steps for 180 degrees

GPIO.setwarnings(False)

 
# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( [out1,out2,out3,out4,enb], GPIO.OUT )


pb = GPIO.PWM(enb,100)

pb.start(100)



 
# initializing
GPIO.output( out1, GPIO.LOW )
GPIO.output( out2, GPIO.LOW )
GPIO.output( out3, GPIO.LOW )
GPIO.output( out4, GPIO.LOW )
 
 
def cleanup2():
    #enb??
    GPIO.output( [out1,out2,out3,out4], GPIO.LOW )
    GPIO.cleanup()
    
   
def move_cw2():
    for _ in range(STEP_PER_REVOLUTION):
        GPIO.output( [out1,out2,out3,out4], [GPIO.LOW,GPIO.LOW,GPIO.LOW,GPIO.HIGH] )
        time.sleep(delay)
        GPIO.output( [out1,out2,out3,out4], [GPIO.LOW,GPIO.HIGH,GPIO.LOW,GPIO.LOW] )
        time.sleep(delay)
        GPIO.output( [out1,out2,out3,out4], [GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.LOW] )
        time.sleep(delay)
        GPIO.output( [out1,out2,out3,out4], [GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.LOW] )
        time.sleep(delay)
    

def move_ccw2():
    for _ in range(STEP_PER_REVOLUTION):
        GPIO.output( [out1,out2,out3,out4], [GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.LOW] )
        time.sleep(delay)
        GPIO.output( [out1,out2,out3,out4], [GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.LOW] )
        time.sleep(delay)
        GPIO.output( [out1,out2,out3,out4], [GPIO.LOW,GPIO.HIGH,GPIO.LOW,GPIO.LOW] )
        time.sleep(delay)
        GPIO.output( [out1,out2,out3,out4], [GPIO.LOW,GPIO.LOW,GPIO.LOW,GPIO.HIGH] )
        time.sleep(delay)
    
''' 
move_cw2()

pb.ChangeDutyCycle(90)
time.sleep(1)
move_ccw2()  
''' 

'''
# the meat
try:
    i = 0
    for i in range(500):
        if i%4==0:
            GPIO.output( out4, GPIO.HIGH )
            GPIO.output( out3, GPIO.LOW )
            GPIO.output( out2, GPIO.LOW )
            GPIO.output( out1, GPIO.LOW )
        elif i%4==1:
            GPIO.output( out4, GPIO.LOW )
            GPIO.output( out3, GPIO.LOW )
            GPIO.output( out2, GPIO.HIGH )
            GPIO.output( out1, GPIO.LOW )
        elif i%4==2:
            GPIO.output( out4, GPIO.LOW )
            GPIO.output( out3, GPIO.HIGH )
            GPIO.output( out2, GPIO.LOW )
            GPIO.output( out1, GPIO.LOW )
        elif i%4==3:
            GPIO.output( out4, GPIO.LOW )
            GPIO.output( out3, GPIO.LOW )
            GPIO.output( out2, GPIO.LOW )
            GPIO.output( out1, GPIO.HIGH )
 
        time.sleep( delay )
 
except KeyboardInterrupt:
    cleanup()
    exit( 1 )

 
cleanup2()
exit( 0 )'''
