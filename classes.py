class Sensor:
    data = 0
    is_literal_numeric = False
    default_literal_p = ""
    default_literal_n = ""
    def __init__(self, sensor_id:str, pin:int, literal_p:str, literal_n:str, action_fcn, setup_fcn):
        self.sensor_id = sensor_id
        self.pin = pin
        self.literal_p = literal_p
        self.literal_n = literal_n
        self.action_fcn = action_fcn
        self.setup_fcn = setup_fcn
        self.default_literal_p = literal_p
        self.default_literal_n = literal_n

    def sensor_setup(self):
        size = len(self.pin)
        if size == 1:
            self.setup_fcn(self.pin[0])
        elif size == 2:
            self.setup_fcn(self.pin[0],self.pin[1])
        elif size == 3:
            self.setup_fcn(self.pin[0],self.pin[1],self.pin[2])
        else:
            self.setup_fcn(self.pin[0],self.pin[1],self.pin[2],self.pin[3])    
            
    def sensor_action(self):
        size = len(self.pin)
        self.prev_data = self.data
        if size == 1:
            self.data = self.action_fcn(self.pin[0])
        elif size == 2:
            self.data = self.action_fcn(self.pin[0],self.pin[1])
        elif size == 3:
            self.data = self.action_fcn(self.pin[0],self.pin[1],self.pin[2])
        else:
            self.data = self.action_fcn(self.pin[0],self.pin[1],self.pin[2],self.pin[3])

    def data_in_literal(self):
        if "X" in self.literal_p:
            self.literal_p = self.literal_p.replace("X", str(int(self.data)))
            self.is_literal_numeric = True
        elif "X" in self.literal_n:
            self.literal_n = self.literal_n.replace("X",str(int(self.data)))
            self.is_literal_numeric = True
        elif any((num in set('0123456789')) for num in self.literal_p):
            if self.literal_p != "":
                self.literal_p = self.default_literal_p
                self.literal_p = self.literal_p.replace("X", str(int(self.data)))
                self.is_literal_numeric = True
            elif self.literal_n != "":
                self.literal_n = self.default_literal_n
                self.literal_n = self.literal_n.replace("X", str(int(self.data)))
                self.is_literal_numeric = True
        else:
            #print("No 'X' character found, could be a boolean literal")
            self.is_literal_numeric = False
            

class Actuator:
    def __init__(self, actuator_id:str, pin:int, literal:str, action_fcn, setup_fcn):
        self.actuator_id = actuator_id
        self.pin = pin
        self.literal = literal
        self.action_fcn = action_fcn
        self.setup_fcn = setup_fcn

    def actuator_setup(self):
        size = len(self.pin)
        if size == 1:
            self.setup_fcn(self.pin[0])
        elif size == 2:
            self.setup_fcn(self.pin[0],self.pin[1])
        elif size == 3:
            self.setup_fcn(self.pin[0],self.pin[1],self.pin[2])
        else:
            self.setup_fcn(self.pin[0],self.pin[1],self.pin[2],self.pin[3])

