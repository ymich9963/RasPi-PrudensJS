import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def reset_rgb_led(pin1, pin2, pin3):
    GPIO.output([pin1, pin2, pin3], 0)

def rgb_setup(pin1, pin2, pin3):
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    reset_rgb_led(pin1, pin2, pin3)

def on_white(pin1, pin2, pin3):
    reset_rgb_led(pin1, pin2, pin3)
    GPIO.output([pin1, pin2, pin3], 1)

def off_white(pin1, pin2, pin3):
    GPIO.output([pin1, pin2, pin3], 0)
    
def on_red(pin1, pin2, pin3):
    reset_rgb_led(pin1, pin2, pin3)
    GPIO.output(pin1, 1)

def off_red(pin1, pin2, pin3):
    GPIO.output(pin1, 0)

def on_green(pin1, pin2, pin3):
    reset_rgb_led(pin1, pin2, pin3)
    GPIO.output(pin2, 1)

def off_green(pin1, pin2, pin3):
    GPIO.output(pin2, 0)
    
def on_blue(pin1, pin2, pin3):
    reset_rgb_led(pin1, pin2, pin3)
    GPIO.output(pin3, 1)

def off_blue(pin1, pin2, pin3):
    GPIO.output(pin3, 0)

def on_yellow(pin1, pin2, pin3):
    reset_rgb_led(pin1, pin2, pin3)
    GPIO.output([pin1, pin2], 1)

def off_yellow(pin1, pin2, pin3):
    GPIO.output([pin1, pin2], 0)

def on_cyan(pin1, pin2, pin3):
    reset_rgb_led(pin1, pin2, pin3)
    GPIO.output([pin2, pin3], 1)

def off_cyan(pin1, pin2, pin3):
    GPIO.output([pin2, pin3], 0)

def on_magenta(pin1, pin2, pin3):
    reset_rgb_led(pin1, pin2, pin3)
    GPIO.output([pin1, pin3], 1)

def off_magenta(pin1, pin2, pin3):
    GPIO.output([pin1, pin3], 0)