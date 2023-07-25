import RPi.GPIO as GPIO
import fcns as fcn
import classes as cf

GPIO.setmode(GPIO.BCM)

def setupLED(pin):
    GPIO.setup(pin,GPIO.OUT, initial = GPIO.LOW)

def setupButton(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin,GPIO.RISING)

def setupUSR(echo_pin, trig_pin):
    GPIO.setup(echo_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(trig_pin, GPIO.OUT, initial = GPIO.LOW)

#declaring sensors and actuators as objects
sens_array = [cf.Sensor("",0,"","",None,None) for i in range(3)] #initialising array with empty sensor objects, there are 3 sensors
sens_array[0] = cf.Sensor("USR1",[17,18],"dist(X);","",fcn.getDist,setupUSR)
sens_array[1] = cf.Sensor("BTN1",[24],"atHome;","-atHome;",fcn.btn_is_held,setupButton)
sens_array[2] = cf.Sensor("BTN2",[2],"","",fcn.btn_is_pressed,setupButton)

act_array = [cf.Actuator("",0,"",None,None) for i in range(2)] #initialising array with empty sensor objects, there are 2 actuators
act_array[0] = cf.Actuator("LED1", [3], "blinkLED1slow", fcn.blinkLEDslow, setupLED)
act_array[1] = cf.Actuator("LED2", [4], "onLED2", fcn.onLED, setupLED)