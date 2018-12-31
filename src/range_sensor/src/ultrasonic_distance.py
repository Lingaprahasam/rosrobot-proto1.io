#Libraries
import RPi.GPIO as GPIO
import time

# Speed of ultrasonic sound 343m/s
SpeedOfUSound = 34300

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

#set GPIO Pins
GPIO_TRIGGER = 11
GPIO_ECHO = 12

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# lastState = False

def init_sensor():
    #
    GPIO.output(GPIO_TRIGGER, False)
    print "waiting for sensor to settle"
    time.sleep(2)

def distance_basic():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 10 micro seconds to LOW
    time.sleep(0.000001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * SpeedOfUSound) / 2
 
    return distance

def MeasureDistance():    
    # Measure distance every 1 second time
    try:
        while True:
            dist = distance_basic()
            
            if dist < 0:
                print ("Error: Distance Sensor Measurement")
                continue
            else:
                print ("Process: Measured Distance = %.1f cm" % dist)

            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Info: Measurement stopped by User")        

    except:
        print ("Info: Uncontrolled Error!")
 
if __name__ == '__main__':
    try:
        # Initialize sensor
        init_sensor()

        # Start Measurement
        MeasureDistance()    

    finally:
        # GPIO pin Clean up
        GPIO.cleanup()