import cgitb ; cgitb.enable() 
import spidev 
import time
import busio
import digitalio
import board
from adafruit_bus_device.spi_device import SPIDevice
import requests 

url = "http://orientationproject.hub.ubeac.io/opg5"  #ubeac link om te uploaden
uid = "raspigroep5"                            #ubeac Unique IDs                            #ubeac Unique IDs
 
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

def stuurData(tempe, gewe):
    data = {                                            #Pak alle data in om te versturen
		"id": uid,
		"sensors":[{
			'id': 'adc kanaal0',
			'data': tempe
			}, {
            'id': 'adc kanaal1',
			'data': gewe
            }]}
    requests.post(url, verify=False,  json=data)        #Verstuur deze data door een http request

def mapper(in_v, in_min, in_max, out_min, out_max):           # (3)
    v = (in_v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if v < out_min: 
        v = out_min 
    elif v > out_max: 
        v = out_max
    return v

while True:
    temperatuur = round(mapper(lees("temp"), 0, 1024, 0, 40), 2)
    gewicht = round(mapper(lees("weight"), 0, 1024, 1, 5), 2)
    stuurData(temperatuur, gewicht)
    time.sleep(0.2)
    
