import RPi.GPIO as GPIO
from drivers import hc_sr04 as usr
from drivers import button as btn
from drivers import led
import sys_fcns as fcn 
import classes as cf

GPIO.setmode(GPIO.BCM) #use GPIO numbers instead of board pin numbers

#declaring sensors and actuators as objects
sens_array = [cf.Sensor("",0,"","",None,None) for i in range(3)] #initialising array with empty sensor objects, there are 3 sensors
sens_array[0] = cf.Sensor("USR1",[17,18],"dist(X);","",usr.getDist,usr.setupUSR)
sens_array[1] = cf.Sensor("BTN1",[24],"btn1_pressed;","-btn1_pressed;",btn.btn_is_held,btn.setupButton)
sens_array[2] = cf.Sensor("BTN2",[2],"","",btn.btn_is_pressed,btn.setupButton)

act_array = [cf.Actuator("",0,"",None,None) for i in range(4)] #initialising array with empty sensor objects, there are 2 actuators
act_array[0] = cf.Actuator("LED1", [3], "blinkLED1slow", led.blinkLEDslow, led.setupLED)
act_array[1] = cf.Actuator("LED2", [4], "onLED2", led.onLED, led.setupLED)
act_array[2] = cf.Actuator("LED1", [3], "blinkLED1fast", led.blinkLEDfast, None) #use None for setup function when having duplicate actions for actuators
act_array[3] = cf.Actuator("all_LED_off", None, "all_LED_off", led.all_offLED, None)
