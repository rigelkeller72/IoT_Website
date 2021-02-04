THIS IS A BRANCH FROM MAIN.

I AM WORKING ON AJAX MATERIAL.


Deleted previous AJAX work
Deleted ajax_info.txt



Donnal Class work

Added hello_world.html 

added the requiremetns.txt file
had to install aiohtpp

switched the configutations to run python and to run the file webserver.py



# Webserver!

from aiohttp import web

#my serial= none


async def home(request):
    f = open("hello_world.html", "r")
    contents = f.read()
    f.close()
    #myserial.read()
    return web.Response(text=contents, content_type="text/html")


async def aboutme(request):
    return web.Response(text="You are at about me!")


def main():
# serial stuff here
    #myserial = serial.Serial('COM6')
    app = web.Application()

    web.run_app(app)
    app.add_routes([web.get('/home.html', home), web.get('/about_me.html', aboutme)])

    print("Hi welcome to Webserver 1.0")
    web.run_app(app, host="127.0.0.1", port="3000")


main()

 
rename html to jinja2 or really just append a jinja2 at the end of the html file ex helloworld.html.jinja2


