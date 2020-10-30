# simpe serial code to read single sensor

import serial
DEVICE = 'COM5'
ser = serial.Serial(DEVICE)
while True:
    rxdata = ser.readline()
    str = rxdata.decode('ascii')
    chunks = str.split(',')
    sensVals =[]
    for sense in chunks:
        sensVals.append(float(sense))

    print("The humidity is %f percent\nThe Temperature is %f percent" %(sensVals[0],sensVals[1]))
    # print("The distance is %f cm.\nThe temperature is %f degrees C" %(sensVals[0],sensVals[1]))
    # print("The humidity is %f percent\nThe potentiometer is %f percent" %(sensVals[2],sensVals[3]))