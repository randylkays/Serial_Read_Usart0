# Serial_Read_Usart0 
RaspberryPI
Serial_Read_Usart0.py is a Raspberry PI (RP) Pico python program to read data from the UART. This program is intend to work with another RP Pico on cable.
The other RP Pico gathering data and sending it up the UART.  It also respond to setting the time (which it does not know) and resending the data header with a 10 second wait. 

It prints and save the data. Filename FishYYYYMMDD_hhmmss.csv
Data rate of 1200 baud, transmit on Pin 0 and read on Pin 1

Reads data from Pin1
Then send the command to set time. 
Then send the  header cmd to resend the header
Now while read data, save to file.

Works with mpremote to save the file on the PC (so far on linux) instead of on the RP Pico
with an alias: 
  alias mp='sudo python3 /usr/local/bin/mpremote'
Then run the program 
  mp mount . run Serial_Read_Usart.py

note "." save the file in the local folder. 
