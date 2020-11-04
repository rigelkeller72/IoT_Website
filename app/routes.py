from flask import render_template
from app import app
import serial
import time
from flask import request

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
    user = {'username': 'Rigel'}
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
    DEVICE = 'COM5'
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

    return render_template('data.html', title='Data', str=str)

#Rigel is here