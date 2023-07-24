from gpiozero import LEDBoard, DistanceSensor, Button
from time import sleep
import subprocess, json

LED0 = 3
LED1 = 4

leds = LEDBoard(LED0,LED1)
sensorDist = DistanceSensor(echo=17, trigger=18)
button1 = Button(24)
button2 = Button(2)

act_array[0] = Actuator("LED", 3, "blinkLEDslow", "blinkLED1slow")
act_array[1] = Actuator("LED", 3, "blinkLEDfast", "blinkLED1fast")

sens_array[0] = Sensor("Dist", 1718, "dist(X)")
sens_array[1] = Sensor("Button", 24, "atHome", "-atHome")

class Sensor:
	sensor_id = 0
	def __init__(self, sensor_type, sensor_port, literal_inp, literal_inp_neg):
		Sensor.sensor_id += 1
		self.sensor_type = sensor_type
		self.sensor_port = sensor_port
		self.literal_inp = literal_inp
		self.literal_inp_neg = literal_inp_neg
		
class Actuator:
	actuator_id = 0
	def __init__(self, actuator_type, actuator_port, actuator_fcn, prudens_on):
		Actuator.actuator_id += 1
		self.actuator_type = actuator_type
		self.actuator_port = actuator_port
		self.actuator_fcn = actuator_fcn
		self.prudens_output = prudens_on
	

def subproc():
    proc = subprocess.Popen(["/usr/bin/node","/home/yiannis/cyens/prudens-js/node/app.js", ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    json_out = json.loads(out)
    proc.terminate()
    return list(json_out["graph"].keys())
    
def blinkLEDslow(led_id):
    for i in range(len(leds)):
        leds[i].off()
    leds[led_id].on()
    sleep(1)
    leds[led_id].off()

def blinkLEDfast(led_id): 
    for i in range(len(leds)):
        leds[i].off()
    leds[led_id].on()
    sleep(0.2)
    leds[led_id].off()
    
def onLED(led_id):
    leds[led_id].on()
    
def sysStandby():
    for i in range(len(leds)):
        leds[i].off()
    
def getDist():
    return sensorDist.distance
