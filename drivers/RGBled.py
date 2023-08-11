"""
    Driver for an RGB. Contains the setup function, reset and on/off for each colour.
"""


import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def reset_rgb_led(red_pin, green_pin, blue_pin):
    GPIO.output([red_pin, green_pin, blue_pin], 0)

def rgb_setup(red_pin, green_pin, blue_pin):
    GPIO.setup(red_pin, GPIO.OUT)
    GPIO.setup(green_pin, GPIO.OUT)
    GPIO.setup(blue_pin, GPIO.OUT)
    reset_rgb_led(red_pin, green_pin, blue_pin)

def on_white(red_pin, green_pin, blue_pin):
    reset_rgb_led(red_pin, green_pin, blue_pin)
    GPIO.output([red_pin, green_pin, blue_pin], 1)

def off_white(red_pin, green_pin, blue_pin):
    GPIO.output([red_pin, green_pin, blue_pin], 0)
    
def on_red(red_pin, green_pin, blue_pin):
    reset_rgb_led(red_pin, green_pin, blue_pin)
    GPIO.output(red_pin, 1)

def off_red(red_pin, green_pin, blue_pin):
    GPIO.output(red_pin, 0)

def on_green(red_pin, green_pin, blue_pin):
    reset_rgb_led(red_pin, green_pin, blue_pin)
    GPIO.output(green_pin, 1)

def off_green(red_pin, green_pin, blue_pin):
    GPIO.output(green_pin, 0)
    
def on_blue(red_pin, green_pin, blue_pin):
    reset_rgb_led(red_pin, green_pin, blue_pin)
    GPIO.output(blue_pin, 1)

def off_blue(red_pin, green_pin, blue_pin):
    GPIO.output(blue_pin, 0)

def on_yellow(red_pin, green_pin, blue_pin):
    reset_rgb_led(red_pin, green_pin, blue_pin)
    GPIO.output([red_pin, green_pin], 1)

def off_yellow(red_pin, green_pin, blue_pin):
    GPIO.output([red_pin, green_pin], 0)

def on_cyan(red_pin, green_pin, blue_pin):
    reset_rgb_led(red_pin, green_pin, blue_pin)
    GPIO.output([green_pin, blue_pin], 1)

def off_cyan(red_pin, green_pin, blue_pin):
    GPIO.output([green_pin, blue_pin], 0)

def on_magenta(red_pin, green_pin, blue_pin):
    reset_rgb_led(red_pin, green_pin, blue_pin)
    GPIO.output([red_pin, blue_pin], 1)

def off_magenta(red_pin, green_pin, blue_pin):
    GPIO.output([red_pin, blue_pin], 0)