from machine import UART, Pin
import time
from os import urandom, statvfs
import re

rtc=machine.RTC()
led = Pin(25, Pin.OUT)   # create LED object from Pin 25, Set Pin 15 to output

myUsart0 = UART(0, baudrate=1200, bits=8, tx=Pin(0), rx=Pin(1), timeout=20)
# Other side
# myUsart1 = UART(1, baudrate=9600, bits=8, tx=Pin(8), rx=Pin(9), timeout=15)
print("Starting FishSerialCmdAndRead.py  You may have to 'STOP' & Run a couple times.  Don't forget to officaly stop the program with a Cntl-C.")
i = 0
lineData=""
stringData=""
iLed=0

timestamp=rtc.datetime()
if timestamp[0] == 2021:
    foh = urandom(4)
    fohlist=list(bytes(foh, 'ascii'))
    fohstrlist=[str(ii) for ii in fohlist]
    fohstr=''.join(fohstrlist)
    # correct year next year
    timestringfilename = "FromFish2023" + fohstr + ".csv"
else:
    timestringfilename="FromFish%04d%02d%02d_%02d%02d%02d.csv"%(timestamp[0:3] + timestamp[4:7])

#File storage data
files_items = statvfs("/")

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

    print("Before try i =", i,"time or header cmd exist =", idx, idh)

print("Set time")
timestamp=rtc.datetime()
settimestring="time,%04d-%02d-%02d %1d %02d:%02d:%02d"%(timestamp[0:7])
myUsart0.write(settimestring)
time.sleep(5)
getLine()
time.sleep(3)
print("Sending header request (10 second pause)")
myUsart0.write("header")
time.sleep(5)
getLine()
time.sleep(5)

try:
    while True:
        rxData = bytes()
        time.sleep(0.1)
        while myUsart0.any() > 0:
            rxData += myUsart0.read(1)
        
        stringData = rxData.decode('utf-8')
        if (not stringData):
            i = i + 1
        else:
            # print(i,stringData)
            if i>0:
                # Print data & write data to files. 
                if (len(lineData)>0):
                    print(lineData)
                    file = open(timestringfilename, "a")
                    file.write(lineData+"\n")
                    file.close()
                lineData=stringData
                i = 0
                # Turn led on/off
                iLed=(iLed+1)%2
                led.value(iLed)
            else:
                lineData=lineData+stringData
            
except KeyboardInterrupt:
    print("Keyboard")
    pass # machine.soft_reset()

  