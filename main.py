import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def welcome():
    return flask.render_template("welcome.html")

@app.route('/login')
def login():

    return 'login'


if __name__ == '__main__':
    app.run()
