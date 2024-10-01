from mpu6050 import mpu6050
import math
import time
 
 
mpu = mpu6050(0x68)

 
roll=0
pitch=0
yaw=0
tLoop=0
cnt=0


while True:
    tStart = time.time()
    
    gyro_data = mpu.get_gyro_data()

    xGyro=gyro_data['x']
    yGyro=gyro_data['y']
    zGyro=gyro_data['z']
    
    roll=roll+yGyro*tLoop
    pitch=pitch+xGyro*tLoop
    yaw=yaw+zGyro*tLoop
    cnt=cnt+1
    if cnt==10:
        cnt=0
        print('R: ',roll,'P: ',pitch,'Y: ',yaw)
    tStop=time.time()
    tLoop=tStop-tStart
