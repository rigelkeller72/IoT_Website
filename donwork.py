import serial
import time
DEVICE = 'COM8'
ser = serial.Serial(DEVICE)
#while True:
if 1 == 1:
    #Reads in serial data
    time.sleep(.01)
    ser.flush()
    serprint = ("r\n").encode('ascii')
    ser.write(serprint)
    rxdata = ser.readline()
    str = rxdata.decode('ascii')
    str = 'ahahah'
    print(str)
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

