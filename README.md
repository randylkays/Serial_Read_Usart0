# rp
RaspberryPI
Serial_Read_Usart0.py is a Raspberry PI Pico python program to read data from the UART. It prints and save the data. Filename FishYYYYMMDD_hhmmss.csv
Data rate of 1200 baud, transmit on Pin 0 and read on Pin 1

Reads data from Pin1
Then send the command to set time. 
Then send the  header cmd to resend the header
Now while read data, save to file.
