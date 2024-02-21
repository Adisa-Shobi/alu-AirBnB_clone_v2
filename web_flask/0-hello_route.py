#!/usr/bin/python3
'''
Starts a minimal flask application and server on the
'''


from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host='localhost', port=5000)
