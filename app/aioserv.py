from flask import render_template, jsonify
from app import app
import serial, json, time, random
from aiohttp import web
import aiohttp_jinja2
import jinja2
from flask import request, redirect, url_for
ser = None

@aiohttp_jinja2.template('test.html.jinja2')
async def home(request):
    holdval=rdata()
    return {}


async def data(request):
    tempvals=rdata()
    sensdata={'temp': tempvals[1], 'humid': tempvals[2], 'door': tempvals[3],
              'gals': tempvals[0], 'near':tempvals[4]}
    return web.json_response(sensdata)


async def ligon(request):
    ser.write(('l').encode('ascii'))
    pstate = ser.readline()
    message = {'mess': pstate.decode('ascii')}
    return web.json_response(message)

def rdata():
    serprint = ('r').encode('ascii')
    ser.write(serprint)
    rxdata = ser.readline()
    str = rxdata.decode('ascii')
    # converts to string and splits comma deliniated
    chunks = str.split(',')
    sensVals = []
    # casts strings into floats
    # print(chunks)
    chunks[0] = chunks[0][1:]
    togalls = .393701 * 23.5 * 23 * .004329
    for sense in chunks:
        sensVals.append(float(sense))
    sensVals[0] = 40 - sensVals[0] * togalls
    sensVals[0] = round(sensVals[0], 2)
    if sensVals[3] != 0:
        # ser.write(('b').encode('ascii'))
        # ser.readline()
        doorstate = "Door OPEN"
    else:
        doorstate = "Door Secured"
    if sensVals[4] > .5:
        near = "Person Near!"
    else:
        near = "No one Around."
        return sensVals


def main():
    global ser
    DEVICE = 'COM8'
    ser = serial.Serial(DEVICE)
    time.sleep(2)
    app = web.Application()
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('templates'))
    app.add_routes([web.get('/', home),
                    web.get('/data.json',data),
                    web.static('/static','static'),
                    web.get('/ligon.json',ligon)])
    web.run_app(app, host="127.0.0.1", port=5000)

if __name__=="__main__":
    main()