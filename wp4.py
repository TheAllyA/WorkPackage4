import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import RPi.GPIO as GPIO
import threading

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

print("Raw ADC Value: ", chan.value)
print("ADC Voltage: " + str(chan.voltage) + "V")

Temp = AnalogIn(mcp, MCP.P1) # analogue input channel for temperature channel 1
LDR = AnalogIn(mcp, MCP.P2) # analogue input channel for LDR pin 3 channel 2
BTN=17 # GPIO pin
index = 0 # incrementer
sample = [10, 5, 1] # different sample rates
rate = sample[index] # sample rate chosen

V0 = 0.5
TC = 0.01


def setup():
        # Set up the GPIO button
        GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BTN, GPIO.FALLING, callback=changeIndex, bouncetime=200)
        pass

def changeIndex(ind):
        # Incremenets the variable called index every time the button on the circuit is pressed,
        #the index determines the sample rate between 10s, 5s or 1s, in that order
        global index
        if (index == 2):
                index = 0
        else:
                index += 1
        pass

def sensor():
        # Implement threading in order to output the Temperature value and LDR value
        global timer
        rate = sample[index]
        threader = threading.Timer(rate,sensor)
        threader.daemon = True
        threader.start()
        timer = time.time() - clock
        T = (Temp.voltage-V0)/TC
        print(str(int(round(timer,0)))+ 's\t\t' + str(Temp.value) + '\t\t\t' + str(round(T,2)) + ' C\t\t' + str(LDR.value))
        pass


if __name__ == "__main__":
        setup()
        clock = time.time()
        sensor()
        while True:
                pass
        GPIO.cleanup()
