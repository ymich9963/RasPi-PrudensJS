"""
    Technician makes modifications here when installing new sensors and acuators.
    If a sensor/actuator is commented out the program will still work. The driver
    has to be imported by being placed in the /drivers directory. This can happen automatically
    by using a USB named DRIVER_USB with a directory of /DRIVER_USB/RasPi-PrudensJS/drivers.

    Sensor declaration format,
        cf.Sensor(
            Sensor ID,
            pin or channel,
            positive literal,
            negative literal,
            action function,
            setup function,
            adc_function
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

#use GPIO numbers instead of board pin numbers
GPIO.setmode(GPIO.BCM) 

#allow control of the number of policy files
total_policy_files = 2

#declaring sensors and actuators as objects
sens_array = [
    cf.Sensor("BTN1",[15],"","",btn.btn_is_pressed,btn.setupButton), #user input button
    cf.Sensor("BTN2",[27],"","",btn.btn_is_pressed,btn.setupButton), #restart button
]

act_array = [

]
