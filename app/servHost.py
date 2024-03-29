from aiohttp import web
import aiohttp_jinja2, secrets, time
import jinja2, requests, sqlite3,math
from hashlib import md5


# Renders Kewl Bus Site
@aiohttp_jinja2.template('polished.html.jinja2')  # loads in the dashboard
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


@aiohttp_jinja2.template('loginpage.html.jinja2')
async def login(request):
    return {}


async def logatmp(request):
    data = await request.post()
    uname = data['username']
    cursor = conn.execute("SELECT password,salt,logexp,cookie from users WHERE username = ?", (uname,))
    rec = cursor.fetchone()
    if rec != None:
        tocomp = data['pword'] + rec[1]
        if rec[0] == md5(tocomp.encode('ascii')).hexdigest():
            if rec[2] < time.time():
                cook = secrets.token_hex()
                cursor = conn.execute("UPDATE users SET cookie = ?, logexp=? WHERE username=?",
                                      (cook, time.time() + 604800, uname))
                conn.commit()
                response = web.Response(text="congrats!",
                                        status=302,
                                        headers={'Location': "/"})
                response.cookies['logged_in'] = cook
                # ahah
                return response
            else:
                response = web.Response(text="congrats!",
                                        status=302,
                                        headers={'Location': "/"})
                response.cookies['logged_in'] = rec[3]
                return response
        else:
            raise web.HTTPFound("/login")
    else:
        raise web.HTTPFound("/login")


def checklogin(request):
    if "logged_in" not in request.cookies:
        return True

    cursor = conn.execute("SELECT logexp FROM users where cookie = ?", (request.cookies['logged_in'],))
    print(request.cookies['logged_in'])

    record = cursor.fetchone()
    if record is None:
        return True
    print(record[0])
    print(time.time())
    if record[0] < time.time():
        return True
    return False


async def logout(request):
    response = aiohttp_jinja2.render_template('loginpage.html.jinja2', request, {})
    response.cookies['logged_in'] = 'badcookie'
    return response


async def data(request):  # requests data from database
    global connection
    try:
        r = requests.get("http://127.0.0.1:5000/data.json")
        connection = 1
        mess = r.json()
        mess['connect'] = connection
        cursor = conn.execute("SELECT * from rvsensor ORDER BY id DESC LIMIT 1;")  # similiar code for face data
        record = cursor.fetchone()
        minid = record[0]
        cursor.close()
        cursor = conn.execute("INSERT INTO rvsensor VALUES(?,?,?,?,?,?,?)",
                              (minid + 1, mess['tor'], mess['temp'], mess['humid'], mess['presence'],
                               mess['water level'], mess['door']))
        conn.commit()
        cursor.close()
        return web.json_response(mess)
    except:
        connection = 0;
        cursor = conn.execute("SELECT * from rvsensor ORDER BY timestamp DESC LIMIT 1;")
        record = cursor.fetchone()
        cursor.close()
        mess = {'temp': record[2], 'humid': record[3], 'door': record[6], 'presence': record[4],
                'water level': record[5], 'tor': record[1], 'astat': 0}
        # mess = {"connect": connection}
        mess["connect"]: connection
        return web.json_response(mess)


# requests data from  face database
async def facedata(request):
    global connection
    cursor = faceconn.execute("SELECT * from faces ORDER BY timestamp DESC LIMIT 1;")
    record = cursor.fetchone()
    cursor.close()
    mess = {'centroidx': record[0], 'centroidy': record[1], 'timestamp': record[2]}
    mess["connect"]: connection
    return web.json_response(mess)


async def ligon(request):  # requests for api to turn on locks
    logmess = checklogin(request)
    if logmess:
        mess = {"mess": "bCookie"}
        return web.json_response(mess)
    if connection == 1:
        r = requests.get("http://127.0.0.1:5000/ligon.json")
        return web.json_response(r.json())


async def ligoff(request):  # requests locks to be turned off
    logmess = checklogin(request)
    if logmess:
        mess = {"mess": "bCookie"}
        return web.json_response(mess)

    if connection == 1:
        r = requests.get("http://127.0.0.1:5000/ligoff.json")

        return web.json_response(r.json())


