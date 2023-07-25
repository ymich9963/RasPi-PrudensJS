import RPi.GPIO as GPIO
import fcns as fcn

GPIO.setmode(GPIO.BCM)

def setupLED(pin):
    GPIO.setup(pin,GPIO.OUT, initial = GPIO.LOW)

def setupButton(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin,GPIO.RISING)

def setupUSR(echo_pin, trig_pin):
    GPIO.setup(echo_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(trig_pin, GPIO.OUT, initial = GPIO.LOW)

class Sensor:
    def __init__(self, sensor_id:str, pin:int, literal_pos:str, literal_neg:str, action_fcn, setup_fcn):
        self.sensor_id = sensor_id
        self.pin = pin
        self.literal_pos = literal_pos
        self.literal_neg = literal_neg
        self.action_fcn = action_fcn
        self.setup_fcn = setup_fcn

    def sensor_config(self):
        size = len(self.pin)
        if size == 1:
            self.setup_fcn(self.pin[0])
        elif size == 2:
            self.setup_fcn(self.pin[0],self.pin[1])
        elif size == 3:
            self.setup_fcn(self.pin[0],self.pin[1],self.pin[2])
        else:
            self.setup_fcn(self.pin[0],self.pin[1],self.pin[2],self.pin[3])

class Actuator:
    def __init__(self, actuator_id:str, pin:int, literal:str, action_fcn, setup_fcn):
        self.actuator_id = actuator_id
        self.pin = pin
        self.literal = literal
        self.action_fcn = action_fcn
        self.setup_fcn = setup_fcn

    def actuator_config(self):
        size = len(self.pin)
        if size == 1:
            self.setup_fcn(self.pin[0])
        elif size == 2:
            self.setup_fcn(self.pin[0],self.pin[1])
        elif size == 3:
            self.setup_fcn(self.pin[0],self.pin[1],self.pin[2])
        else:
            self.setup_fcn(self.pin[0],self.pin[1],self.pin[2],self.pin[3])

sens_array = [Sensor("",0,"","",None,None) for i in range(3)] #initialising array with empty sensor objects
sens_array[0] = Sensor("USR1",[17,18],"dist(X)","",fcn.getDist,setupUSR)
sens_array[1] = Sensor("BTN1",[2],"atHome","-atHome",fcn.btn_is_held,setupButton)
sens_array[2] = Sensor("BTN2",[24],"","",None,setupButton)

act_array = [Actuator("",0,"",None,None) for i in range(2)] #initialising array with empty sensor objects
act_array[0] = Actuator("LED1", [3], "blinkLED1slow", fcn.blinkLEDslow, setupLED)
act_array[1] = Actuator("LED2", [4], "onLED2", fcn.onLED, setupLED)