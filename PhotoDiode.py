import machine
from machine import Pin, ADC, UART
# import utime
import time 

lightSensor_value = machine.ADC(26) # Setup GP26 with a photodiode to sense light level
BRate=2400
print("Baud Rate:" ,BRate)
myUsart0 = UART(0, baudrate=BRate, bits=8, tx=Pin(0), rx=Pin(1), timeout=10)
myUsart1 = UART(1, baudrate=BRate, bits=8, tx=Pin(8), rx=Pin(9), timeout=10)

rxData = bytes()
t00 = time.ticks_us()
myUsart0.write(str(t00))
i=0
while True:
  lightValue = lightSensor_value.read_u16()  # proves ADC26 is functioning
  i=i+1
  t0 = time.ticks_us()
  if i % 1000 == 0:
      rxData = bytes()
      myUsart0.write(str(t0))
      print("t0:",t0)
      time.sleep(0.1)
      
  while myUsart1.any() > 0:
    rxData += myUsart1.read(1)
    print("myUsart1: " , rxData.decode('utf-8'))
  
  print ("i,t0,lightValue:",i/10000,t0/t00,lightValue*3.3/(65535),"myUsart1: " , rxData.decode('utf-8'))
  
  # utime.sleep(0.250)
