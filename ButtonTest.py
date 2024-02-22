from machine import Pin
import time
from sys import exit
              
button = Pin(17, Pin.IN, Pin.PULL_UP)    #Create button object from Pin13 , Set GP13 to input
led = Pin(25, Pin.OUT)   # create LED object from Pin 25, Set Pin 15 to output
print("Push the button", button.value())

try:
    while True:
        if not button.value():
            led.value(0)
            # print("Button Pushed - Bye")
            exit()
        else:
            led.value(1)
            # print("Button off") # button.valve()) #Set led turn off


except:
    pass

