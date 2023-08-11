import sys
import spidev

class motor():
    def __init__(self, spi_bus, chip_select):
        self.spi_bus = spi_bus
        self.spi_chip_select = chip_select
        self.spi_max_speed = 500000
        self.spi_mode = 0

        self.spi = spidev.SpiDev()
        # Open a connection to a specific bus and device (chip select pin)
        self.spi.open(self.spi_bus, self.spi_chip_select)
        # Set SPI speed and mode
        self.spi.max_speed_hz = self.spi_max_speed
        self.spi.mode = self.spi_mode

        self.register_addr = {  "GCONF": {"addr": 0x00, "access": "RW"}, # normal mode + stealth chop (stealthChop voltage PWM mode enabled (depending on velocity thresholds). Switch on while in stand still, only.)
                                "GSTAT": {"addr": 0x01, "access": "R"}, # Write reset at start up
                                "IFCNT": {"addr": 0x02, "access": "R"},
                                "SLAVECONF": {"addr": 0x03, "access": ""}, # not used in SPI mode
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

    def connect(self):
        spi = spidev.SpiDev()
        # Open a connection to a specific bus and device (chip select pin)
        spi.open(self.spi_bus, self.spi_chip_select)

        # Set SPI speed and mode
        spi.max_speed_hz = self.spi_max_speed
        spi.mode = self.spi_mode

        return spi

    def address_resolver(self, addr):
        return self.register_addr[addr]["addr"]

    def register_access(self, addr, rw):
        """"Checking register access right"""
        if rw not in self.register_addr[addr]["access"]:
            print(f"Error {addr} Register can't be {rw}, system stop.")
            sys.exit(1)
        else:
            return 0

    def data_builder(self, addr, value, rw):
        """Build data trame.
        Check for register access, configure MSB and concate into a list.
        input:  register name, list of values, read of write status
        output: hexadecimal trame list [register_addr, val1, val2, val3, val4]"""
        addr_value = self.address_resolver(addr)
        self.register_access(addr, rw)

        # IF write to buffer => set MSB to 1
        if rw == "W":
            addr_value += 0x80 # set MSB to 1
        value.insert(0, addr_value)

        return value


    def send_data(self, data):
        "send data trame to driver using SPI"
        response = self.spi.xfer(data)
        return response


if __name__ == "__main__":

    motor_1 = motor(spi_bus=1, chip_select=0)

    # print("GSTAT R") 
    # data = [0x01, 0x00, 0x00, 0x00, 0x00] 0x01
    data = motor_1.data_builder("GSTAT", [0x00, 0x00, 0x00, 0x00], "R")
    response = motor_1.send_data(data)

    # Initialize position
    data = motor_1.data_builder("XTARGET", [0x00, 0x00, 0x00, 0x00], "W")
    response = motor_1.send_data(data)
    data = motor_1.data_builder("XACTUAL", [0x00, 0x00, 0x00, 0x00], "W")
    response = motor_1.send_data(data)

    # Write chopper configs 0x6C
    # data = [0xEC, 0x00, 0x01, 0x00, 0xC5]
    # print("CHOPCONF W") # EC
    data = motor_1.data_builder("CHOPCONF", [0x00, 0x01, 0x00, 0xC5], "W")
    response = motor_1.send_data(data)

    # Write IRUN=10 IHOLD=2 0x10
    # data = [0x90, 0x00, 0x06, 0x0A, 0x02]
    data = motor_1.data_builder("IHOLD_IRUN", [0x00, 0x06, 0x0A, 0x02], "W")
    response = motor_1.send_data(data)

    # Write - Set RAMPMODE to 1 (Velocity mode) 0x20
    # data = [0xA0, 0x00, 0x00, 0x00, 0x01]
    data = motor_1.data_builder("RAMPMODE", [0x00, 0x00, 0x00, 0x01], "W")
    response = motor_1.send_data(data)

    # A1 = 1, first acceleration 0x24
    # data = [0xA4, 0x00, 0x00, 0x03, 0xE8]
    data = motor_1.data_builder("A1", [0x00, 0x00, 0x03, 0xE8], "W")
    response = motor_1.send_data(data)

    # V1 = 50000 Acceleration threshold velocity 0x25
    # data = [0xA5, 0x00, 0x00, 0xC3, 0x50]
    data = motor_1.data_builder("V1", [0x00, 0x00, 0xC3, 0x50], "W")
    response = motor_1.send_data(data)

    # AMAX = 500 acceleration above V1 0x26
    # data = [0xA6, 0x00, 0x00, 0x01, 0xF4]
    data = motor_1.data_builder("AMAX", [0x00, 0x00, 0x01, 0xF4], "W")
    response = motor_1.send_data(data)

    # VMAX = 200000 0x27
    data = [0xA7, 0x00, 0x03, 0x0D, 0x40]
    data = motor_1.data_builder("VMAX", [0x00, 0x03, 0x0D, 0x40], "W")
    response = motor_1.send_data(data)

    # DMAX = 700 deceleration above V1 0x28
    # data = [0xA8, 0x00, 0x00, 0x02, 0xBC]
    data = motor_1.data_builder("DMAX", [0x00, 0x00, 0x02, 0xBC], "W")
    response = motor_1.send_data(data)

    # D1 = 1400 deceleration below V1 0x2A
    # data = [0xAA, 0x00, 0x00, 0x05, 0x78]
    data = motor_1.data_builder("D1", [0x00, 0x00, 0x05, 0x78], "W")
    response = motor_1.send_data(data)

    # VSTOP = 10 stop velocity (near to 0) 0x2B
    # data = [0xAB, 0x00, 0x00, 0x00, 0x0A]
    data = motor_1.data_builder("VSTOP", [0x00, 0x00, 0x00, 0x0A], "W")
    response = motor_1.send_data(data)

    # RAMPMODE = 0 (Target position move) 0x20
    # data = [0xA0, 0x00, 0x00, 0x00, 0x00]
    data = motor_1.data_builder("RAMPMODE", [0x00, 0x00, 0x00, 0x00], "W")
    response = motor_1.send_data(data)

    # TEST Move
    import time

    data = motor_1.data_builder("XACTUAL", [0x00, 0x00, 0x00, 0x00], "R")
    response = motor_1.send_data(data)
    print(f"XACTUAL:{response}")

    data = motor_1.data_builder("XTARGET", [0x00, 0x00, 0xAA, 0x00], "W")
    response = motor_1.send_data(data)
    print(f"Move to AA")

    time.sleep(2)
    data = motor_1.data_builder("XACTUAL", [0x00, 0x00, 0x00, 0x00], "R")
    response = motor_1.send_data(data)
    print(f"XACTUAL:{response}")

    data = motor_1.data_builder("XTARGET", [0x00, 0x00, 0x00, 0x00], "W")
    response = motor_1.send_data(data)
    print(f"Move to 00")

    time.sleep(2) # If small timing:0.1 => read XACTUAL during motor movement => stop the motor
    data = motor_1.data_builder("XACTUAL", [0x00, 0x00, 0x00, 0x00], "R")
    response = motor_1.send_data(data)
    print(f"XACTUAL:{response}")