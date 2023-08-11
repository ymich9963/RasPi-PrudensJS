"""
    Driver for LEDs. Contains the setup function and any action functions.
"""

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

LED_pin_array = []

def setupLED(pin):
    GPIO.setup(pin,GPIO.OUT, initial = GPIO.LOW)
    LED_pin_array.append(pin)

def blinkLEDslow(pin):
    GPIO.output(pin, 1)
    sleep(0.5)
    GPIO.output(pin, 0)
    sleep(0.5)
    
def blinkLEDfast(pin):
    GPIO.output(pin, 1)
    sleep(0.05)
    GPIO.output(pin, 0)
    sleep(0.05)

def onLED(pin):
    GPIO.output(pin, 1)
    
def offLED(pin):
    GPIO.output(pin, 0)

def all_offLED():
    for pin in LED_pin_array:
        GPIO.output(pin, 0)