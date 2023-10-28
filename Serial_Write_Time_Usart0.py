from machine import UART, Pin
import time
from os import urandom, statvfs

rtc=machine.RTC()
led = Pin(25, Pin.OUT)   # create LED object from Pin 25, Set Pin 15 to output

myUsart0 = UART(0, baudrate=1200, bits=8, tx=Pin(0), rx=Pin(1), timeout=20)
# Other side
# myUsart1 = UART(1, baudrate=9600, bits=8, tx=Pin(8), rx=Pin(9), timeout=15)
print("Starting Serial_Write_Time_Usart0.py")
iLed=0

try:
    while True:
        print("Set time")
        timestamp=rtc.datetime()
        settimestring="time,%04d-%02d-%02d %1d %02d:%02d:%02d"%(timestamp[0:7])
        myUsart0.write(settimestring)
        iLed=(iLed+1)%2
        led.value(iLed)
        time.sleep(5) #  nbmmmm1)

            
except KeyboardInterrupt:
    print("Keyboard")
    pass # machine.soft_reset()
