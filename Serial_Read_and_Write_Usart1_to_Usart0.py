from machine import UART, Pin
import time
BRate=2400
print("Baud Rate:" ,BRate)
myUsart0 = UART(0, baudrate=BRate, bits=8, tx=Pin(0), rx=Pin(1), timeout=10)
myUsart1 = UART(1, baudrate=BRate, bits=8, tx=Pin(8), rx=Pin(9), timeout=10)

while True:
    rxData = bytes()
    input_cnt = str(input("myUsart0: "))
    myUsart0.write(input_cnt)
    time.sleep(0.1)
    while myUsart0.any() > 0:
        rxData += myUsart0.read(1)
    print("myUsart0: " , rxData.decode('utf-8'))
    