import RPi.GPIO as GPIO
from time import sleep
import time
import subprocess, json

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

def setupButton(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin,GPIO.RISING)

def btn_is_pressed(pin):
    return GPIO.event_detected(pin)

def btn_is_held(pin):
    return not GPIO.input(pin)

def setupUSR(echo_pin, trig_pin):
    GPIO.setup(echo_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(trig_pin, GPIO.OUT, initial = GPIO.LOW)
    
def getDist(echo_pin, trig_pin):
    GPIO.output(trig_pin, 0)
    sleep(0.000002)
    GPIO.output(trig_pin, 1)
    sleep(0.000001)
    GPIO.output(trig_pin, 0)
    speed_of_sound = 343.26
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()
    return (pulse_end - pulse_start) * 343.26 / 2

def subproc():
    proc = subprocess.Popen(["/usr/bin/node","/home/yiannis/cyens/prudens-js/node/app.js", ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    json_out = json.loads(out)
    proc.terminate()
    return list(json_out["graph"].keys())

def onLED(pin):
    GPIO.output(pin, 1)
    
def offLED(pin):
    GPIO.output(pin, 0)

def sysStandby():
    GPIO.output(3, 0)
    GPIO.output(4, 0)


setupLED(3)
setupLED(4)
setupButton(24)
setupButton(2)
setupUSR(17, 18)