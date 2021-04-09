import aiohttp_jinja2
import jinja2
from aiohttp import web
import requests
import serial, time, sqlite3, asyncio
import cv2


async def data(request):  # returns most recent database entry
    cursor = conn.execute("SELECT * from rvsensor ORDER BY timestamp DESC LIMIT 1;")
    record = cursor.fetchone()
    cursor.close()
    sensdata = {'temp': record[2], 'humid': record[3], 'door': record[6], 'presence': record[4],
                'water level': record[5], 'tor': record[1], 'astat': alarmarm}

    return web.json_response(sensdata)


# Face database located in site_data.db
# returns most recent face database entry
async def facedata(request):
    cursor = faceconn.execute("SELECT * from faces ORDER BY timestamp DESC LIMIT 1;")
    record = cursor.fetchone()
    cursor.close()
    sensfacedata = {'centroidx': record[0], 'centroidy': record[1], 'timestamp': record[2]}

    return web.json_response(sensfacedata)


# returns 24 entries, spaced according to desired range
async def tempinfo(request):
    numbah = int(request.query["num"])
    skipfreq = int(request.query["skip"])
    cursor = conn.execute(
        "SELECT timestamp,temperature,humidity from rvsensor ORDER BY timestamp DESC LIMIT %d" % numbah)
    record = cursor.fetchall()
    cursor.close()
    times = []
    temps = []
    hums = []
    for x in range(0, numbah, skipfreq):
        times.append(record[x][0])
        temps.append(record[x][1])
        hums.append(record[x][2])
    senddict = {'times': times, 'temps': temps, 'hums': hums}
    return web.json_response(senddict)


async def waterinfo(request):  # same as heathum, but for water level
    numbah = int(request.query["num"])
    skipfreq = int(request.query["skip"])
    cursor = conn.execute("SELECT timestamp,waterlevel from rvsensor ORDER BY timestamp DESC LIMIT %d" % numbah)
    record = cursor.fetchall()
    cursor.close()
    times = []
    wlev = []
    for x in range(0, numbah, skipfreq):
        times.append(record[x][0])
        wlev.append(record[x][1])
    senddict = {'times': times, 'levs': wlev}
    return web.json_response(senddict)


async def ligon(request):  # engages lock
    ser.write(('l').encode('ascii'))
    pstate = ser.readline()
    message = {'mess': pstate.decode('ascii')}
    return web.json_response(message)


# unlock process, tells arduino to actuate
async def ligoff(request):
    ser.write(('o').encode('ascii'))
    pstate = ser.readline()
    message = {'mess': pstate.decode('ascii')}
    return web.json_response(message)


# tells arduino to turn off buzzer
def buzzoff():
    ser.write(('q').encode('ascii'))
    ser.readline()


# turns on buzzer by telling arduino
def buzzon():
    ser.write(('b').encode('ascii'))
    ser.readline()


async def armDisarm(request):
    global alarmarm
    if alarmarm:
        alarmarm = 0
    else:
        alarmarm = 1
    message = {"mess": "Alarm toggeled"}
    return web.json_response(message)


def rdata():  # process of reading and recording data
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
    sensVals[1] = round(sensVals[1] * 9 / 5.0 + 32)
    cursor = conn.execute("INSERT INTO rvsensor VALUES(?,?,?,?,?,?,?)",
                          (minid + 1, round(time.time()), sensVals[1], sensVals[2], round(sensVals[4]), sensVals[0],
                           sensVals[3]))
    cursor.close()
    conn.commit()
    # migrated over to server instead of website to avoid the alarm turning off when site exited
    if alarmarm and round(sensVals[4]):
        buzzon()
    else:
        buzzoff()
    # return sensVals


async def runserver(app):  # runs site on port 5000, local hosting
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="127.0.0.1", port=5000)
    await site.start()


# reads data every x seconds, infinitly
async def readdata(serial):
    while (True):
        rdata()
        await asyncio.sleep(2.5)


def main():
    global ser, conn, faceconn, alarmarm
    alarmarm = 0
    conn = sqlite3.connect("development.db")
    faceconn = sqlite3.connect("site_data.db")
    DEVICE = 'COM5'
    ser = serial.Serial(DEVICE)
    time.sleep(2)
    app = web.Application()
    app.add_routes([
        web.get("/data.json", data),
        web.get("/facedata.json", facedata),
        web.get('/tempinfo.json', tempinfo),
        web.get('/watinfo.json', waterinfo),
        web.get('/ligon.json', ligon),
        web.get('/ligoff.json', ligoff),
        web.get('/togglealarm.json', armDisarm)
    ])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runserver(app))
    loop.run_until_complete(readdata(ser))


main()
