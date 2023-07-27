import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

def setupLED(pin):
    GPIO.setup(pin,GPIO.OUT, initial = GPIO.LOW)

def blinkLEDslow(pin):
    GPIO.output(pin, 1)
    sleep(1)
    GPIO.output(pin, 0)
    
def blinkLEDfast(pin):
    GPIO.output(pin, 1)
    sleep(0.2)
    GPIO.output(pin, 0)

def onLED(pin):
    GPIO.output(pin, 1)
    
def offLED(pin):
    GPIO.output(pin, 0)