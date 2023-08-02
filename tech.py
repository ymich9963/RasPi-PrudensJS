import RPi.GPIO as GPIO
from drivers import hc_sr04 as usr
from drivers import button as btn
from drivers import led
from drivers import DFR0023_temp as temp
from drivers import DFR0025_light as light
from drivers import potentiometre as pot
import classes as cf
import sys_fcns as fcn

GPIO.setmode(GPIO.BCM) #use GPIO numbers instead of board pin numbers

SENSOR_AMOUNT = 6 #Digital sensors are the ones that send digital data
#ADC sensors are the ones that are connected to the channels of the MCP3008
ACTUATOR_AMOUNT = 4

#declaring sensors and actuators as objects
sens_array = [cf.Sensor] * SENSOR_AMOUNT #initialising array with empty sensor objects, there are 3 sensor
sens_array[0] = cf.Sensor("USR1",[17,18],"dist(X);","",usr.getDist,usr.setupUSR)
sens_array[1] = cf.Sensor("BTN1",[24],"btn1_pressed;","-btn1_pressed;",btn.btn_is_held,btn.setupButton)
sens_array[2] = cf.Sensor("BTN2",[2],"","",btn.btn_is_pressed,btn.setupButton)
sens_array[3] = cf.Sensor("TEMP1",1,"temp(X);","",temp.printTemp, adc_fcn = fcn.adc_read)
sens_array[4] = cf.Sensor("LIGHT1",2,"light_intensity(X);","",light.printLightInt, adc_fcn = fcn.adc_read)
sens_array[5] = cf.Sensor("POT1",0,"pot_value(X);","",pot.printPotValue, adc_fcn = fcn.adc_read)

act_array = [cf.Actuator] * ACTUATOR_AMOUNT #initialising array with empty sensor objects, there are 2 actuators
act_array[0] = cf.Actuator("LED1", [3], "blinkLED1slow", led.blinkLEDslow, led.setupLED)
act_array[1] = cf.Actuator("LED2", [4], "onLED2", led.onLED, led.setupLED)
act_array[2] = cf.Actuator("LED1", [3], "blinkLED1fast", led.blinkLEDfast, None) #use None for setup function when having duplicate actions for actuators
act_array[3] = cf.Actuator("all_LED_off", None, "all_LED_off", led.all_offLED, None)
