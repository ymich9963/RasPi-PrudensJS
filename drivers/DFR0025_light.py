def calibrate(x, in_min = 0, in_max = 1023, out_min = 1, out_max = 6000):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def getLightInt(data):
    return calibrate(data)

def printLightInt(data):
    print("Light Int. (Lux): ", getLightInt(data))