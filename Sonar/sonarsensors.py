import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#Front Sonar
TRIG1 = 23
ECHO1 = 24
#Right Sonar
TRIG2 = 27
ECHO2 = 22
#Left Sonar
TRIG3 = 5
ECHO3 = 17
#Back Sonar
TRIG4 = 4
ECHO4 = 6


GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(TRIG1, False)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)
GPIO.setup(TRIG2, False)
GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3,GPIO.IN)
GPIO.setup(TRIG3, False)
GPIO.setup(TRIG4,GPIO.OUT)
GPIO.setup(ECHO4,GPIO.IN)
GPIO.setup(TRIG4, False)

while True:
    print("Wait for Front Sonar to send signal")
    time.sleep(2)
    GPIO.output(TRIG1, True)
    time.sleep(0.00001)
    GPIO.output(TRIG1, False)
    while GPIO.input(ECHO1) == 0:
        pulse_start1 = time.time()
    while GPIO.input(ECHO1) == 1:
        pulse_end1 = time.time()
    pulse_duration1 = pulse_end1 - pulse_start1
    distance1 = pulse_duration1 * 17150
    distance1 = round(distance1,2)
    print("Distance for Front Sonar: ", distance1)

    print("Wait for Right Sonar to send signal")
    time.sleep(2)
    GPIO.output(TRIG2, True)
    time.sleep(0.00001)
    GPIO.output(TRIG2, False)
    while GPIO.input(ECHO2) == 0:
        pulse_start2 = time.time()
    while GPIO.input(ECHO2) == 1:
       pulse_end2 = time.time()
    pulse_duration2 = pulse_end2 - pulse_start2
    distance2 = pulse_duration2 * 17150
    distance2 = round(distance2,2)
    print("Distance for Right Sonar: ", distance2)

    print("Wait for Rear Sonar to send signal")
    time.sleep(2)
    GPIO.output(TRIG3, True)
    time.sleep(0.00001)
    GPIO.output(TRIG3, False)
    while GPIO.input(ECHO3) == 0:
        pulse_start3 = time.time()
    while GPIO.input(ECHO3) == 1:
        pulse_end3 = time.time()
    pulse_duration3 = pulse_end3 - pulse_start3
    distance3 = pulse_duration3 * 17150
    distance3 = round(distance3,2)
    print("Distance for Rear Sonar: ", distance3)

    print("Wait for Left Sonar to send signal")
    time.sleep(2)
    GPIO.output(TRIG4, True)
    time.sleep(0.00001)
    GPIO.output(TRIG4, False)
    while GPIO.input(ECHO4) == 0:
        pulse_start4 = time.time()
    while GPIO.input(ECHO4) == 1:
        pulse_end4 = time.time()
    pulse_duration4 = pulse_end4 - pulse_start4
    distance4 = pulse_duration4 * 17150
    distance4 = round(distance4,2)
    print("Distance for Front Sonar: ", distance4)
 
 GPIO.cleanup()
