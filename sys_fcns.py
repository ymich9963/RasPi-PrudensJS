import RPi.GPIO as GPIO
import subprocess, json

GPIO.setmode(GPIO.BCM)

def subproc():
    proc = subprocess.Popen(["/usr/bin/node","/home/yiannis/cyens/prudens-js/node/app.js", ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    json_out = json.loads(out)
    proc.terminate()
    return list(json_out["graph"].keys())

def sysStandby():
    GPIO.output(3, 0)
    GPIO.output(4, 0)