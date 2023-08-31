"""
    Driver for a button. Contains the setup function and any action functions. Buttons must always go from GPIO pin to ground.
"""
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def setupButton(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP) #pull-up resistor due to buttons connecting to ground
    GPIO.add_event_detect(pin,GPIO.RISING) #add the event to the Interrupt Service Routine (ISR)
    
def btn_is_pressed(pin):
    return GPIO.event_detected(pin) #checks in the ISR

def btn_is_held(pin):
    return not GPIO.input(pin) #using not due to pull-up resistor

