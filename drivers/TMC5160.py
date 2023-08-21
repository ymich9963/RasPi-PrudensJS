import spidev
from time import sleep
import RPi.GPIO as GPIO

reg_addr = {  "GCONF": {"addr": 0x00, "access": "RW"}, # normal mode + stealth chop (stealthChop voltage PWM mode enabled (depending on velocity thresholds). Switch on while in stand still, only.)
            "GSTAT": {"addr": 0x01, "access": "R"}, # Write reset at start up
            "IFCNT": {"addr": 0x02, "access": "R"},
            "NODECONF": {"addr": 0x03, "access": ""}, # not used in SPI mode
            "IOIN": {"addr": 0x04, "access": "R"},
            "X_COMPARE": {"addr": 0x05, "access": "RW"},
            "IHOLD_IRUN": {"addr": 0x10, "access": "W"}, # Current control with stealthChop mode
            "TPOWERDOWN": {"addr": 0x11, "access": "W"}, # (Reset default=20) Sets the delay time from stand still (stst) detection to motor current power down. Time range is about 0 to 5.6 seconds. 0...((2^8)-1) * 2^18 tclk Attention: A minimum setting of 2 is required to allow automatic tuning of stealthChop PWM_OFFS_AUTO.
            "TSTEP": {"addr": 0x12, "access": "R"},
            "TPWMTHRS": {"addr": 0x13, "access": "W"}, # unclear
            "TCOOLTHRS": {"addr": 0x14, "access": "W"}, #This is the lower threshold velocity for switching on smart energy coolStep and stallGuard feature.
            "THIGH": {"addr": 0x15, "access": "W"},
            "RAMPMODE": {"addr": 0x20, "access": "W"}, # 0: Positioning mode (using all A, D and V parameters) 1: Velocity mode to positive VMAX (using AMAX acceleration)
            "XACTUAL": {"addr": 0x21, "access": "RW"}, # Actual motor position (signed) Hint: This value normally should only be modified, when homing the drive. In positioning mode, modifying the register content will start a motion.
            "VACTUAL": {"addr": 0x22, "access": "RW"}, # Actual motor velocity from ramp generator (signed) The sign matches the motion direction. A negative sign means motion to lower XACTUAL.
            "VSTART": {"addr": 0x23, "access": "W"}, # Motor start velocity (unsigned) Set VSTOP = VSTART!
            "A1": {"addr": 0x24, "access": "W"}, # First acceleration between VSTART and V1 (unsigned)
            "V1": {"addr": 0x25, "access": "W"}, # First acceleration / deceleration phase threshold velocity (unsigned) 0: Disables A1 and D1 phase, use AMAX, DMAX only
            "AMAX": {"addr": 0x26, "access": "W"}, # Second acceleration between V1 and VMAX (unsigned) This is the acceleration and deceleration value for velocity mode.
            "VMAX": {"addr": 0x27, "access": "W"}, # Motion ramp target velocity (for positioning ensure VMAX = VSTART) (unsigned) This is the target velocity in velocity mode. It can be changed any time during a motion.
            "DMAX": {"addr": 0x28, "access": "W"}, # Deceleration between VMAX and V1 (unsigned)
            "D1": {"addr": 0x2A, "access": "W"}, # Deceleration between V1 and VSTOP (unsigned) Attention: Do not set 0 in positioning mode, even if V1=0!
            "VSTOP": {"addr": 0x2B, "access": "W"}, # Motor stop velocity (unsigned) Attention: Set VSTOP = VSTART! Attention: Do not set 0 in positioning mode, minimum 10 recommend!
            "TZEROWAIT": {"addr": 0x2C, "access": "W"}, # Defines the waiting time after ramping down to zero velocity before next movement or direction inversion can start. Time range is about 0 to 2 seconds. 
            "XTARGET": {"addr": 0x2D, "access": "RW"}, # Target position for ramp mode (signed).
            "VDCMIN": {"addr": 0x33, "access": "W"}, # Automatic commutation dcStep becomes enabled above velocity VDCMIN (unsigned)
            "SWMODE": {"addr": 0x34, "access": "RW"}, # reference switch input
            "RAMPSTAT": {"addr": 0x35, "access": "R"}, # Reference switch
            "XLATCH": {"addr": 0x36, "access": "R"}, # programmable switch event
            "ENCMODE": {"addr": 0x38, "access": "RW"}, # channel event
            "XENC": {"addr": 0x39, "access": "RW"}, # Actual encoder position
            "ENC_CONST": {"addr": 0x3A, "access": "W"}, # encoder
            "ENC_STATUS": {"addr": 0x3B, "access": "R"}, # Encoder status
            "ENC_LATCH": {"addr": 0x3C, "access": "R"}, # Encoder position X_ENC latched on N event
            "MSLUT0":     {"addr": 0x60, "access":"W"}, # microstep table entry 0-31
            "MSLUT1":     {"addr": 0x61, "access":"W"},
            "MSLUT2":     {"addr": 0x62, "access":"W"},
            "MSLUT3":     {"addr": 0x63, "access":"W"},
            "MSLUT4":     {"addr": 0x64, "access":"W"},
            "MSLUT5":     {"addr": 0x65, "access":"W"},
            "MSLUT6":     {"addr": 0x66, "access":"W"},
            "MSLUT7":     {"addr": 0x67, "access":"W"},
            "MSLUTSEL":   {"addr": 0x68, "access":"W"}, # LUT width and segment start config
            "MSLUTSTART": {"addr": 0x69, "access":"W"}, # Absolute current for microstep table entry
            "MSCNT":      {"addr": 0x6A, "access":"R"}, # Microstep counter. Indicates actual position in the microstep table
            "MSCURACT":   {"addr": 0x6B, "access":"R"}, # Actual microstep current for motor phase
            "CHOPCONF":   {"addr": 0x6C, "access":"RW"}, # Chopper mode config
            "COOLCONF":   {"addr": 0x6D, "access":"W"}, # stallGuard config
            "DCCTRL":   {"addr": 0x6E, "access":"W"}, # PWM config
            "DRVSTATUS":   {"addr": 0x6F, "access":"R"}, # Driver status
            "PWMCONF":   {"addr": 0x70, "access":"W"}, # PMW config
            "PWMSCALE":   {"addr": 0x71, "access":"R"}, # Actual PWM amplitude scaler (255=max. Voltage) In voltage mode PWM, this value allows to detect a motor stall.
            "ENCM_CTRL":   {"addr": 0x72, "access":"W"}, 
            "LOST_STEPS":   {"addr": 0x73, "access":"R"}, 
}

