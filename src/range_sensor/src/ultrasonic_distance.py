#Libraries
import RPi.GPIO as GPIO
import time

# Speed of sound at sea level 343m/s
SpeedOfSound_sealevel = 34300

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

#set GPIO Pins
GPIO_TRIGGER = 11
GPIO_ECHO = 12

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

lastState = False

def init_sensor():
    #
    GPIO.output(GPIO_TRIGGER, False)
    print "waiting for sensor to settle"
    time.sleep(2)

def distance_basic():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, False)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, True)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = round((StopTime - StartTime),2)
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def distance_advanced():
    global SpeedOfSound_sealevel    
    global lastState

    StartTime = time.time()
    StopTime = time.time()

    if GPIO.input(GPIO_ECHO) == 0 or lastState == True:
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
 
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        lastState = False
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        lastState = True
        StopTime = time.time()           
 
    # time difference between start and arrival
    TimeElapsed = round((StopTime - StartTime), 2)    
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    if TimeElapsed > 0:
        distance = (TimeElapsed * 34300) / 2
        return distance
    else:
        return -1

def MeasureDistance():    
    # Measure distance every 1 second time
    try:
        while True:
            # dist = distance_basic()
            dist = distance_advanced()
            
            if dist == -1:
                print ("Fault on sensor measurement")
                break
            else:
                print ("Measured Distance = %.1f cm" % dist)

            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")        

    except:
        print ("Uncontrolled Error!")
 
if __name__ == '__main__':
    # Initialize sensor
    init_sensor()

    # Start Measurement
    MeasureDistance()    

    # GPIO pin Clean up
    GPIO.cleanup()