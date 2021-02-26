from flask import render_template, jsonify
from app import app
import sqlite3
import math, asyncio
import serial, json, time, random
from aiohttp import web
import aiohttp_jinja2
import jinja2
from flask import request, redirect, url_for
ser = None
conn = None

@aiohttp_jinja2.template('test.html.jinja2')
async def home(request):
   # holdval=rdata()
    return {}

@aiohttp_jinja2.template('newtemp.html.jinja2')
async def newdisp(request):
    wlevel = 30
    return{}



async def data(request):
    cursor = conn.execute("SELECT * from rvsensor ORDER BY timestamp DESC LIMIT 1;")
    record = cursor.fetchone()
    cursor.close()



    # tempvals=rdata()
    sensdata={'temp': record[2], 'humid': record[3], 'door': record[6], 'presence': record[4], 'water level': record[5], 'tor': record[1]}

    return web.json_response(sensdata)

async def tempinfo(request):
    cursor = conn.execute("SELECT * from rvsensor ORDER BY timestamp DESC LIMIT 10;")
    record = cursor.fetchall()
    cursor.close()
    times=[]
    temps=[]
    #currently just making a 5 point plot, can add more/take them away in future
    for x in range(10):
        times.append(record[x][1])
        temps.append(record[x][2])
    senddict ={'times': times, 'temps': temps}
    return web.json_response(senddict)


async def ligon(request):
    ser.write(('l').encode('ascii'))
    pstate = ser.readline()
    message = {'mess': pstate.decode('ascii')}
    return web.json_response(message)


async def ligoff(request):
    ser.write(('o').encode('ascii'))
    pstate = ser.readline()
    message = {'mess': pstate.decode('ascii')}
    return web.json_response(message)

async def buzzoff(request):
    ser.write(('q').encode('ascii'))
    pstate = ser.readline()
    message = {'mess': pstate.decode('ascii')}
    return web.json_response(message)

async def buzzon(request):
    ser.write(('b').encode('ascii'))
    pstate = ser.readline()
    message = {'mess': pstate.decode('ascii')}
    return web.json_response(message)

async def servo_l(request):
    ser.write(('x').encode('ascii'))
    pstate = ser.readline()
    message = {'mess': pstate.decode('ascii')}
    return web.json_response(message)

async def servo_r(request):
    ser.write(('y').encode('ascii'))
    pstate = ser.readline()
    message = {'mess': pstate.decode('ascii')}
    return web.json_response(message)

def rdata():
    cursor = conn.execute("SELECT * from rvsensor ORDER BY id DESC LIMIT 1;")
    record = cursor.fetchone()
    minid = record[0]
    cursor.close()
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


    cursor = conn.execute("INSERT INTO rvsensor VALUES(?,?,?,?,?,?,?)",
                          (minid + 1,round(time.time()) , sensVals[1], sensVals[2], round(sensVals[4]), sensVals[0], sensVals[3]))
    cursor.close()
    conn.commit()
    #return sensVals

def randtableEntries():
    cursor = conn.execute("SELECT * from rvsensor ORDER BY id DESC LIMIT 1;")
    record = cursor.fetchone()
    minid = record[0]
    cursor.close()
    logtime = math.floor(time.time())
    for x in range(100):
        temp = random.random()*35
        temp = round(temp,2)
        hum = 10 + random.random()*30
        hum = round(hum,2)
        pir = random.randint(0,1)
        halleff = random.randint(0,1)
        gals = round(random.random()*40,2)
        cursor = conn.execute("INSERT INTO rvsensor VALUES(?,?,?,?,?,?,?)",(x+minid+1,logtime,temp,hum,pir,gals,halleff))
        cursor.close()
        conn.commit()
        logtime +=1

async def runserver(app):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="127.0.0.1", port=5000)
    await site.start()

async def readdata(serial):
    while(True):
        rdata()
        await asyncio.sleep(2.34)

def main():
    global ser, conn
    conn = sqlite3.connect("development.db")
    DEVICE = 'COM8'
    ser = serial.Serial(DEVICE)
    time.sleep(2)
    #randtableEntries()
    app = web.Application()
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('templates'))
    app.add_routes([web.get('/', home),
                    web.get('/data.json',data),
                    web.static('/static','static'),
                    web.get('/ligon.json',ligon),
                    web.get('/new',newdisp),
                    web.get('/ligoff.json',ligoff),
                    web.get('/buzzon.json',buzzon),
                    web.get('/tempinfo.json', tempinfo),
                    web.get('/buzzoff.json',buzzoff)])
    #web.run_app(app, host="127.0.0.1", port=5000)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runserver(app))
    loop.run_until_complete(readdata(ser))

if __name__=="__main__":
    main()