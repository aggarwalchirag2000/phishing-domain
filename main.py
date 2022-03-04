from flask import Flask
from wsgiref import simple_server
import atexit
import uuid
import os
from flask import Flask, session, request, Response, jsonify,render_template


app = Flask(__name__)

@app.route('/',methods = ['GET'])
def home_page():
    return render_template('home.html')

port =int(os.getenv("PORT",5001))

if __name__ == '__main__':
    host = '0.0.0.0'
    httpd = simple_server.make_server(host=host, port = port, app = app)
    print("http://localhost:5001/" )
    httpd.serve_forever()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
