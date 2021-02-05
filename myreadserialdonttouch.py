from flask import Flask
import serial
import time
from flask import request
app = Flask(__name__)   


@app.route('/', methods=['GET'])
def turnOn():
    DEVICE = 'COM8'
    ser = serial.Serial(DEVICE)
    time.sleep(1.8)
    serprint = ('l').encode('ascii')
    ser.write(serprint)
    ser.readline()

def turnOff():
    DEVICE = 'COM8'
    ser = serial.Serial(DEVICE)
    time.sleep(1.8)
    serprint = ('l').encode('ascii')
    ser.write(serprint)
    ser.readline()


