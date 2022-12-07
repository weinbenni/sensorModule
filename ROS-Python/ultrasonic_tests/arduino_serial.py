import serial
import csv


ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM5'

ser.open()
while True:
    s = ser.readline()
    
    
    f = open('data.csv','a')

    writer = csv.writer(f)

    ss= s.decode("utf-8").split(' ')[1]
    print(ss)
    sss=[ss]
    writer.writerow(sss) 



ser.close()
