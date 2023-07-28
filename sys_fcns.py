import RPi.GPIO as GPIO
import subprocess, json
import sys
import tech

GPIO.setmode(GPIO.BCM)

def subproc():
    proc = subprocess.Popen(["/usr/bin/node","/home/yiannis/cyens/prudens-js/node/app.js", ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    json_out = json.loads(out)
    proc.terminate()
    return list(json_out["graph"].keys())

def sys_exit():
    sys.exit(0)

def sys_restart():
    GPIO.cleanup()
    for sensor in tech.sens_array: #for-loops to setup each sensor specified
        sensor.sensor_setup()
    for actuator in tech.act_array:
        actuator.actuator_setup()

def sys_stand_by():
    #while loop that exits when the controller is removed from standby
    pass