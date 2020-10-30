import serial
import time
DEVICE = 'COM8'
ser = serial.Serial(DEVICE)
time.sleep(1)
#Reads in serial data
for i in range(4):
    serprint = ("l").encode('ascii')
    ser.write(serprint)
    time.sleep(.5)
    rxdata = ser.readline()
    str = rxdata.decode('ascii')
    print(str)
    ser.write("o".encode('ascii'))
    time.sleep(.5)
ser.flush()
ser.close()
#converts to string and splits comma deliniated
#chunks = str.split(',')
#sensVals =[]
#casts strings into floats
#for sense in chunks:
#    sensVals.append(float(sense))
#sensVals[3] = sensVals[3]*100
##prints the values sent
#print("The distance is %f cm.\nThe temperature is %f degrees C" %(sensVals[0],sensVals[1]))
#print("The humidity is %f percent\nThe potentiometer is %f percent" %(sensVals[2],sensVals[3]))

