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

data = reg.data_builder("GCONF", [0x00, 0x00, 0x00, 0x0C], "W")
response = spi.xfer2(data)

data = reg.data_builder("CHOPCONF", [0x00, 0x01, 0x00, 0xC3], "W")
response = spi.xfer2(data)

data = reg.data_builder("IHOLD_IRUN", [0x00, 0x80, 0x0F, 0x0A], "W")
response = spi.xfer2(data)

data = reg.data_builder("TPOWERDOWN", [0x00, 0x00, 0x00, 0x0A], "W")
response = spi.xfer2(data)

data = reg.data_builder("TPWMTHRS", [0x00, 0x00, 0x01, 0xF4], "W")
response = spi.xfer2(data)

#Values for speed and acceleration, values set should obey rules set by datasheet but only VMAX matters for the movement in this case
data = reg.data_builder("VSTART", [0x00, 0x00, 0x00, 0x01], "W")
response = spi.xfer2(data)

data = reg.data_builder("A1", [0x00, 0x00, 0x13, 0x88], "W")
response = spi.xfer2(data)

data = reg.data_builder("V1", [0x00, 0x00, 0x68, 0xDB], "W")
response = spi.xfer2(data)

data = reg.data_builder("AMAX", [0x00, 0x00, 0x13, 0x88], "W")
response = spi.xfer2(data)

data = reg.data_builder("DMAX", [0x00, 0x00, 0x13, 0x88], "W")
response = spi.xfer2(data)

data = reg.data_builder("D1", [0x00, 0x00, 0x13, 0x88], "W")
response = spi.xfer2(data)

data = reg.data_builder("VSTOP", [0x00, 0x00, 0x00, 0x0A], "W")
response = spi.xfer2(data)

data = reg.data_builder("RAMPMODE", [0x00, 0x00, 0x00, 0x02], "W") #set it to 2 to have constant velocity with no target
response = spi.xfer2(data)
  
def spin1():
    data = reg.data_builder("VMAX", [0x00, 0x05, 0x86, 0xA0], "W")
    response = spi.xfer2(data)

def spin2():
    data = reg.data_builder("VMAX", [0x00, 0x0B, 0xFF, 0xEE], "W")
    response = spi.xfer2(data)

def stop_and_reset():
    data = reg.data_builder("VMAX", [0x00, 0x00, 0x00, 0x00], "W")
    response = spi.xfer2(data)
    spi.close()
    GPIO.output(22, 0) #to reset motor registers
    GPIO.cleanup()
    print("Exited gracefully")


spin1()
sleep(5)
spin2()
sleep(5)
stop_and_reset()