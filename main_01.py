#c Verfiy LED/Sensor pairs work
# Printing Sent and receive data
# Solid LED: RP running, but not receiving
# Flashing LED: receive working
# LED off: RP Not running

from machine import UART, Pin
import time
led = Pin(25, Pin.OUT)   # create LED object from Pin 25, Set Pin 15 to output

BRate=2400
print("Baud Rate:" ,BRate)
myUsart0 = UART(0, baudrate=BRate, bits=8, tx=Pin(0), rx=Pin(1), timeout=10)
myUsart1 = UART(1, baudrate=BRate, bits=8, tx=Pin(4), rx=Pin(5), timeout=10)
led.value(1)
i=1

try:
    while True:
        rxData = bytes()
        i=i+1
        j=1
        input_cnt = "Test:" + str(i) # str(input("myUsart0: "))
        print("Sending: ", input_cnt)
        myUsart0.write(input_cnt)
        time.sleep(0.1)
        while myUsart1.any() > 0:
            rxData += myUsart1.read(1)
            j=i%2
        print("myUsart1 receive: " , rxData.decode('utf-8'))
        led.value(j)
    
    
except KeyboardInterrupt:
    print("Keyboard -> LED off")
    led.value(0)
    pass 