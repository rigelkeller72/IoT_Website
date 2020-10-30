from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Rigel!!...Trying to run on a different virtual enviornment'