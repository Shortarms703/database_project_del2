import datetime

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


@app.route('/logout')
def logout():
    session["cust_or_emp"] = ""
    session["current_cust_id"] = ""
    session["current_emp_id"] = ""
    return redirect(url_for("welcome"))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        if session["cust_or_emp"] == "employee":
            value = db.check_if_login_valid_emp(name, password)
            if value == False:
                # remember to put message they fuck up telling them they fucked up
                return render_template('login.html')
            else:
                session["current_emp_id"] = value
                session["position"] = db.get_employee(value).position
                return redirect(url_for("rent_room"))

        if session["cust_or_emp"] == "customer":
            value = db.check_if_login_valid_cust(name, password)
            if value == False:
                # remember to put message they fuck up telling them they fucked up
                return render_template('login.html')
            else:
                session["current_cust_id"] = value
                return redirect(url_for("room_search"))

    return render_template('login.html')


@app.route('/create_customer', methods=["GET", "POST"])
def create_customer():
    create_cust_failed = False
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
        current_customer = Customer(None, sin, hotel_id, first_name, last_name,
                                    datetime.datetime.today().strftime('%Y-%m-%d'),
                                    street, city, postal_code, country, password)
        current_customer.create_cust()

        # checks to see if it is possible to login as the new customer
        if db.check_if_login_valid_cust(first_name, password):
            return redirect(url_for("login"))
        else:
            create_cust_failed = True

    hotels = db.get_hotel_from_create()
    return render_template('create_customer.html', hotels=hotels, create_cust_failed=create_cust_failed)


@app.route('/create_employee', methods=["GET", "POST"])
def create_employee():
    create_emp_failed = False
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
        current_employee = Employee(sin, first_name, last_name, hotel_id, password, None, street, city, postal_code,
                                    country, position)
        current_employee.create_emp()

        # checks to see if it is possible to login as the new employee
        if db.check_if_login_valid_emp(first_name, password):
            return redirect(url_for("login"))
        else:
            create_emp_failed = True

    hotels = db.get_hotel_from_create()
    return render_template('create_employee.html', hotels=hotels, create_emp_failed=create_emp_failed)


# CUSTOMER STUFF

@app.route('/room_search', methods=["GET", "POST"])
def room_search():
    # checks that you are logged in as a customer
    list_of_rooms = db.get_all_rooms()
    areas = db.get_all_areas()
    if request.method == "POST":
        # print(request.form.to_dict())
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
            string_area = ""
        else:
            area = request.form["area"].split(', ')
            area = {"city": area[0], "country": area[1]}
            string_area = area["city"] + ", " + area["country"]

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

        return render_template('room_list.html', rooms=list_of_rooms, areas=areas,
                               start_date=start_date,
                               end_date=end_date,
                               room_capacity=room_capacity,
                               area=string_area,
                               hotel_chain=hotel_chain,
                               hotel_stars=hotel_stars,
                               num_rooms_in_hotel=num_rooms_in_hotel,
                               price_of_room=price_of_room)
    return render_template('room_list.html', rooms=list_of_rooms, areas=areas)


