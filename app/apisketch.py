import aiohttp
from aiohttp import web


async def temp(request):
    return web.json_response({'temperature':80})

def main():
    app = web.Application()
    app.add_routes([
        web.get("/temperature.json",temp)
    ])
    web.run_app(app, port=5000)

main()