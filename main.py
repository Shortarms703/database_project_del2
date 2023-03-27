from datetime import datetime

import db

from flask import Flask, request, render_template, session, redirect, url_for

from classes import Book, Chain, Customer, Employee, Hotel, Rent, Room

app = Flask(__name__)
app.secret_key = 'f796d2d8943e04e26f93a27802d72d369f47f310f7533e8a2d6a6bdb27c8ae0a'


def setup():
    # TODO actually call this sometime
    db.init_db()


# LOGIN STUFF


@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':

        # Handle the case where the "login" button was clicked
        if 'login' in request.form:
            session["login_or_create"] = "login"
        # Handle the case where the "create_new_account" button was clicked
        elif 'create_new_account' in request.form:
            session["login_or_create"] = "create_new_account"

        return redirect(url_for("cust_or_emp"))

    return render_template("welcome.html")


@app.route('/cust_or_emp', methods=['GET', 'POST'])
def cust_or_emp():
    if request.method == 'POST':

        # Handle the case where the "employee" button was clicked
        if 'employee' in request.form:
            session["cust_or_emp"] = "employee"

        # Handle the case where the "customer" button was clicked
        elif 'customer' in request.form:
            session["cust_or_emp"] = "customer"
        if session["login_or_create"] == "login":
            return redirect(url_for("login"))
        if session["login_or_create"] == "create_new_account":
            if session["cust_or_emp"] == "employee":
                return redirect(url_for("create_employee"))
            if session["cust_or_emp"] == "customer":
                return redirect(url_for("create_customer"))

    return render_template("cust_or_emplo.html")


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/create_customer', methods = ["GET", "POST"])
def create_customer():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        sin = request.form["sin"]
        street = request.form["street"]
        city = request.form["city"]
        postal_code = request.form["postal_code"]
        country = request.form["country"]
        hotel_id = request.form["chain_name_hotel_name"]
        current_customer = Customer(None, sin, hotel_id, first_name, last_name, datetime.today().strftime('%Y-%m-%d'),
                                    street, city, postal_code, country, password)
        current_customer.create_cust()
    hotels = db.get_hotel_from_create()
    return render_template('create_customer.html', hotels = hotels)


@app.route('/create_employee', methods = ["GET", "POST"])
def create_employee():
    if request.method == "POST":
        position = request.form["position"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        sin = request.form["sin"]
        street = request.form["street"]
        city = request.form["city"]
        postal_code = request.form["postal_code"]
        country = request.form["country"]
        hotel_id = request.form["chain_name_hotel_name"]
        current_emploee = Employee(sin, first_name, last_name, hotel_id, password, None, street, city, postal_code,
                                   country, position)
        current_emploee.create_emp()
    hotels = db.get_hotel_from_create()
    return render_template('create_employee.html', hotels = hotels)


# CUSTOMER STUFF

@app.route('/room_search', methods=["GET", "POST"])
def room_search():
    # checks that you are logged in as a customer
    list_of_rooms = db.get_all_rooms()  # should be just all the rooms
    if request.method == "POST":
        print(request.form.to_dict())
        if request.form["start_date"] == "":
            start_date = None
        else:
            start_date = request.form["start_date"]

        if request.form["end_date"] == "":
            end_date = None
        else:
            end_date = request.form["end_date"]

        if request.form["room_capacity"] == "":
            room_capacity = None
        else:
            room_capacity = int(request.form["room_capacity"])

        if request.form["area"] == "":
            area = None
        else:
            area = request.form["area"]

        if request.form["hotel_chain"] == "":
            hotel_chain = None
        else:
            hotel_chain = request.form["hotel_chain"]

        if request.form["hotel_stars"] == "none":
            hotel_stars = None
        else:
            hotel_stars = int(request.form["hotel_stars"])

        if request.form["num_rooms_in_hotel"] == "":
            num_rooms_in_hotel = None
        else:
            num_rooms_in_hotel = int(request.form["num_rooms_in_hotel"])

        if request.form["price_of_room"] == "":
            price_of_room = None
        else:
            price_of_room = int(request.form["price_of_room"])

        list_of_rooms = db.db_room_search(start_date, end_date, room_capacity, area, hotel_chain, hotel_stars,
                                          num_rooms_in_hotel, price_of_room)
        return render_template('room_list.html', rooms=list_of_rooms,
                               start_date=start_date,
                               end_date=end_date,
                               room_capacity=room_capacity,
                               area=area,
                               hotel_chain=hotel_chain,
                               hotel_stars=hotel_stars,
                               num_rooms_in_hotel=num_rooms_in_hotel,
                               price_of_room=price_of_room)
    return render_template('room_list.html', rooms=list_of_rooms)


@app.route('/book_room')
def book_room():
    # linked to from room_search
    return render_template('book_room.html')


@app.route('/customer_view_rooms')
def customer_view_rooms():
    # check that user is customer
    list_of_rooms = []  # a list of only the rooms that the customer has booked/rented
    return render_template('room_list.html', rooms=list_of_rooms)


@app.route('/customer_account')
def customer_account():
    return render_template('customer_details.html')


# EMPLOYEE STUFF

@app.route('/rent_room')
def rent_room():
    list_of_rooms = []
    return render_template('room_list.html', rooms=list_of_rooms)


@app.route('/employee_account')
def employee_account():
    return render_template('employee_details.html')


# MANAGER STUFF

@app.route('/edit_hotel')
def edit_hotel():
    # edit/delete hotel
    return render_template('edit_hotel.html')


@app.route('/add_hotel')
def add_hotel():
    return render_template('add_hotel.html')


@app.route('/room_list')
def room_list():
    list_of_rooms = []
    return render_template('room_list.html', rooms=list_of_rooms)


@app.route('/edit_room')
def edit_room():
    return render_template('edit_room_info.html')


@app.route('/add_room')
def add_room():
    return render_template('add_room.html')


if __name__ == '__main__':
    app.run()
