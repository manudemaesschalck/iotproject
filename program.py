import cgitb ; cgitb.enable() 
import spidev 
import time
import busio
import digitalio
import board
from adafruit_bus_device.spi_device import SPIDevice
 
# Start SPI op
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Start analogDigitalConvertor op
cs0 = digitalio.DigitalInOut(board.CE0)
adc = SPIDevice(spi, cs0, baudrate= 1000000)
 
def lees(sensor): 
    if sensor == 'temp':
        with adc:
            r = bytearray(3)
            spi.write_readinto([1,(8)<<4,0], r)
            time.sleep(0.000005)
            adcout = ((r[1]&3) << 8) + r[2] 
            return adcout 
    elif sensor == 'weight':
        with adc:
            r = bytearray(3)
            spi.write_readinto([1,(9)<<4,0], r)
            time.sleep(0.000005)
            adcout = ((r[1]&3) << 8) + r[2]
            return adcout 
    else: 
        return -1

while True:
	temperatuur = lees("temp")
	gewicht = lees("weight")

	time.sleep(0.2)
