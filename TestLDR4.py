# -*- coding: utf-8 -*-
import threading
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0 
i = 0 
#define function as thread for light reading
def print_light_thread():
    l = AnalogIn(mcp, MCP.P0)
    t = threading.Timer(10.0, print_light_thread())
    t.start()
    print('Raw ADC Value:', l.value)
        #print('ADC Voltage: ' + str(l.voltage) + 'V')
    i=i+1

def print_sensor_thread():
    s = AnalogIn(mcp, MCP.P0)
    a = threading.Timer(10.0, print_sensor_thread())
    a.start()
    print('Raw ADC Value:', s.value)
        #print('ADC Voltage: ' + str(s.voltage) + 'V') 
    i=i+1
while i<7:
    print_light_thread()
    print_sensor_thread()
