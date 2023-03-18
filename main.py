import db

from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'f796d2d8943e04e26f93a27802d72d369f47f310f7533e8a2d6a6bdb27c8ae0a'


def setup():
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

        # to do, figure out where to redirect and then do it in the function below
        # return redirect(url_for("cust_or_emp"))

    return render_template("cust_or_emplo.html")



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
