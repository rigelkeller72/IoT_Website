import serial
DEVICE = 'COM8'
ser = serial.Serial(DEVICE)
while True:
    #Reads in serial data
    serprint = ('r' + '\n').encode('ascii')
    rxdata = ser.readline()
    str = rxdata.decode('ascii')
    #converts to string and splits comma deliniated
    chunks = str.split(',')
    sensVals =[]
    #casts strings into floats
    for sense in chunks:
        sensVals.append(float(sense))
    sensVals[3] = sensVals[3]*100
    #prints the values sent
    print("The distance is %f cm.\nThe temperature is %f degrees C" %(sensVals[0],sensVals[1]))
    print("The humidity is %f percent\nThe potentiometer is %f percent" %(sensVals[2],sensVals[3]))
    if sensVals[0] < 10:
        #sends info to turn on light/turn off light
        print("Back up")
        serprint = ('l'+'\n').encode('ascii')
        ser.flush()
        ser.write(serprint)
        ser.flush()
    else:


        ser.write(serprint)
        ser.flush()
