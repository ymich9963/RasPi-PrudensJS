def calibrate(x, in_min = 0, in_max = 1023, out_min = 0, out_max = 150):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def getTemp(data):
    return calibrate(data)

def printTemp(data):
    print("Temp (C): ", getTemp(data))