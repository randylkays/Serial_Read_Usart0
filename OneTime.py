# Send Time CMD Once
from machine import UART, Pin
import time
from os import urandom, statvfs

rtc=machine.RTC()
led = Pin(25, Pin.OUT)   # create LED object from Pin 25, Set Pin 15 to output

myUsart0 = UART(0, baudrate=1200, bits=8, tx=Pin(0), rx=Pin(1), timeout=20)
# Other side
# myUsart1 = UART(1, baudrate=9600, bits=8, tx=Pin(8), rx=Pin(9), timeout=15)
print("Starting OneTime.py to send time command once. ")
iLed=1
led.value(iLed)

def getLine():
    i=0
    idx=None
    idh=None
    stringData=""
    while stringData=="":
        rxData = bytes()
        time.sleep(0.1)
        while myUsart0.any() > 0:
            rxData += myUsart0.readline()

        stringData = rxData.decode('utf-8')
        if (not stringData):
            i = i + 1
            print("No data:",i)
        else:
            idx=re.search("time",stringData)
            idh=re.search("header",stringData)
            
            #if stringData contains "time" then idx will not be None
            #if stringData contains "header" then idh will not be None
            if idx==None and idh==None:
                print("Neither Time nor header were sent.  i=",i)
            elif idx!=None:
                print("time CMD sent i=",i)
            elif idh!=None:
                print("header CMD sent i=",i)
            else:
                print("WTF! Got both time & header?  i=",i)
            #print("i=",i,"Waiting for CMD response>" , stringData,"<")
            i = 0

try:
    timestamp=rtc.datetime()
    settimestring="time,%04d-%02d-%02d %1d %02d:%02d:%02d"%(timestamp[0:7])
    print("Set time CMD:",settimestring)
    myUsart0.write(settimestring)
    iLed=(iLed+1)%2
    led.value(iLed)
    time.sleep(5)
    getLine()
    print("Did it work?")

            
except KeyboardInterrupt:
    print("Keyboard")
    pass # machine.soft_reset()
