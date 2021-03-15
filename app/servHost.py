from aiohttp import web
import aiohttp_jinja2
import jinja2, requests, sqlite3

# Renders Kewl Bus Site
@aiohttp_jinja2.template('polished.html.jinja2')#loads in the dashboard
async def home(request):
    # holdval=rdata()
    return {}

# Render template for first site
# Still named test.html
@aiohttp_jinja2.template('test.html.jinja2')
async def firstsite(request):
    return {}

# Render template timeline page
@aiohttp_jinja2.template('timeline.jinja2')
async def timeline(request):
    return {}

# Render arduino code page
@aiohttp_jinja2.template('arduino_code_static.jinja2')
async def arduino_code_static(request):
    return {}

@aiohttp_jinja2.template('team.html.jinja2')
async def bioinfo(request):
    return {}

async def data(request):#requests data from database
    global connection
    try:
        r = requests.get("http://127.0.0.1:5000/data.json")
        connection = 1
        mess = r.json()
        mess['connect'] = connection
        cursor = conn.execute("SELECT * from rvsensor ORDER BY id DESC LIMIT 1;")
        record = cursor.fetchone()
        minid = record[0]
        cursor.close()
        cursor = conn.execute("INSERT INTO rvsensor VALUES(?,?,?,?,?,?,?)",
                              (minid+1,mess['tor'],mess['temp'],mess['humid'],mess['presence'],mess['water level'],))
        return web.json_response(r.json())
    except:
        connection=0;
        cursor = conn.execute("SELECT * from rvsensor ORDER BY timestamp DESC LIMIT 1;")
        record = cursor.fetchone()
        cursor.close()
        mess = {'temp': record[2], 'humid': record[3], 'door': record[6], 'presence': record[4],
                    'water level': record[5], 'tor': record[1], 'astat': 0}
        print(mess)
        #mess = {"connect": connection}
        mess["connect"]: connection
        return web.json_response(mess)

async def localdata(): #returns most recent database entry
    cursor = conn.execute("SELECT * from rvsensor ORDER BY timestamp DESC LIMIT 1;")
    record = cursor.fetchone()
    cursor.close()
    sensdata={'temp': record[2], 'humid': record[3], 'door': record[6], 'presence': record[4], 'water level': record[5], 'tor': record[1], 'astat':0}
    print(sensdata)
    return sensdata

async def ligon(request):#requests for api to turn on locks
    if connection==1:
        r = requests.get("http://127.0.0.1:5000/ligon.json")
        return web.json_response(r.json())

async def ligoff(request): #requests locks to be turned off
    if connection==1:
        r = requests.get("http://127.0.0.1:5000/ligon.json")
        return web.json_response(r.json())

async def tempinfo(request): #requests data for heat/humidity graph
    if connection==1:
        reqstr = "http://127.0.0.1:5000/tempinfo.json?num="+request.query['num']+"&skip="+request.query['skip']
        r=requests.get(reqstr)
        return web.json_response(r.json())
    else:
        numbah = int(request.query['num'])
        skipfreq = int(request.query['skip'])
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


async def watinfo(request): #requests water level graph info
    if connection==1:
        reqstr = "http://127.0.0.1:5000/watinfo.json?num="+request.query['num']+"&skip="+request.query['skip']
        r=requests.get(reqstr)
        return web.json_response(r.json())
    else:
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

async def arm(request):#requests alarm to toggle
    if connection:
        r = requests.get("http://127.0.0.1:5000/togglealarm.json")
        return web.json_response(r.json())

def main():#defines paths, launches on 0.0.0.0:
    global connection, conn;
    conn = sqlite3.connect("servdb.db") #add in later prolly change name
    app = web.Application()
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('templates'))
    # creates routes for various methods
    app.add_routes([web.get('/', home),
                    web.get('/firstsite', firstsite),
                    web.get('/timeline', timeline),
                    web.get('/team',bioinfo),
                    web.get('/arduino_code_static', arduino_code_static),
                    web.get('/data.json', data),
                    web.static('/static', 'static'),
                    web.get('/ligon.json', ligon),
                    web.get('/ligoff.json', ligoff),
                    web.get('/tempinfo.json', tempinfo),
                    web.get('/watinfo.json', watinfo),
                    web.get('/togglealarm.json', arm)])

    #web.run_app(app, port=80)
    web.run_app(app, host="127.0.0.1", port=3000) #for local dev

main()
