"""
    Driver for the DFR0025 Ambient Light Sensor. Contains the setup function, calibraton, and getter.
"""

def calibrate(x):
    return x * (3.3/1023) * 100 #Vref = 3V3, Bit resolution = 10

def getLightInt(data):
    return calibrate(data)

def printLightInt(data):
    print("Light Int. (Lux): ", getLightInt(data))