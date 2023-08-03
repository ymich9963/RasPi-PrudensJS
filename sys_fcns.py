import RPi.GPIO as GPIO
import subprocess, json
import sys
import spidev
import os

GPIO.setmode(GPIO.BCM)

# Enable SPI
spi = spidev.SpiDev(0, 0)
spi.max_speed_hz = 250000

def subproc():
    proc = subprocess.Popen(["/usr/bin/node","/home/yiannis/cyens/prudens-js/node/app.js", ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    #print(out)
    #print(err)
    json_out = json.loads(out)
    proc.terminate()
    return list(json_out["graph"].keys())

def adc_read(channel):
    msg = [0b1, (0b1000 + channel) << 4, 0]
    d_out = spi.xfer2(msg)
    #First value is ANDed with 0b11  and shifted by 8 to the left, then the 2nd value is added
    adc_out = ((d_out[1] & 0b11) << 8) + d_out[2]  
    return adc_out

def sys_exit():
    GPIO.cleanup()
    sys.exit(0)
    spi.close()

def sys_restart():
    GPIO.cleanup()
    for sensor in tech.sens_array: #for-loops to setup each sensor specified
        sensor.sensor_setup()
    for actuator in tech.act_array:
        actuator.actuator_setup()

def sys_stand_by():
    #while loop that exits when the controller is removed from standby
    pass

def debug_print():
        print("debug here")

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def copy_from_USB():
    #copies driver files found on USB
    if os.path.exists("//media/yiannis/DRIVER_USB/RasPi-PrudensJS/drivers/"):
        os.system("cp -r //media/yiannis/DRIVER_USB/RasPi-PrudensJS/drivers ~/cyens")


def print_adc_readings():
    print("Potentiometre reading: ", pot_reading)
    print("Temperature reading: ", temp_reading)
    print("Light reading: ", light_reading)

def manual_all_adc_sensor_read():
    pot_reading = fcn.adc_read(0)
    temp_reading = fcn.adc_read(1)
    light_reading = fcn.adc_read(2)