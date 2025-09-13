# Starting Serial_Read_Usart0.py
# By Randy Kays 
from machine import UART, Pin
import time
from os import urandom, statvfs

rtc=machine.RTC()
led = Pin(25, Pin.OUT)   # create LED object from Pin 25, Set Pin 15 to output

myUsart0 = UART(0, baudrate=1200, bits=8, tx=Pin(0), rx=Pin(1), timeout=20)
# Other side
# myUsart1 = UART(1, baudrate=9600, bits=8, tx=Pin(8), rx=Pin(9), timeout=15)
print("Starting Serial_Read_Usart0.py")
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
    timestringfilename = "Fish2025_" + fohstr + ".csv"
else:
    timestringfilename="Fish%04d%02d%02d_%02d%02d%02d.csv"%(timestamp[0:3] + timestamp[4:7])

#Create file
files_items = statvfs("/")
# file = open(timestringfilename, "w")
# file.write("Time,Thermister,Voltage,ThrCnt,Internal Temp degF,IT_Cnt,Tmp IC degF,PhotoR,PhtCnt,Press,PRcnt,Battery,BtCNt,MemAvailable\n")
# file.close()

def getLine():
    i=0
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
            if stringData=="CMD:":
                print("No command.")
            print("i=",i,"Waiting for CMD response>" , stringData,"<")
            i = 0

    print("Before try:", i, stringData)

print("Set time")
timestamp=rtc.datetime()
settimestring="time,%04d-%02d-%02d %1d %02d:%02d:%02d"%(timestamp[0:7])
myUsart0.write(settimestring)
time.sleep(5) #  nbmmmm1)
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
                if (len(lineData)>0):
                    print(lineData)
                    file = open(timestringfilename, "a")
                    file.write(lineData+"\n")
                    file.close()
                lineData=stringData
                i = 0
                iLed=(iLed+1)%2
                led.value(iLed)
            else:
                lineData=lineData+stringData
            
except KeyboardInterrupt:
    print("Keyboard")
    pass # machine.soft_reset()

  