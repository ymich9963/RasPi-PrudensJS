import RPi.GPIO as GPIO
import subprocess, json, sys, spidev, os, importlib, threading

GPIO.setmode(GPIO.BCM)

#Enable SPI
spi = spidev.SpiDev(0, 0)
spi.max_speed_hz = 250000

#terminal formatting
blackFG_bold_whiteBG = "\033[30;1;47m"
ENDC = "\033[0m"
blackFG_bold_yellowBG = "\033[30;1;43m"
NL = "\n"

def subproc(context_inp):
    """Function to interface with Prudens

    Args:
        context_inp (string): Context to be inputed into Prudens
    """

    proc = subprocess.Popen(
        ["/usr/bin/node","/home/yiannis/cyens/blank_system/prudens-js/node/app.js", context_inp],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = proc.communicate()
    proc.terminate() 

    """
    #different method, used the one above due to proc.terminate()
    proc = subprocess.run(
        args = ["/usr/bin/node","/home/yiannis/cyens/prudens-js/node/app.js", context_inp],
        capture_output = True,
        text = True,
    )
    json_out = json.loads(proc.stdout)
    """

#   parse to JSON string
    json_out = json.loads(out)
    return list(json_out["graph"].keys())

def change_policy_version(version, max_policy_num):
    """
        code to change policy level, 
        will not be in the final version, temporarily simulates user input
    """
    pf = open("/home/yiannis/cyens/blank_system/txt/policy.txt", "w")
    path = "/home/yiannis/cyens/blank_system/txt/policy"+str(version % max_policy_num)+".txt"
    with open(path, "r") as policy:
        data = policy.read()
    pf.write(data)
    pf.close()

def adc_read(channel):
    """Read a single value from ADC. 

    Args:
        channel (int): The ADC channel to be used for a reading

    Returns:
        int: Returns ADC value
    """
    msg = [0b1, (0b1000 + channel) << 4, 0] #First value is ANDed with 0b11  and shifted by 8 to the left,then the 2nd value is added
    d_out = spi.xfer2(msg)
    adc_out = ((d_out[1] & 0b11) << 8) + d_out[2]  
    return adc_out

#Exit the program gracefully
def sys_exit():
    GPIO.cleanup()
    spi.close()
    sys.exit(0)


def sys_restart(sens_array, act_array, module):
    """Restart the program my re-initialising the setup

    Args:
        sens_array (Sensor): The sensor array initialised in the tech.py file
        act_array (Actuator): The actuator array initialised in the tech.py file
        module (module): The module to restart. By default tech.py is restarted
    """
    GPIO.cleanup()
    importlib.reload(module)
    for sensor in sens_array:
        sensor.sensor_setup()
    for actuator in act_array:
        actuator.actuator_setup()
    print(f"{blackFG_bold_yellowBG}System restarted{ENDC}")

#TODO: used to pause the system
def sys_stand_by():
    pass

#Print to use for debugging
def debug_print():
        print("debug here")

def map(x, in_min, in_max, out_min, out_max):
    """Used to map value with one range, to another range. Taken from the Arduino docs

    Args:
        x (int): Inputted data
        in_min (int): Minimum range of the inputed data
        in_max (int): Maximum range of the inputed data
        out_min (int): Minimum range of the outputed data
        out_max (int): Maximum range of the outputed data

    Returns:
        float: Data mapped to the specified range
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#Copies driver files found on USB
def copy_from_USB():
    if os.path.exists("/media/yiannis/DRIVER_USB/RasPi-PrudensJS/drivers/"):
        os.system("cp -r /media/yiannis/DRIVER_USB/RasPi-PrudensJS/drivers ~/cyens/blank_system")

#Print the ADC readings for testing
def print_adc_readings(pot_reading, temp_reading, light_reading):
    print("Potentiometre reading: ", pot_reading)
    print("Temperature reading: ", temp_reading)
    print("Light reading: ", light_reading)

#Read ADC readings for testing
def manual_all_adc_sensor_read():
    pot_reading = adc_read(0)
    temp_reading = adc_read(1)
    light_reading = adc_read(2)
