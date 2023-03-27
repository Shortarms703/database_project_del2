import config

import sqlite3 as sl

from classes import *


def execute(sql, params=None, one=False):
    # conn = sl.connect(config.database)
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


def init_db():
    execute_file(config.schema_file)
    # uncomment when these arent empty:
    # execute_file(config.sample_data_file)
    # execute_file(config.sql_index_file)
    # execute_file(config.sql_views_file)

def db_room_search(start_date, end_date, room_capacity, area, hotel_chain, hotel_stars, num_rooms_in_hotel, price_of_room):
    no_selection = None  # to compare against parameters to know when there is no selection, might change to None in the future or be specific per parameter idk yet

    # don't want to use sql to get the specific rows since we need to sometimes ignore certain conditions when they do not have a selection
    # sql = f"SELECT Room.* FROM Room, Hotel WHERE capacity='{room_capacity}' AND Room.hotel_id = Hotel.hotel_id AND Hotel.chain_name = '{hotel_chain}' AND Hotel.star_num = '{hotel_stars}'"
    rooms = get_all_rooms()
    search_result = []
    
    for room in rooms:
        searched_for = True
        # TODO: check dates and area (same city and country?)
        if room_capacity != no_selection and room.capacity != room_capacity:
            searched_for = False
        if hotel_chain != no_selection and room.get_hotel().get_chain().name != hotel_chain:
            searched_for = False
        if hotel_stars != no_selection and room.get_hotel().star_num != hotel_stars:
            searched_for = False
        if num_rooms_in_hotel != no_selection and room.get_hotel().get_num_rooms() != num_rooms_in_hotel:
            searched_for = False
        if price_of_room != no_selection and room.price != price_of_room:
            searched_for = False

        if searched_for:
            search_result.append(room)
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


def get_hotel_from_create():
    sql = f"SELECT chain_name, hotel_name, hotel_id FROM Hotel, Chain WHERE Hotel.chain_name = Chain.name"
    chain_hotels = execute(sql)
    chain_hotel_list = []
    for chain_hotel in chain_hotels:
        chain_hotel_list.append([chain_hotel[0], chain_hotel[1], chain_hotel[2]])
    return chain_hotel_list
    print(chain_hotel_list)

def check_if_login_vaid_emp(name, passwrod):
    sql = f"select * from Employee where first_name = '{name}'and password = '{passwrod}'"
    row = execute(sql)
    if len(row) == 0:
        return False
    else:
        return row[0]["employee_ID"]




def check_if_login_vaid_cust(name, password):
    sql = f"select * from Customer where first_name = '{name}'and password = '{password}'"
    row = execute(sql)
    if len(row) == 0:
        return False
    else:

        return row[0]["customer_id"]










if __name__ == '__main__':
    rooms = db_room_search(start_date="", end_date="", room_capacity=2, area="", hotel_chain="test", hotel_stars=3,
                           num_rooms_in_hotel="", price_of_room="")

   # get_hotel()
    # print("searched rooms", rooms)
    # for x in rooms:
    #     print(x)
    #     hotel = x.get_hotel()
    #     print(hotel)
    #     print(hotel.get_rooms())
    pass
    # execute_file(config.schema_file)
    # chains = [row in execute("SELECT name, street, city, postal_code, country FROM Chain")]
    # for chain in chains:
    #     for i in range(1,9):
    #         hotel_name = f"Hotel {i}"
    #         star_num = i % 5 + 1
    #
    #         street_number = str(random.randint(1, 9999))
    #         street_name = random.choice(["Main", "Oak", "Maple", "Elm", "Cedar", "Pine", "Spruce", "Birch"])
    #         street_type = random.choice(["St", "Ave", "Blvd", "Rd", "Ln", "Dr"])
    #         street = f"{street_number} {street_name} {street_type}"
    #
    #         city = chain[2]
    #         postal_code = str(int(chain[3]) + i)
    #         country = chain[4]
    #         email = f"hotel{i}@{chain_name}.com"
    #         phone_number = f"{555 + (i // 3):03d}-{(i % 3) * 3 + 100:03d}"
    #         execute("INSERT INTO Hotel (chain_name, hotel_name, star_num, street, city, postal_code, country, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (chain_name, hotel_name, star_num, street, city, postal_code, country, email, phone_number))

