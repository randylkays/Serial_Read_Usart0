from machine import UART, Pin
import time
from os import urandom, statvfs
import re
from sys import exit

rtc=machine.RTC()
led = Pin(25, Pin.OUT)   # create LED object from Pin 25, Set Pin 15 to output

myUsart0 = UART(0, baudrate=1200, bits=8, tx=Pin(0), rx=Pin(1), timeout=20)
# Other side
# myUsart1 = UART(1, baudrate=9600, bits=8, tx=Pin(8), rx=Pin(9), timeout=15)
print("Starting FishFilesCMDs.py  Use Cntl-C to Stop Program")
i = 0
lineData=""
stringData=""
iLed=0
sCmdFiles="listfiles"
sCmdPrint="printfile,"
sCmdRemove="remove,"

timestamp=rtc.datetime()
if timestamp[0] == 2021:
    foh = urandom(4)
    fohlist=list(bytes(foh, 'ascii'))
    fohstrlist=[str(ii) for ii in fohlist]
    fohstr=''.join(fohstrlist)
    # correct year next year
    timestringfilename = "FileDumpFish2023" + fohstr + ".csv"
else:
    timestringfilename="FilesDump%04d%02d%02d_%02d%02d%02d.csv"%(timestamp[0:3] + timestamp[4:7])

#File storage data
files_items = statvfs("/")

def getLine(sCmd):
    i=0
    idx=None
    stringData=""
    while stringData=="":
        rxData = bytes()
        time.sleep(1)
        while myUsart0.any() > 0:
            rxData += myUsart0.readline()
        idx=re.search("^CMD",rxData)
        if idx==None:
            print("No command, try again.")
            exit()
        print("rxData:", rxData)
        stringData = rxData.decode('utf-8')
        if (not stringData):
            i = i + 1
            print("No data:",i)
        else:
            idx=re.search(sCmd,stringData)
            
            #if stringData contains "listfiles" then idx will not be None
            if idx==None:
                print("CMD ",sCmd, "was not sent. Try again.")
                exit()
            elif idx!=None:
                print("CMD ",sCmd, "was sent")
            else:
                print("CMD ", sCmd, "WTF! What Happened?  i=",i)
            #print("i=",i,"Waiting for CMD response>" , stringData,"<")
            i = 0

def GetFileDump(sCmd):
    print("running GetFileDump =",sCmd)
    iFlg=0
    lineData=""
    stringData=""
    iLed=0
    iCmd=0
    recomma=re.compile(",")
    f=recomma.split(sCmd)
    filename="FilesDump"+f[1]
    file = open(filename, "w")
    # file.close()
    regex=re.compile("\n")
    while True:
        rxData = bytes()
        time.sleep(0.1)
        while myUsart0.any() > 0:
            rxData += myUsart0.read(1)
            # print("fileDump:", rxData)
        
        idx=re.search("CMD",rxData)
        idp=re.search("printfile",rxData)
        idlf=re.search("\n",rxData)
        if idx!=None or idp!=None:
            iCmd=2
            # print("When not None ->",iFlg,"iCmd=",iCmd,stringData,lineData,rxData)
        if iCmd>0:
            stringData = rxData.decode('utf-8')
            if len(stringData)==0:
                iFlg=1
                if lineData=="EOF":
                    file.close
                    return
                # print("stringData len=0, iFlg=",iFlg,"lineData=",lineData)
                lineData=""
            else:
                # print("if stringData len>0 ->",iFlg,stringData,lineData)
                if stringData=="EOF":
                    file.close
                    return
                if idlf!=None:   # iFlg==1:
                    # Print data & write data to files.
                    s=regex.split(stringData)
                    lineData=lineData+s[0]
                    if (len(lineData)>0):
                        if iCmd==1:
                            # print("Final-> ",lineData)
                            #file = open(filename, "a")
                            file.write(lineData+"\n")
                            #file.close()
                        else:
                            recmd=re.compile("CMD:")
                            fCmd=recmd.split(lineData)
                            print("Commmand ack received:",fCmd[1])
                    iCmd=1
                    lineData=s[1]
                    iFlg = 0
                    # Turn led on/off
                    iLed=(iLed+1)%2
                    led.value(iLed)
                else:
                    lineData=lineData+stringData
                # print("stringData len>0  iFlg==1? ->",iFlg,"iCmd=",iCmd,"idlf=",idlf,stringData,lineData)
            # print("iFlg=",iFlg,"len(stringData)=",len(stringData),"lineData=", lineData)



def SelectFile():
    j=0
    i=0
    iLed=0
    lineData=""
    
    while j==0:
        rxData = bytes()
        time.sleep(0.1)
        while myUsart0.any() > 0:
            rxData += myUsart0.read(1)
        
        stringData = rxData.decode('utf-8')
        if (len(stringData)==0):
            # print(len(stringData),stringData)
            i = i + 1
        else:
            # print(len(stringData),stringData)
            if i>0:
                # Print data & write data to files. 
                if (len(lineData)>0):
                    #print(len(lineData),">",lineData,"<")
                    fileNames=lineData.split("\n")
                    k=0
                    for each in fileNames:
                        k=k+1
                        if len(each)>0:
                            print(k,each)
                    j=1
                    # file = open(timestringfilename, "a")
                    # file.write(lineData+"\n")
                    # file.close()
                lineData=stringData
                i = 0
                # Turn led on/off
                iLed=(iLed+1)%2
                led.value(iLed)
            else:
                lineData=lineData+stringData
    
    fileno=int(input('Enter filename number here (0 for none): '))
    
    k=0
    fileSelected=""
    for each in fileNames:
        k=k+1
        # print(k,fileno,each,fileSelected)
        if k==fileno:
            fileSelected=each
    # print("File Selected:",fileSelected)
    return fileSelected

try: 
    print("Get filenames")
    myUsart0.write(sCmdFiles)
    time.sleep(1)
    getLine(sCmdFiles)
    time.sleep(1)

    print("Waiting for filenames.")
    fileSelected= SelectFile()

    if len(fileSelected)>0:
        myUsart0.write(sCmdPrint+fileSelected)
        time.sleep(1)
        GetFileDump(sCmdPrint+fileSelected)
        time.sleep(1)
        # remove files=? 
        yn=""
        while yn!="y" and yn!="n":
            yn=input("Remove "+fileSelected+"(y/n)")
        if yn=="y":
            myUsart0.write(sCmdRemove+fileSelected)
    time.sleep(3)
    print("Restart sending data")
    myUsart0.write("restart")
    print("FishFilesCMDs.py Complete")


except KeyboardInterrupt:
    print("Keyboard")
    pass # machine.soft_reset()

  