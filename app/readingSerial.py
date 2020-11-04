from flask import Flask
import serial
import time
from flask import request
app = Flask(__name__)   


@app.route('/', methods=['GET'])
def hello_world():
    DEVICE = 'COM8'
    ser = serial.Serial(DEVICE)
    time.sleep(2)
    serprint = ('r').encode('ascii')
    ser.write(serprint)
    rxdata = ser.readline()
    str = rxdata.decode('ascii')
    # converts to string and splits comma deliniated
    chunks = str.split(',')
    sensVals = []
    # casts strings into floats
    for sense in chunks:
        sensVals.append(float(sense))
    #sensVals[3] = sensVals[3] * 100
    ser.close()


    return "<h1>" + str + "</h1>"
