"""
    Driver for the DFR0023 Temperature Sensor. Contains the setup function, calibraton, and getter.
"""

def calibrate(x): #3.3/10244
    return x * (3.3/1023) * 100 #Vref = 3V3, Bit resolution = 10

def getTemp(data):
    return calibrate(data)

def printTemp(data):
    print("Temp (C): ", getTemp(data))