@app.route('/book_room/<room_num>', methods=["GET", "POST"])
def book_room(room_num):
    room = db.get_room_from_num(room_num)
    availability_message = ""
    message_color = ""
    if request.method == "POST":
        room_num = room.room_num
        customer_id = session["current_cust_id"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        booking = Book(None, room_num, customer_id, start_date, end_date)
        room = db.get_room_from_num(room_num)

        # checks that booking does not start in the past
        if booking.starts_in_past():
            availability_message = "Cannot create booking that starts in the past"
            message_color = "red"

        # check that start is before end
        elif booking.start_date_before_end():
            availability_message = "End date cannot come before start date"
            message_color = "red"

        # checks that room is available
        elif not room.check_room_available(start_date, end_date):
            availability_message = "Room is unavailable for that time period"
            message_color = "red"

        else:
            booking.create_booking()
            availability_message = "Room successfully booked"
            message_color = "green"

    unavailable_days = room.get_unavailable_days_for_room()

    today = datetime.datetime.today()
    today_date = today.strftime('%Y-%m-%d')
    tomorrow_date = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    return render_template('book_room.html', room=room, unavailable_days=unavailable_days,
                           availability_message=availability_message, message_color=message_color,
                           today_date=today_date, tomorrow_date=tomorrow_date)


@app.route('/customer_view_rooms')
def customer_view_rooms():
    # check that user is customer
    customer = db.get_customer(session["current_cust_id"])
    rented_rooms = customer.get_rented_currently_rooms()
    booked_rooms = customer.get_currently_booked_rooms()
    return render_template('customers_rooms.html', rented_rooms=rented_rooms, booked_rooms=booked_rooms)


@app.route('/customer_account', methods=["GET", "POST"])
def customer_account():
    customer_id = session["current_cust_id"]
    customer = db.get_customer(customer_id)
    if request.method == "POST":
        customer.password = request.form["password"]
        # customer.hotel_id = request.form["hotel_id"]
        customer.SIN = request.form["SIN"]
        customer.first_name = request.form["first_name"]
        customer.last_name = request.form["last_name"]
        customer.street = request.form["street"]
        customer.city = request.form["city"]
        customer.postal_code = request.form["postal_code"]
        customer.country = request.form["country"]
        # customer.registration_date = request.form["registration_date"]
        customer.update()
        return redirect(url_for("customer_account"))

    return render_template('customer_details.html', customer=customer)


@app.route('/delete_account')
def delete_account():
    if session["cust_or_emp"] == "employee":
        employee_id = session["current_emp_id"]
        db.delete_employee(employee_id)
    if session["cust_or_emp"] == "customer":
        customer_id = session["current_cust_id"]
        db.delete_customer(customer_id)

    return redirect(url_for("welcome"))


# EMPLOYEE STUFF

@app.route('/rent_room', methods=["GET", "POST"])
def rent_room():
    list_of_rooms = []
    return render_template('room_list.html', rooms=list_of_rooms)


@app.route('/employee_account', methods=["GET", "POST"])
def employee_account():
    employee_id = session["current_emp_id"]
    employee = db.get_employee(employee_id)
    if request.method == "POST":
        employee.password = request.form["password"]
        employee.hotel_id = request.form["hotel_id"]
        employee.SIN = request.form["SIN"]
        employee.first_name = request.form["first_name"]
        employee.last_name = request.form["last_name"]
        employee.street = request.form["street"]
        employee.city = request.form["city"]
        employee.postal_code = request.form["postal_code"]
        employee.country = request.form["country"]
        employee.position = request.form["position"]
        employee.update()
        return redirect(url_for("employee_account"))

    return render_template('employee_details.html', employee=employee)


# MANAGER STUFF

@app.route('/edit_hotel/<hotel_id>', methods=["GET", "POST"])
def edit_hotel(hotel_id):    
    hotel = db.get_hotel(hotel_id)
    if request.method == "POST":
        hotel.hotel_name == request.form["hotel_name"]
        hotel.street = request.form["street"]
        hotel.city = request.form["city"]
        hotel.postal_code = request.form["postal_code"]
        hotel.country = request.form["country"]
        hotel.email = request.form["email"]
        hotel.phone_number = request.form["phone_number"]
        hotel.update()
        # return redirect(url_for("edit_hotel"))
    return render_template('edit_hotel.html', hotel = hotel)

@app.route('/delete_hotel/<int:hotel_id>')
def delete_hotel(hotel_id):
    db.delete_hotel(hotel_id)
    return redirect(url_for("rent_room")) #not really sure abt where to go after this

@app.route('/add_hotel',  methods=["GET", "POST"])
def add_hotel():
    create_success = False
    if request.method == "POST":
        chain_name = request.form["chain_name"]
        hotel_name = request.form["hotel_name"]
        star_num = request.form["star_num"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        street = request.form["street"]
        city = request.form["city"]
        postal_code = request.form["postal_code"]
        country = request.form["country"]
        
        hotel = Hotel(NULL, chain_name, hotel_name, star_num, street, city, postal_code, country, email, phone_number)
        create_success = hotel.create_hotel()

        if create_success:
            return redirect(url_for("add_hotel"))

    chains = db.get_chains()
    return render_template('add_hotel.html', chains=chains, create_success=create_success)


@app.route('/room_list')
def room_list():
    list_of_rooms = []
    return render_template('room_list.html', rooms=list_of_rooms)

@app.route('/hotel_list')
def hotel_list():
    chain_name = db.get_employee(session["current_emp_id"]).get_chain()
    list_of_hotels = db.get_hotels_from_chain(chain_name)
    return render_template('hotel_list.html', hotels=list_of_hotels)

@app.route('/hotel_search', methods=["GET", "POST"])
def hotel_search():
    employee = db.get_employee(session["current_emp_id"])
    chain_name = employee.get_chain()
    list_of_hotels = db.get_hotels_from_chain(chain_name)
    areas = db.get_all_areas()
    if request.method == "POST":
        if request.form["area"] == "":
                area = None
        else:
            area = request.form["area"].split(', ')
            area = {"city": area[0], "country": area[1]}
            string_area = area["city"] + ", " + area["country"]

        if request.form["hotel_stars"] == "none":
            hotel_stars = None
        else:
            hotel_stars = int(request.form["hotel_stars"])

        list_of_hotels = db.db_hotel_search(chain_name=chain_name, hotel_stars=hotel_stars, area=area)
        return render_template('hotel_list.html', hotels = list_of_hotels, areas = areas, area=area, chain_name=chain_name, hotel_stars=hotel_stars)
    return render_template("hotel_list.html", hotels = list_of_hotels, areas=areas)


@app.route('/edit_room')
def edit_room():
    return render_template('edit_room_info.html')

@app.route('/add_room')
def add_room():
    return render_template('add_room.html')


if __name__ == '__main__':
    app.run()
