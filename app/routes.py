from flask import render_template, jsonify
from app import app
import serial, json, time, random
from flask import request, redirect, url_for


@app.route('/')
def home():
    if request.method =='GET':
        DEVICE = 'COM8'
        ser = serial.Serial(DEVICE)
        time.sleep(2)
        serprint = ('r').encode('ascii')
        ser.write(serprint)
        rxdata = ser.readline()
        ser.close()
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
        sensVals[0] = round(sensVals[0],2)
        if sensVals[3] != 0:
            #ser.write(('b').encode('ascii'))
            #ser.readline()
            doorstate = "Door OPEN"
        else:
            doorstate = "Door Secured"
        if sensVals[4] > .5:
            near = "Person Near!"
        else:
            near = "No one Around."
        newstr = "Water: %.2f gallons, Temp: %.2f C, Humidity: %.2f Percent, %s, %s"% (sensVals[0], sensVals[1], sensVals[2], doorstate, near)

        #return newstr
        #return render_template('data.html', title='Data', str=newstr)
        return render_template('test.html', title='test', temp=sensVals[1], hum=sensVals[2], gals=sensVals[0], pir=near,hall=doorstate)
@app.route('/data.json')
def data():
    mockdata={'temp': random.randint(150,250)/10, 'humid': random.randint(100,700)/10, 'door': random.randint(0,1),
              'gals': random.randint(10,400)/10, 'near':random.randint(0,1)}
    return jsonify(mockdata)

@app.route('/ligon.json')
def ligon():
    #time.sleep(1.8)
    #DEVICE = 'COM8'
    #ser = serial.Serial(DEVICE)
    #time.sleep(1.8)
    #serprint = ('l').encode('ascii')
    #ser.write(serprint)
    #pstate=ser.readline()
    #ser.close()
    #message = {'mess': pstate.decode('ascii')}
    #return jsonify(message)
    msend= {'mess': "Light on"}
    return jsonify(msend)

@app.route('/ligoff.json')
def ligoff():
    #time.sleep(1.8)
    #DEVICE = 'COM8'
    #ser = serial.Serial(DEVICE)
    #time.sleep(1.8)
    #serprint = ('l').encode('ascii')
    #ser.write(serprint)
    #pstate=ser.readline()
    #ser.close()
    #message = {'mess': pstate.decode('ascii')}
    #return jsonify(message)
    msend= {'mess': "Light off"}
    return jsonify(msend)

#@app.route('/turnon', methods=['POST'])
#def turnON():
#    if request.method == 'POST':
#        DEVICE = 'COM8'
#        ser = serial.Serial(DEVICE)
#        time.sleep(1.8)
#        serprint = ('l').encode('ascii')
#        ser.write(serprint)
#        ser.readline()
#        ser.close()
#        return redirect(url_for('data'))

#@app.route('/turnoff', methods=['POST'])
#def turnOff():
#    if request.method == 'POST':
#        DEVICE = 'COM8'
#        ser = serial.Serial(DEVICE)
#        time.sleep(1.8)
#        serprint = ('o').encode('ascii')
#        ser.write(serprint)
#        ser.readline()
#        ser.close()
#        return redirect(url_for('/'))

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