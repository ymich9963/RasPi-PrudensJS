import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

def setupUSR(echo_pin, trig_pin):
    GPIO.setup(echo_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(trig_pin, GPIO.OUT, initial = GPIO.LOW)

def getDist(echo_pin, trig_pin):
    GPIO.output(trig_pin, 0)
    sleep(0.0000005)
    GPIO.output(trig_pin, 1)
    sleep(0.000001)
    GPIO.output(trig_pin, 0)
    speed_of_sound = 343.26
    timeout = 100000
    pulse_start = 0
    while GPIO.input(echo_pin) == 0 and timeout != 0:
        timeout -= 1
        pulse_start = time.time()
    pulse_end = pulse_start
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()
    _dist = 100 * (pulse_end - pulse_start) * speed_of_sound / 2 #*100 for cm
    if _dist < 0:
        _dist = 0
    elif _dist > 100:
        _dist = 100 #100 is max dist
    return _dist