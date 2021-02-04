# Webserver!
import jinja2 as jinja2
from aiohttp import web
import aiohttp_jinja2
import jinja2

@aiohttp_jinja2.template('hello_world.html.jinja2')
async def home(request):
    return{}

async def home(request):
    f = open("hello_world.html", "r")
    contents = f.read()
    f.close()
    return web.Response(text=contents, content_type="text/html")


async def aboutme(request):
    return web.Response(text="You are at about me!")


def main():
    app = web.Application()

    app.add_routes([web.get('/home.html', home), web.get('/about_me.html', aboutme)])

    print("Hi welcome to Webserver 1.0")
    web.run_app(app, host="127.0.0.1", port=3000)


main()