async def tempinfo(request):  # requests data for heat/humidity graph
    if connection == 1:
        reqstr = "http://127.0.0.1:5000/tempinfo.json?num=" + request.query['num']
        r = requests.get(reqstr)
        return web.json_response(r.json())
    else:
        numbah = int(request.query['num'])
        cursor = conn.execute(
            "SELECT timestamp from rvsensor ORDER BY timestamp DESC")
        record = cursor.fetchone()
        lasttime=record[0]-numbah
        cursor.close()
        cursor = conn.execute(
            "SELECT timestamp,temperature,humidity from rvsensor WHERE timestamp>? ORDER BY timestamp DESC", (lasttime,))
        record = cursor.fetchall()
        cursor.close()
        times = []
        temps = []
        hums = []
        skipfreq=math.ceil(len(record)/24)
        for x in range(0, len(record), skipfreq):
            times.append(record[x][0])
            temps.append(record[x][1])
            hums.append(record[x][2])
        senddict = {'times': times, 'temps': temps, 'hums': hums}
        return web.json_response(senddict)


async def watinfo(request):  # requests water level graph info
    if connection == 1:
        reqstr = "http://127.0.0.1:5000/watinfo.json?num=" + request.query['num']
        r = requests.get(reqstr)
        return web.json_response(r.json())
    else:
        numbah = int(request.query["num"])
        cursor = conn.execute(
            "SELECT timestamp from rvsensor ORDER BY timestamp DESC")
        record = cursor.fetchone()
        lasttime = record[0] - numbah
        cursor.close()
        cursor = conn.execute("SELECT timestamp,waterlevel from rvsensor WHERE timestamp > ? ORDER BY timestamp DESC" ,(lasttime,))
        record = cursor.fetchall()
        cursor.close()
        times = []
        wlev = []
        skipfreq = math.ceil(len(record) / 24)
        for x in range(0, len(record), skipfreq):
            times.append(record[x][0])
            wlev.append(record[x][1])
        senddict = {'times': times, 'levs': wlev}
        return web.json_response(senddict)


async def arm(request):  # requests alarm to toggle
    logmess = checklogin(request)

    if logmess:
        mess = {"mess": "bCookie"}
        return web.json_response(mess)
    if connection == 1:
        r = requests.get("http://127.0.0.1:5000/togglealarm.json")
        return web.json_response(r.json())


# async def webcam(request):
#     logmess = checklogin(request)
#     # grab the reference to the webcam
#     camera = cv2.VideoCapture(0)
#
#     # keep looping
#     while True:
#         print("Camera is running")
#         # grab the current frame
#         (grabbed, frame) = camera.read()
#
#         #    # resize the frame, optional
#         #    frame = cv2.resize(frame, (0,0), fx=2.0, fy=2.0)
#
#         # show the frame to our screen and increment the frame
#         show = cv2.imshow("Test Webcam", frame)
#
#         # if the 'q' key is pressed, stop the loop
#         key = cv2.waitKey(1) & 0xFF
#         if key == 27 or key == ord("q"):
#             break
#
#     # cleanup the camera and close any open windows
#     camera.release()
#     cv2.destroyAllWindows()
#
#     return web.json_response(show)


def main():  # defines paths, launches on 0.0.0.0:
    global connection, conn, faceconn;
    connection = 1
    conn = sqlite3.connect("servdb.db")  # add in later prolly change name
    faceconn = sqlite3.connect("site_data.db")
    app = web.Application()
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('templates'))
    # creates routes for various methods
    app.add_routes([web.get('/', home),
                    web.get('/firstsite', firstsite),
                    web.get('/timeline', timeline),
                    web.get('/team', bioinfo),
                    web.get('/arduino_code_static', arduino_code_static),
                    web.get('/data.json', data),
                    web.get('/facedata.json', facedata),
                    web.static('/static', 'static'),
                    web.get('/ligon.json', ligon),
                    web.get('/ligoff.json', ligoff),
                    web.get('/tempinfo.json', tempinfo),
                    web.get('/watinfo.json', watinfo),
                    web.get('/login', login),
                    web.get('/logout', logout),
                    web.post('/login', logatmp),
                    web.get('/togglealarm.json', arm)])

    # web.run_app(app, port=80)
    web.run_app(app, host="127.0.0.1", port=3000)  # for local dev


main()
