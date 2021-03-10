import aiohttp
from aiohttp import web
import requests


async def index(request):
    r = requests.get("http://127.0.0.1:5000/temperature.json")
    data = r.json()
    return web.Response(text="temperature is %d" % data['temperature'])

def main():
    app = web.Application()
    app.add_routes([
        web.get("/",index)
    ])
    web.run_app(app)

main()