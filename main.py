import db

from flask import Flask, request, render_template

app = Flask(__name__)

def setup():
    db.init_db()

# LOGIN STUFF

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

# CUSTOMER STUFF

@app.route('/room_search')
def room_search():
    # checks that you are logged in as a customer
    return 'searchbar, list of rooms'

@app.route('/book_room')
def book_room():
    # linked to from room_search
    return 'book a room'

@app.route('customer_view_rooms')
def customer_view_rooms():
    # check that user is customer
    return 'list of booked and rented rooms'

@app.route('customer_account')
def customer_account():
    return 'customer account details'

# EMPLOYEE STUFF

@app.route('rent_room')
def rent_room():
    return 'rent room'

@app.route('employee_account')
def employee_account():
    return 'employee account details'

# MANAGER STUFF

@app.route('edit_hotel')
def edit_hotel():
    # edit/delete hotel
    return 'edit hotel'

@app.route('add_hotel')
def add_hotel():
    return 'add hotel'

@app.route('room_list')
def room_list():
    return 'list of rooms'

@app.route('edit_room')
def edit_room():
    return 'edit room info'

@app.route('add_room')
def add_room():
    return 'add room'


if __name__ == '__main__':
    app.run()
