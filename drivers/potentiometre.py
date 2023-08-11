"""
    Driver for a potentiometre. Contains the setup function, calibration and getter.
"""

def calibrate(x, in_min = 0, in_max = 1023, out_min = 0, out_max = 5):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def getPotValue(data):
    return calibrate(data)

def printPotValue(data):
    print("Pot. Value (V): ", getPotValue(data))