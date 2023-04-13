import random as random

from classes import *


def execute(sql, params=None, one=False):
    with sl.connect(config.database) as conn:
        conn.row_factory = sl.Row
        if params:
            result = conn.execute(sql, params)
        else:
            result = conn.execute(sql)
        if one:
            result = result.fetchone()
        else:
            result = result.fetchall()
        conn.commit()
    conn.close()
    return result


def execute_file(file):
    with open(file) as f:
        conn = sl.connect(config.database)
        conn.executescript(f.read())
        conn.commit()
        conn.close()


def setup():
    create_database = False
    try:
        rows = execute(f"SELECT name FROM sqlite_master WHERE type='table'")
        tables = ["Book", "Chain", "Customer", "Employee", "Hotel", "Rent", "Room"]
        for table in tables:
            if table not in [x["name"] for x in rows]:
                create_database = True
    except sl.Error as e:
        raise e

    if create_database:
        print("Creating the database and inserting sample data...")
        init_db()
        init_hotels()
        init_rooms()


def init_db():
    execute_file(config.schema_file)
    execute_file(config.sample_data_file)
    execute_file(config.sql_index_file)
    execute_file(config.trigger_file)
    execute_file(config.sql_views_file)


def init_hotels():
    chains = execute(
        "SELECT name, street, city, postal_code, country FROM Chain")
    for chain in chains:
        for i in range(1, 9):
            chain_name = chain[0]
            hotel_name = f"Hotel {i}"
            star_num = i % 5 + 1

            street_number = str(random.randint(1, 9999))
            street_name = random.choice(
                ["Main", "Oak", "Maple", "Elm", "Cedar", "Pine", "Spruce", "Birch"])
            street_type = random.choice(
                ["St", "Ave", "Blvd", "Rd", "Ln", "Dr"])
            street = f"{street_number} {street_name} {street_type}"

            city = random.choice(
                ["Los Angeles", "New York", "Chicago", "Seattle", "San Jose", "Austin", "Las Vegas", "Nashville", "Denver", "Detroit", "El Paso", "Memphis", "Sacramento", "Tulsa", "Omaha"])
            postal_code = str(int(chain[3]) + i)
            country = chain[4]
            email = f"hotel{i}@{chain_name}.com"
            phone_number = f"{555 + (i // 3):03d}-{(i % 3) * 3 + 100:03d}"
            execute(
                "INSERT INTO Hotel (chain_name, hotel_name, star_num, street, city, postal_code, country, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (chain_name, hotel_name, star_num, street, city, postal_code, country, email, phone_number))

            # hiring new manager for the hotel
            latest_hotel = get_hotels_from_chain(chain_name)[-1]
            hire_manager(latest_hotel.hotel_id)

def init_rooms():
    hotels = execute("SELECT hotel_id FROM Hotel")
    # unique_room_nums = random.sample(range(100, 999), 200)
    for hotel in hotels:
        for i in range(1, 6):
            # room_num = unique_room_nums.pop(0) # basically take hotel ID digit 1 and add to a random number
            price = float(random.randint(150, 700))
            capacity = i # wrote this explicitly just for clarity
            view = random.choice(["Sea", "Mountain"])
            amenities = ', '.join(random.choices(["Wifi", "Breakfast", "Pool", "Free Laundry"], weights=[10, 6, 4, 1], k=2))
            problems = ', '.join(random.choices(["None", "Leak", "Electrical", "Furniture Damage", "Window"], weights=[90, 3, 3, 2, 2], k=1))
            extendable = random.choices([True, False], weights=[20, 80], k=1)

            execute(
                "INSERT INTO Room (room_num, hotel_id, price, capacity, view, amenities, problems, extendable) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                (None, hotel[0], price, capacity, view, amenities, problems, extendable[0]))



def db_room_search(start_date=None, end_date=None, room_capacity=None, area=None, hotel_chain=None, hotel_stars=None, num_rooms_in_hotel=None,
                   price_of_room=None):
    no_selection = None  # to compare against parameters to know when there is no selection, might change to None in the future or be specific per parameter idk yet

    # don't want to use sql to get the specific rows since we need to sometimes ignore certain conditions when they do not have a selection
    # sql = f"SELECT Room.* FROM Room, Hotel WHERE capacity='{room_capacity}' AND Room.hotel_id = Hotel.hotel_id AND Hotel.chain_name = '{hotel_chain}' AND Hotel.star_num = '{hotel_stars}'"
    rooms = get_all_rooms()
    search_result = []

    for room in rooms:
        searched_for = True
        if start_date != no_selection and not room.check_room_available(start_date, datetime.datetime.max.strftime('%Y-%m-%d')):
            searched_for = False
        if end_date != no_selection and not room.check_room_available(datetime.datetime.min.strftime('%Y-%m-%d'), end_date):
            searched_for = False
        if area != no_selection and (room.get_hotel().city != area["city"] or room.get_hotel().country != area["country"]):
            searched_for = False
        if room_capacity != no_selection and room.capacity != room_capacity:
            searched_for = False
        if hotel_chain != no_selection and room.get_hotel().get_chain().name != hotel_chain:
            searched_for = False
        if hotel_stars != no_selection and room.get_hotel().star_num != hotel_stars:
            searched_for = False
        if num_rooms_in_hotel != no_selection and room.get_hotel().get_num_rooms() != num_rooms_in_hotel:
            searched_for = False
        if price_of_room != no_selection and room.price > price_of_room:
            searched_for = False

        if searched_for:
            search_result.append(room)
    return search_result


def db_hotel_search(chain_name = None, hotel_stars=None, area=None):
    no_selection = None
    search_result = []
    if chain_name == no_selection:
        return search_result
        
    hotels = get_hotels_from_chain(chain_name)
    for hotel in hotels:
        searched_for = True
        if hotel_stars != no_selection and hotel.star_num != hotel_stars:
            searched_for = False
        if area != no_selection and (hotel.city != area["city"] or hotel.country != area["country"]):
            searched_for = False
        if searched_for:
            search_result.append(hotel)
    return search_result

def get_all_rooms():
    sql = f"SELECT * FROM Room"
    rows = execute(sql)
    rooms = []
    for row in rows:
        room = Room(row["room_num"], row["hotel_id"], row["price"], row["capacity"], row["view"], row["amenities"],
                    row["problems"], row["extendable"])
        rooms.append(room)
    return rooms

def get_hotels_from_chain(chain_name):
    sql = f"SELECT * FROM Hotel WHERE chain_name ='{chain_name}'"
    rows = execute(sql)
    hotels = []
    for row in rows:
        hotel = Hotel(row["hotel_id"], row["chain_name"], row["hotel_name"], row["star_num"], row["street"], row["city"], row["postal_code"], row["country"], row["email"], row["phone_number"],)
        hotels.append(hotel)
    return hotels

def get_hotel_from_create():
    sql = f"SELECT chain_name, hotel_name, hotel_id FROM Hotel, Chain WHERE Hotel.chain_name = Chain.name"
    chain_hotels = execute(sql)
    chain_hotel_list = []
    for chain_hotel in chain_hotels:
        chain_hotel_list.append(
            [chain_hotel[0], chain_hotel[1], chain_hotel[2]])
    return chain_hotel_list

def get_chains():
    sql = "SELECT name FROM Chain"
    chains = execute(sql)
    chain_list = []
    for chain in chains:
        chain_list.append(chain["name"])
    return chain_list

def get_room_from_num(room_num):
    sql = f"SELECT * FROM Room WHERE room_num = '{room_num}'"
    rows = execute(sql)
    if rows:
        row = rows[0]
        room = Room(row["room_num"], row["hotel_id"], row["price"], row["capacity"],
                    row["view"], row["amenities"], row["problems"], row["extendable"])
        return room
    else:
        return False


def check_if_login_valid_emp(name, password):
    sql = f"select * from Employee where first_name = '{name}'and password = '{password}'"
    row = execute(sql)
    if len(row) == 0:
        return False
    else:
        return row[0]["employee_ID"]


def check_if_login_valid_cust(name, password):
    sql = f"select * from Customer where first_name = '{name}'and password = '{password}'"
    row = execute(sql)
    if len(row) == 0:
        return False
    else:
        return row[0]["customer_id"]


def get_customer(customer_id):
    sql = f"SELECT * FROM Customer WHERE customer_id='{customer_id}'"
    rows = execute(sql)
    if rows:
        row = rows[0]
        customer = Customer(row["customer_id"], row["SIN"], row["hotel_id"], row["first_name"],
                            row["last_name"], row["registration_date"], row["street"], row["city"], row["postal_code"],
                            row["country"], row["password"])
        return customer
    else:
        return False

def get_customer_from_name(first_name, last_name):
    sql = f"SELECT * FROM Customer WHERE first_name='{first_name}' AND last_name='{last_name}'"
    rows = execute(sql)
    if len(rows) == 1:
        row = rows[0]
        customer = get_customer(row["customer_id"])
        return customer
    else:
        return False

def get_employee(employee_ID):
    sql = f"SELECT * FROM Employee WHERE employee_id='{employee_ID}'"
    rows = execute(sql)
    if rows:
        row = rows[0]
        employee = Employee(row["SIN"], row["first_name"], row["last_name"], row["hotel_id"], row["password"], row["employee_id"], row["street"], row["city"], row["postal_code"], row["country"],  row["position"])
        return employee
    else:
        return False

def get_hotel(hotel_id):
    sql = f"SELECT * FROM Hotel WHERE hotel_id='{hotel_id}'"
    rows = execute(sql)
    if rows:
        row = rows[0]
        hotel = Hotel(row["hotel_id"], row["chain_name"], row["hotel_name"], row["star_num"], row["street"], row["city"], row["postal_code"], row["country"], row["email"], row["phone_number"],)
        return hotel
    else:
        return False

def get_chain_from_employee(employee_id):
    sql = f"""
        SELECT h.chain_name
        FROM Hotel h
        JOIN (SELECT hotel_id FROM Employee WHERE employee_id = {employee_id}) as e
        ON h.hotel_id = e.hotel_id
    """
    result = execute(sql)
    if result:
        return result[0][0]
    return None

def delete_customer(customer_id):
    sql = f"DELETE FROM Customer WHERE customer_id='{customer_id}'"
    execute(sql)

def delete_employee(employee_id):
    sql = f"DELETE FROM Employee WHERE employee_id='{employee_id}'"
    execute(sql)

def delete_hotel(hotel_id):
    sql = f"DELETE FROM Hotel WHERE hotel_id='{hotel_id}'"
    execute(sql)

def delete_room(room_num):
    sql = f"DELETE FROM Room WHERE room_num='{room_num}'"
    execute(sql)

def get_all_areas():
    sql = f"SELECT city, country FROM Hotel"
    rows = execute(sql)
    areas = [f"{x['city']}, {x['country']}" for x in rows]

    unique_areas = []
    # remove duplicates from list areas
    for area in areas:
        if area not in unique_areas:
            unique_areas.append(area)

    return unique_areas


def hire_manager(hotel_id):
    # employee_ID
    hotel = get_hotel(hotel_id)
    chain = hotel.get_chain()
    password = random.randint(1000, 9999)
    SIN = random.randint(100000000, 999999999)
    first_name = random.choice(["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Jackson", "Isabella", "Aiden", "Mia", "Lucas", "Charlotte", "Mason", "Amelia", "Logan", "Harper", "Jacob", "Evelyn", "Elijah"])
    last_name = random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Perez", "Wilson", "Anderson", "Thomas", "Jackson", "White", "Harris"])
    street_number = str(random.randint(1, 9999))
    street_name = random.choice(
        ["Main", "Oak", "Maple", "Elm", "Cedar", "Pine", "Spruce", "Birch"])
    street_type = random.choice(
        ["St", "Ave", "Blvd", "Rd", "Ln", "Dr"])
    street = f"{street_number} {street_name} {street_type}"
    city = random.choice(
        ["Los Angeles", "New York", "Chicago", "Seattle", "San Jose", "Austin", "Las Vegas", "Nashville", "Denver",
         "Detroit", "El Paso", "Memphis", "Sacramento", "Tulsa", "Omaha"])
    postal_code = str(int(chain.postal_code) + random.randint(0, 9))
    country = chain.country
    position = "manager"
    employee = Employee(SIN, first_name, last_name, hotel_id, password, None, street, city, postal_code, country, position)
    employee.create_emp()


# FOR VIEWS
def get_capacities_view():
    sql = f"SELECT * FROM hotel_room_capacities"
    rows = execute(sql)
    capacities = [[f"{x[0]}", f"{x[1]}"] for x in rows]
    return capacities

def get_areas_view():
    sql = f"SELECT * FROM hotel_count_by_area"
    rows = execute(sql)
    return [[f"{x['city']}", f"{x['hotel_count']}"] for x in rows]

if __name__ == '__main__':
    init_db()
    init_hotels()
    init_rooms()
