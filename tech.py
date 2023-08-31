"""
    Technician makes modifications here when installing new sensors and acuators.
    If a sensor/actuator is commented out the program will still work. The driver
    has to be imported by being placed in the /drivers directory. This can happen automatically
    by using a USB named DRIVER_USB with a directory of /DRIVER_USB/RasPi-PrudensJS/drivers. May need 
    to change the username in the path. 

    Sensor declaration format,
        cf.Sensor(
            Sensor ID,
            pin or channel,
            positive literal,
            negative literal,
            action function,
            setup function,
            adc_function (use instead of the setup function for an analogue sensor)
        )

    Actuator declaration format,
        cf.Actuator(
            actuator ID,
            pin,
            literal,
            action function,
            setup function
        )

"""

import RPi.GPIO as GPIO
import classes as cf
import sys_fcns as fcn

#driver imports
from drivers import button as btn
from drivers import hc_sr04 as usr
from drivers import led
from drivers import DFR0023_temp as temp
from drivers import DFR0025_light as light
from drivers import potentiometre as pot
from drivers import RGBled as rgb
from drivers import TMC5160 as motor

#use GPIO numbers instead of board pin numbers
GPIO.setmode(GPIO.BCM) 

#allow control of the number of policy files
total_policy_files = 9

#declaring sensors and actuators as objects
sens_array = [
    cf.Sensor("BTN1",[15],"","",btn.btn_is_pressed,btn.setupButton), #user input button
    cf.Sensor("BTN2",[27],"","",btn.btn_is_pressed,btn.setupButton), #restart button
    cf.Sensor("USR1",[17,15],"dist(X);","",usr.getDist,usr.setupUSR),
    cf.Sensor("BTN3",[24],"btn1_pressed;","-btn1_pressed;",btn.btn_is_held,btn.setupButton),
    cf.Sensor("TEMP1",1,"temp(X);","",temp.getTemp, setup_fcn=None, adc_fcn = fcn.adc_read),
    cf.Sensor("LIGHT1",2,"light_intensity(X);","",light.getLightInt, setup_fcn=None, adc_fcn = fcn.adc_read),
    cf.Sensor("POT1",0,"pot_value(X);","",pot.getPotValue, setup_fcn=None, adc_fcn = fcn.adc_read),
]

act_array = [
    cf.Actuator("LED1", [3], "blinkLED1slow", led.blinkLEDslow, led.setupLED),
    cf.Actuator("LED2", [4], "onLED2", led.onLED, led.setupLED),
    cf.Actuator("LED2", [4], "offLED2", led.offLED, None),
    cf.Actuator("LED1", [3], "blinkLED1fast", led.blinkLEDfast, None), #use None for setup function when having duplicate actions for actuators
    cf.Actuator("all_LED_off", None, "all_LED_off", led.all_offLED, None),
    cf.Actuator("RGB_led",[13, 12, 6], "rgb_led_red_on", rgb.on_red,rgb.rgb_setup),
    cf.Actuator("RGB_led",[13, 12, 6], "rgb_led_red_off", rgb.off_red,None),
    cf.Actuator("RGB_led",[13, 12, 6], "rgb_led_yellow_on", rgb.on_yellow,None),
    cf.Actuator("RGB_led",[13, 12, 6], "rgb_led_yellow_off", rgb.off_yellow,None),
    cf.Actuator("Motor1", None, "move_motor_1", motor.spin1, motor.setup),
    cf.Actuator("Motor1", None, "stop_motor", motor.stop, None),
    cf.Actuator("Motor1", None, "move_motor_2", motor.spin2, None)
]