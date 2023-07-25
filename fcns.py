import RPi.GPIO as GPIO
from time import sleep
import time
import subprocess, json

GPIO.setmode(GPIO.BCM)

def blinkLEDslow(pin):
    GPIO.output(pin, 1)
    sleep(1)
    GPIO.output(pin, 0)
    
def blinkLEDfast(pin):
    GPIO.output(pin, 1)
    sleep(0.2)
    GPIO.output(pin, 0)

def btn_is_pressed(pin):
    return GPIO.event_detected(pin)

def btn_is_held(pin):
    return not GPIO.input(pin)

def getDist(echo_pin, trig_pin):
    GPIO.output(trig_pin, 0)
    sleep(0.0000005)
    GPIO.output(trig_pin, 1)
    sleep(0.000001)
    GPIO.output(trig_pin, 0)
    speed_of_sound = 343.26
    timeout = 100000
    while GPIO.input(echo_pin) == 0 and timeout != 0:
        timeout -= 1
        pulse_start = time.time()
    if timeout == 0:
        pulse_end = pulse_start
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()
    _dist = 100 * (pulse_end - pulse_start) * speed_of_sound / 2 #*100 for cm
    if _dist < 0:
        _dist = 0
    elif _dist > 100:
        _dist = 100 #100 is max dist
    return _dist

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