"""
This Python file contains the two classes used in the system, Sensors and Actuators. Due to the 
common functions they have they can have a parent class in future implementations. The action and setup functions
require the driver file to be in the /drivers location. Currently all drivers
are coded specifically for the system and no libraries are used.
"""

class Sensor:
    """
    Sensor object contains all of the relative sensor data.
    
    Args:
        data: Data retrieved by sensor

        is_literal_numeric: Set when the literal of the sensor has a X for numbers, e.g. dist(X)

        default_literal_p: Default literal to for easier replacement of X

        default_literal_n: Same as above

        sensor_id (str, optional): ID for each sensor, duplicates are currently allowed. Defaults to "".

        pin_or_channel (int or list, optional): Can be an array or an int but that depends if adc_fcn is not set to None. Defaults to [0].

        literal_p (str, optional): The positive literal used by the sensor for the Context. Defaults to "".

        literal_n (str, optional): The negative literal used by the sensor for the Context. Defaults to "".

        action_fcn (function, optional): The action done by the sensor, e.g. get distance or check for a button press. Defaults to None.

        setup_fcn (function, optional): Used to set up the correct pins in the correct way to accept the sensor data. Defaults to None.

        adc_fcn (function, optional): Must be set if using an ADC channel for measurements. Defaults to None.

    """
    data = 0
    is_literal_numeric = False
    default_literal_p = ""
    default_literal_n = ""
    def __init__(self, sensor_id = "", pin_or_channel = [0], literal_p = "", literal_n = "", action_fcn = None, setup_fcn = None, adc_fcn = None):
        
        self.sensor_id = sensor_id
        self.pin_or_channel = pin_or_channel
        self.literal_p = literal_p
        self.literal_n = literal_n
        self.action_fcn = action_fcn
        self.setup_fcn = setup_fcn
        self.default_literal_p = literal_p
        self.default_literal_n = literal_n
        self.adc_fcn = adc_fcn

#   use the setup function to assign the sensor to the correct pins, max 4 pins can be used
    def sensor_setup(self):
        if self.setup_fcn == None:
            return
        else:
            size = len(self.pin_or_channel)
            if size == 1:
                self.setup_fcn(self.pin_or_channel[0])
            elif size == 2:
                self.setup_fcn(self.pin_or_channel[0],self.pin_or_channel[1])
            elif size == 3:
                self.setup_fcn(self.pin_or_channel[0],self.pin_or_channel[1],self.pin_or_channel[2])
            elif size == 4:
                self.setup_fcn(self.pin_or_channel[0],self.pin_or_channel[1],self.pin_or_channel[2],self.pin_or_channel[3])
            else:
                print("Error notify dev, allowed pins exceeded for " + self.sensor_id)  

#   function used to retrieve data from sensor        
    def sensor_action(self): 
        if self.adc_fcn != None:
            self.data = self.adc_fcn(self.pin_or_channel)
            self.data = self.action_fcn(self.data)
            return

#       if any mistake happens in initialisation and there is an empty entry, ignore it
        elif self.action_fcn == None: 
            return
        else:    
            size = len(self.pin_or_channel)
            if size == 1:
                self.data = self.action_fcn(self.pin_or_channel[0])
            elif size == 2:
                self.data = self.action_fcn(self.pin_or_channel[0],self.pin_or_channel[1])
            elif size == 3:
                self.data = self.action_fcn(self.pin_or_channel[0],self.pin_or_channel[1],self.pin_or_channel[2])
            else:
                self.data = self.action_fcn(self.pin_or_channel[0],self.pin_or_channel[1],self.pin_or_channel[2],self.pin_or_channel[3])

#   fcn used to replace the X in a numerical input to the context
    def data_in_literal(self): 
        if "X" in self.literal_p:
            self.literal_p = self.literal_p.replace("X", str(int(self.data)))
            self.is_literal_numeric = True
        elif "X" in self.literal_n:
            self.literal_n = self.literal_n.replace("X",str(int(self.data)))
            self.is_literal_numeric = True
        elif self.is_literal_numeric and any((num in set('0123456789')) for num in self.literal_p):
            if self.literal_p != "":
                self.literal_p = self.default_literal_p
                self.literal_p = self.literal_p.replace("X", str(int(self.data)))
            elif self.literal_n != "":
                self.literal_n = self.default_literal_n
                self.literal_n = self.literal_n.replace("X", str(int(self.data)))
        else:
            self.is_literal_numeric = False
            

class Actuator:
    def __init__(self, actuator_id = "", pin = [0], literal = "", action_fcn = None, setup_fcn = None):
        """Actuator object contains all of the actuator data.

        Args:
            actuator_id (str, optional): ID for each actuator, duplicates are currently allowed. Defaults to "".

            pin (list, optional): Pin used by the actuator. Defaults to [0].

            literal (str, optional): Literal to detect in order to use it. Defaults to "".

            action_fcn (function, optional): The action done by the actuator, e.g. turn LED on. Defaults to None.

            setup_fcn (function, optional): Used to set up the correct pins in the correct way to accept the sensor data. Defaults to None.

        """
        self.actuator_id = actuator_id
        self.pin = pin
        self.literal = literal
        self.action_fcn = action_fcn
        self.setup_fcn = setup_fcn

#   use the setup function to assign the actuator to the correct pins, max 4 pins can be used
    def actuator_setup(self):
        if self.setup_fcn == None:
            return
        else:
            size = len(self.pin)
            if size == 1:
                self.setup_fcn(self.pin[0])
            elif size == 2:
                self.setup_fcn(self.pin[0],self.pin[1])
            elif size == 3:
                self.setup_fcn(self.pin[0],self.pin[1],self.pin[2])
            elif size == 4:
                self.setup_fcn(self.pin[0],self.pin[1],self.pin[2],self.pin[3])
            else:
                print("Error notify dev, allowed setup pins exceeded for " + self.actuator_id)

#   function used to retrieve data from actuator
    def actuator_action(self): 
        if self.pin == None:
            self.action_fcn()
        else:
            size = len(self.pin)
            if size == 1:
                self.data = self.action_fcn(self.pin[0])
            elif size == 2:
                self.data = self.action_fcn(self.pin[0],self.pin[1])
            elif size == 3:
                self.data = self.action_fcn(self.pin[0],self.pin[1],self.pin[2])
            elif size == 4:
                self.data = self.action_fcn(self.pin[0],self.pin[1],self.pin[2],self.pin[3])
            else:
                print("Error notify dev, allowed action pins exceeded for " + self.actuator_id)