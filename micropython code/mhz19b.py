import time
from machine import UART

class MHZ19BSensor:

    # constructor
    def __init__(self, rx_sensor, tx_sensor):
        self.uart = UART(2, baudrate=9600, rx=tx_sensor, tx=rx_sensor, bits=8, parity=None, stop=1, timeout = 1000, timeout_char = 1000)
        self.data = bytearray(9)
        self.request_data = b'\xff\x01\x86\x00\x00\x00\x00\x00\x79'
        self.measure() # dummy reading since the first reading usually fails
        
    # measure CO2
    def measure(self):
        # send a read command to the sensor
        self.uart.write(self.request_data)

        # read and validate the data
        self.uart.readinto(self.data,9)
        if self.is_valid():
            co2 = (self.data[2] << 8) + self.data[3]
            return co2
        else:
            self.reset()
            return None
        
    # check data returned by the sensor
    def is_valid(self):
        if self.data[0] != 0xFF or self.data[1] != 0x86:
            return False
        i = 1
        checksum = 0x00
        while i < 8:
            checksum += self.data[i] % 256
            i += 1
        checksum = ~checksum & 0xFF
        checksum += 1
        return checksum == self.data[8]
    
    def reset(self):
        self.uart.read(self.uart.any())


# used for debugging
if __name__ == "__main__":
    sensor = MHZ19BSensor()
    print(sensor.measure())
