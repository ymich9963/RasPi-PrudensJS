import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def setupButton(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin,GPIO.RISING)
    
def btn_is_pressed(pin):
    return GPIO.event_detected(pin)

def btn_is_held(pin):
    return not GPIO.input(pin)

