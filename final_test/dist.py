
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins
TRIG = 23
ECHO = 24

print("Distance Measurement In Progress")

# Set GPIO direction (IN / OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
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

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

