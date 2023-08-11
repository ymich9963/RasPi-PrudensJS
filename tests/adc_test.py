"""
    Small script to test an ADC with an SPI connection.
"""

import spidev

# Enable SPI
spi = spidev.SpiDev(0, 0)
spi.max_speed_hz = 250000
#spi.writebytes()

def adc_read(channel):

    #msg = [0b11000000]

    msg = [0b1, (0b1000 + channel) << 4, 0]
    r = spi.xfer2(msg)

    #r = spi.xfer2([1, (8 + channel) << 4, 0])
    #adc_out = ((r[1]&3) << 8) + r[2]

    

    return r

while True:

    adc = adc_read(0)

    print("Result:", adc)