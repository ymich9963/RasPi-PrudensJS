import RPi.GPIO as GPIO
import subprocess, json
import sys
import spidev
import os
import importlib

GPIO.setmode(GPIO.BCM)

# Enable SPI
spi = spidev.SpiDev(0, 0)
spi.max_speed_hz = 250000

#function to interface with Prudens
def subproc(context_inp):
    # proc = subprocess.Popen(
    #     ["/usr/bin/node","/home/yiannis/cyens/prudens-js/node/app.js", context_inp],
    #     stdin=subprocess.PIPE,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE
    # )
    proc = subprocess.run(
        args = ["/usr/bin/node","/home/yiannis/cyens/prudens-js/node/app.js", context_inp],
        capture_output = True,
        text = True,
        #check = True
    )

    


    #print("stdout: ",proc.stdout)
    #print(proc.args)
    #raise SystemExit()
    # bytes_context = bytes(context_inp, "utf-8")
    # print(bytes_context)
    # out, err = proc.communicate(input=bytes_context)
    json_out = json.loads(proc.stdout)
    #print(json_out)
    # proc.terminate()


    #return [json.loads(r) for r in proc.stdout.splitlines()]

    #return json.loads(proc.stdout)


    return list(json_out["graph"].keys())

#Read a single value from ADC
def adc_read(channel):
    msg = [0b1, (0b1000 + channel) << 4, 0]
    d_out = spi.xfer2(msg)
    #First value is ANDed with 0b11  and shifted by 8 to the left, then the 2nd value is added
    adc_out = ((d_out[1] & 0b11) << 8) + d_out[2]  
    return adc_out

#exit the program gracefully
def sys_exit():
    GPIO.cleanup()
    sys.exit(0)
    spi.close()

#restart the program my re-initialising the setup
def sys_restart(sens_array, act_array, module):
    GPIO.cleanup()
    importlib.reload(module)
    for sensor in sens_array: #for-loops to setup each sensor specified
        sensor.sensor_setup()
    for actuator in act_array:
        actuator.actuator_setup()

#TODO: used to pause the system
def sys_stand_by():
    #while loop that exits when the controller is removed from standby
    pass

#print to use for debugging
def debug_print():
        print("debug here")

#used to map value with one range, to another range
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#copies driver files found on USB
def copy_from_USB():
    if os.path.exists("//media/yiannis/DRIVER_USB/RasPi-PrudensJS/drivers/"):
        os.system("cp -r //media/yiannis/DRIVER_USB/RasPi-PrudensJS/drivers ~/cyens")


def print_adc_readings(pot_reading, temp_reading, light_reading):
    print("Potentiometre reading: ", pot_reading)
    print("Temperature reading: ", temp_reading)
    print("Light reading: ", light_reading)

def manual_all_adc_sensor_read():
    pot_reading = adc_read(0)
    temp_reading = adc_read(1)
    light_reading = adc_read(2)