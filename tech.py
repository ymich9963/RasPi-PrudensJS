import RPi.GPIO as GPIO
import classes as cf
import sys_fcns as fcn

#driver imports
from drivers import hc_sr04 as usr
from drivers import button as btn
from drivers import led
from drivers import DFR0023_temp as temp
from drivers import DFR0025_light as light
from drivers import potentiometre as pot
from drivers import RGBled as rgb

GPIO.setmode(GPIO.BCM) #use GPIO numbers instead of board pin numbers

#declaring sensors and actuators as objects
sens_array = [
    cf.Sensor("USR1",[17,18],"dist(X);","",usr.getDist,usr.setupUSR),
    cf.Sensor("BTN1",[24],"btn1_pressed;","",btn.btn_is_held,btn.setupButton),
    cf.Sensor("BTN2",[2],"","",btn.btn_is_pressed,btn.setupButton),
    cf.Sensor("TEMP1",1,"temp(X);","",temp.getTemp, adc_fcn = fcn.adc_read),
    cf.Sensor("LIGHT1",2,"light_intensity(X);","",light.getLightInt, adc_fcn = fcn.adc_read),
    cf.Sensor("POT1",0,"pot_value(X);","",pot.getPotValue, adc_fcn = fcn.adc_read),
    cf.Sensor("BTN3",[27],"","",btn.btn_is_pressed,btn.setupButton),

]

act_array = [
    cf.Actuator("LED1", [3], "blinkLED1slow", led.blinkLEDslow, led.setupLED),
    cf.Actuator("LED2", [4], "onLED2", led.onLED, led.setupLED),
    cf.Actuator("LED1", [3], "blinkLED1fast", led.blinkLEDfast, None), #use None for setup function when having duplicate actions for actuators
    cf.Actuator("all_LED_off", None, "all_LED_off", led.all_offLED, None),
    cf.Actuator("RGB_led",[13, 12, 6], "rgb_led_magenta_on", rgb.on_magenta,rgb.rgb_setup), #pins 13 and 12 are PWM pins
    cf.Actuator("RGB_led",[13, 12, 6], "rgb_led_magenta_off", rgb.off_magenta,None),
    cf.Actuator("RGB_led",[13, 12, 6], "rgb_led_red_on", rgb.on_red,None),
    cf.Actuator("RGB_led",[13, 12, 6], "rgb_led_red_off", rgb.off_red,None),
    cf.Actuator("RGB_led",[13, 12, 6], "rgb_led_yellow_on", rgb.on_yellow,None),
    cf.Actuator("RGB_led",[13, 12, 6], "rgb_led_yellow_off", rgb.off_yellow,None)
]