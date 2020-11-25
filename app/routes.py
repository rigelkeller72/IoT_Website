from flask import render_template
from app import app
import serial, json, time
from flask import request, redirect, url_for


@app.route('/')
@app.route('/data', methods=['GET'])
def data():
    if request.method =='GET':
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
        #print(chunks)
        chunks[0] = chunks[0][1:]
        togalls = .393701*23.5*23*.004329
        for sense in chunks:
            sensVals.append(float(sense))
        sensVals[0] =40 - sensVals[0]*togalls
        if sensVals[3] != 0:
            #ser.write(('b').encode('ascii'))
            #ser.readline()
            doorstate = "Door OPEN"
        else:
            doorstate = "Door Secured"
        ser.close()
        if sensVals[4] > .5:
            near = "Person Near!"
        else:
            near = "No one Around."
        newstr = "Water: %.2f gallons, Temp: %.2f C, Humidity: %.2f Percent, %s, %s"% (sensVals[0], sensVals[1], sensVals[2], doorstate, near)

        #return newstr
        #return render_template('data.html', title='Data', str=newstr)
        return render_template('test.html', title='test', temp=sensVals[1], hum=sensVals[2], gals=sensVals[1], pir=near,hall=doorstate)


@app.route('/turnon', methods=['POST'])
def turnON():
    if request.method == 'POST':
        DEVICE = 'COM8'
        ser = serial.Serial(DEVICE)
        time.sleep(1.8)
        serprint = ('l').encode('ascii')
        ser.write(serprint)
        ser.readline()
        ser.close()
        return redirect(url_for('data'))

@app.route('/turnoff', methods=['POST'])
def turnOff():
    if request.method == 'POST':
        DEVICE = 'COM8'
        ser = serial.Serial(DEVICE)
        time.sleep(1.8)
        serprint = ('o').encode('ascii')
        ser.write(serprint)
        ser.readline()
        ser.close()
        return redirect(url_for('data'))

@app.route('/turnonb', methods=['POST'])
def turnONB():
    if request.method == 'POST':
        DEVICE = 'COM8'
        ser = serial.Serial(DEVICE)
        time.sleep(1.8)
        serprint = ('b').encode('ascii')
        ser.write(serprint)
        ser.readline()
        ser.close()
        return redirect(url_for('data'))

@app.route('/turnoffb', methods=['POST'])
def turnOffB():
    if request.method == 'POST':
        DEVICE = 'COM8'
        ser = serial.Serial(DEVICE)
        time.sleep(1.8)
        serprint = ('q').encode('ascii')
        ser.write(serprint)
        ser.readline()
        ser.close()
        return redirect(url_for('data'))

@app.route('/test')
def index():
    return render_template('test.html', title='Test Site')