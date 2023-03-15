import db

from flask import Flask, request, render_template

app = Flask(__name__)

def setup():
    db.init_db()

@app.route('/')
def welcome():
    if request.method == 'POST':
        print("post")
    return render_template("welcome.html")

@app.route('/login')
def login():
    return 'login'

@app.route('/create_customer')
def create_customer():
    return 'create customer'

@app.route('/create_employee')
def create_employee():
    return 'create employee'


if __name__ == '__main__':
    app.run()