def address_resolver(addr):
    return reg_addr[addr]["addr"]

def register_access(addr, rw):
    """"Checking register access right"""
    if rw not in reg_addr[addr]["access"]:
        print(f"Error {addr} Register can't be {rw}, system stop.")
        sys.exit(1)
    else:
        return 0

def data_builder(addr, value, rw):
    """Build data trame.
    Check for register access, configure MSB and concate into a list.
    input:  register name, list of values, read of write status
    output: hexadecimal trame list [register_addr, val1, val2, val3, val4]"""
    addr_value = address_resolver(addr)
    register_access(addr, rw)

    # IF write to buffer => set MSB to 1
    if rw == "W":
        addr_value += 0x80 # set MSB to 1
    value.insert(0, addr_value)

    return value

max_speed_hz = 500000
spi_mode = 0

spi_motor1 = spidev.SpiDev()
spi_motor1.open(1,2)  # Open SPI bus 1, device 2
spi_motor1.mode = spi_mode # could comment out
spi_motor1.max_speed_hz = max_speed_hz

spi_motor2 = spidev.SpiDev()
spi_motor2.open(1,1)  # Open SPI bus 1, device 1
spi_motor2.mode = spi_mode
spi_motor2.max_speed_hz = max_speed_hz

spi_motor3 = spidev.SpiDev()
spi_motor3.open(1,0)  # Open SPI bus 1, device 0
spi_motor3.mode = spi_mode
spi_motor3.max_speed_hz = max_speed_hz

GPIO.setmode(GPIO.BCM)
GPIO.setup([22,26,5], GPIO.OUT)
GPIO.output(22, 1) #Vcc_IO
GPIO.output(26, 0) #CLK
GPIO.output(5 , 0) #DRV_EN

#Started example from Trinamic
data = data_builder("GCONF", [0x00, 0x00, 0x00, 0x0C], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("CHOPCONF", [0x00, 0x01, 0x00, 0xC3], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("IHOLD_IRUN", [0x00, 0x80, 0x0F, 0x0A], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("TPOWERDOWN", [0x00, 0x00, 0x00, 0x0A], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("TPWMTHRS", [0x00, 0x00, 0x01, 0xF4], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

#Values for speed and acceleration
data = data_builder("VSTART", [0x00, 0x00, 0x00, 0x01], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("A1", [0x00, 0x00, 0x13, 0x88], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("V1", [0x00, 0x00, 0x68, 0xDB], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("AMAX", [0x00, 0x00, 0x13, 0x88], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("VMAX", [0x00, 0x01, 0x86, 0xA0], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("DMAX", [0x00, 0x00, 0x13, 0x88], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("D1", [0x00, 0x00, 0x13, 0x88], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("VSTOP", [0x00, 0x00, 0x00, 0x0A], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)

data = data_builder("RAMPMODE", [0x00, 0x00, 0x00, 0x00], "W")
#print(data, end='---')
response = spi_motor1.xfer2(data)
#print(response)        

def _action():
    try:
        data = data_builder("XACTUAL", [0x00, 0x00, 0x00, 0x00], "R")
        response = spi_motor1.xfer2(data)
        #print("Reply: ", response)

        data = data_builder("XTARGET", [0x00, 0x07, 0xD0, 0x00], "W")
        response = spi_motor1.xfer2(data)
        #print("Writing...")

        sleep(1)

        data = data_builder("XACTUAL", [0x00, 0x00, 0x00, 0x00], "R")
        response = spi_motor1.xfer2(data)
        #print("Reply: ", response)


        data = data_builder("XTARGET", [0x00, 0x00, 0x00, 0x00], "W")
        response = spi_motor1.xfer2(data)
        #print("Writing...")

        sleep(1)
    finally:
        #spi.close()
        GPIO.output(22, 0) #to reset motor registers
        GPIO.output(22, 1)
        #GPIO.cleanup()
        #print("Exited gracefully")

def stop():
    #spi.close()
    GPIO.output(22, 0) #to reset motor registers
    GPIO.output(22, 1)
    #GPIO.cleanup()
    #print("Exited gracefully")