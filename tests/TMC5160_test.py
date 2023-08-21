import TMC5160_registers as reg
import spidev
from time import sleep
import RPi.GPIO as GPIO

spi = spidev.SpiDev()
spi.open(1,2)  # Open SPI bus 1, device 2
spi.mode = 0 # could comment out
spi.max_speed_hz = 500000

GPIO.setmode(GPIO.BCM)
GPIO.setup([22,26,5], GPIO.OUT)
GPIO.output(22, 1)
GPIO.output(26, 0)
GPIO.output(5 , 0)

try:
    #Started example from Trinamic
    data = reg.data_builder("GCONF", [0x00, 0x00, 0x00, 0x0C], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("CHOPCONF", [0x00, 0x01, 0x00, 0xC3], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("IHOLD_IRUN", [0x00, 0x80, 0x0F, 0x0A], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("TPOWERDOWN", [0x00, 0x00, 0x00, 0x0A], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("TPWMTHRS", [0x00, 0x00, 0x01, 0xF4], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    #Values for speed and acceleration
    data = reg.data_builder("VSTART", [0x00, 0x00, 0x00, 0x01], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("A1", [0x00, 0x00, 0x13, 0x88], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("V1", [0x00, 0x00, 0x68, 0xDB], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("AMAX", [0x00, 0x00, 0x13, 0x88], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("VMAX", [0x00, 0x01, 0x86, 0xA0], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("DMAX", [0x00, 0x00, 0x13, 0x88], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("D1", [0x00, 0x00, 0x13, 0x88], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("VSTOP", [0x00, 0x00, 0x00, 0x0A], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    data = reg.data_builder("RAMPMODE", [0x00, 0x00, 0x00, 0x00], "W")
    print(data, end='---')
    response = spi.xfer2(data)
    print(response)

    while True:
        data = reg.data_builder("XACTUAL", [0x00, 0x00, 0x00, 0x00], "R")
        response = spi.xfer2(data)
        print("Reply: ", response)

        # data = reg.data_builder("XTARGET", [0x00, 0x07, 0xD0, 0x00], "W")
        # response = spi.xfer2(data)
        # print("Writing...")

        sleep(1)

        data = reg.data_builder("XACTUAL", [0x00, 0x00, 0x00, 0x00], "R")
        response = spi.xfer2(data)
        print("Reply: ", response)


        # data = reg.data_builder("XTARGET", [0x00, 0x00, 0x00, 0x00], "W")
        # response = spi.xfer2(data)
        # print("Writing...")

        sleep(1)
        

finally:
    spi.close()
    GPIO.output(22, 0) #to reset motor registers
    GPIO.cleanup()
    print("Exited gracefully")