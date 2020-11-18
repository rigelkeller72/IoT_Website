from flask import render_template
from app import app
import serial, json
import time
from flask import request, redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Rigel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Annapolis!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'What about that election? Am I right!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/cats')
def cats():
    user = {'username': 'Rigel is cool'}
    posts = [
        {
            'author': {'username': 'Max'},
            'body': 'I love cats soooo much!'
        },
        {
            'author': {'username': 'Bob'},
            'body': 'I LOVE CATS TOO! We should hang out?'
        }
    ]
    return render_template('index.html', title='Cats', user=user, posts=posts)


@app.route('/login')
def login():
    user = {'username': 'Rigel'}
    return render_template('login.html', title='Login', user=user)


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
        for sense in chunks:
            sensVals.append(float(sense))
        #sensVals[3] = sensVals[3] * 100
        if sensVals[3] != 0:
            ser.write(('b').encode('ascii'))
            ser.readline()
            doorstate = "Door OPEN!"
        else:
            doorstate = "Door Secured."
        ser.close()
        newstr = "Range: %.2f cm, Temp: %.2f C, Humidity: %.2f Percent, %s"% (sensVals[0], sensVals[1], sensVals[2], doorstate)

        #return newstr
        return render_template('data.html', title='Data', str=newstr)


@app.route('/turnon', methods=['POST'])
def turnON():
    if request.method == 'POST':
        print(request.values)
        DEVICE = 'COM8'
        ser = serial.Serial(DEVICE)
        time.sleep(1.8)
        serprint = ('l').encode('ascii')
        ser.write(serprint)
        ser.readline()
        return redirect(url_for('data'))

@app.route('/turnoff', methods=['POST'])
def turnOff():
    if request.method == 'POST':
        print(request.values)
        DEVICE = 'COM8'
        ser = serial.Serial(DEVICE)
        time.sleep(1.8)
        serprint = ('o').encode('ascii')
        ser.write(serprint)
        ser.readline()
        return redirect(url_for('data'))