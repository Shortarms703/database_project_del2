import db

from flask import Flask, request, render_template, sessions

app = Flask(__name__)


def setup():
    db.init_db()


# LOGIN STUFF

@app.route('/')
def welcome():
    return render_template("welcome.html")


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/create_customer')
def create_customer():
    return render_template('create_customer.html')


@app.route('/create_employee')
def create_employee():
    return render_template('create_employee.html')


# CUSTOMER STUFF

@app.route('/room_search')
def room_search():
    # checks that you are logged in as a customer
    list_of_rooms = []  # list of rooms depending on what is being searched for
    return render_template('room_list.html', rooms=list_of_rooms)


@app.route('/book_room')
def book_room():
    # linked to from room_search
    return render_template('book_room.html')


@app.route('customer_view_rooms')
def customer_view_rooms():
    # check that user is customer
    list_of_rooms = []  # a list of only the rooms that the customer has booked/rented
    return render_template('room_list.html', rooms=list_of_rooms)


@app.route('customer_account')
def customer_account():
    return render_template('customer_details.html')


# EMPLOYEE STUFF

@app.route('rent_room')
def rent_room():
    list_of_rooms = []
    return render_template('room_list.html', rooms=list_of_rooms)


@app.route('employee_account')
def employee_account():
    return render_template('employee_details.html')


# MANAGER STUFF

@app.route('edit_hotel')
def edit_hotel():
    # edit/delete hotel
    return render_template('edit_hotel.html')


@app.route('add_hotel')
def add_hotel():
    return render_template('add_hotel.html')


@app.route('room_list')
def room_list():
    list_of_rooms = []
    return render_template('room_list.html', rooms=list_of_rooms)


@app.route('edit_room')
def edit_room():
    return render_template('edit_room_info.html')


@app.route('add_room')
def add_room():
    return render_template('add_room.html')


if __name__ == '__main__':
    app.secret_key('f796d2d8943e04e26f93a27802d72d369f47f310f7533e8a2d6a6bdb27c8ae0a')
    app.run()
