import config

import sqlite3 as sl


class ExecutesSQL:
    def execute(self, sql, params=None, one=False):
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

    def __repr__(self):
        return str(self.__dict__)

class Book:

    def __int__(self, book_id, room_num, customer_id, start_date, end_date):
        self.book_id = book_id
        self.room_num = room_num
        self.customer_id = customer_id
        self.start_date = start_date
        self.end_date = end_date

class Chain:

    def __init__(self, name = None, street = None, city = None, postal_code = None, country = None, email = None, phone_number = None):
        self.name = name
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.email = email
        self.phone_number = phone_number

class Customer:

    def __init__(self, customer_id, SIN, hotel_id, first_name, last_name, registration_date, street = None, city = None, postal_code = None, country = None, password = None):
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.SIN = SIN
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.registration_date = registration_date
        self.password = password

class Employee:

    def __init__(self, SIN, first_name, last_name, hotel_id, password=None, employee_id=None, street=None, city=None,
                 postal_code=None, country=None, position=None):
        self.employee_id = employee_id
        self.password = password
        self.hotel_id = hotel_id
        self.SIN = SIN
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.position = position

class Hotel(ExecutesSQL):

    def __init__(self, hotel_id, chain_name, hotel_name, star_num=None, street=None, city=None, postal_code=None,
                 country=None, email=None, phone_number=None):
        self.hotel_id = hotel_id
        self.chain_name = chain_name
        self.hotel_name = hotel_name
        self.star_num = star_num
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.email = email
        self.phone_number = phone_number

    def get_chain(self):
        # from classes.chain import Chain
        sql = f"SELECT * FROM Chain WHERE name = '{self.chain_name}'"
        row = self.execute(sql, one=True)
        chain = Chain(row["name"], row["street"], row["city"], row["postal_code"], row["country"], row["email"],
                      row["phone_number"])
        return chain

    def get_rooms(self):
        # from classes.room import Room
        sql = f"SELECT * FROM Room WHERE hotel_id = '{self.hotel_id}'"
        rows = self.execute(sql)
        rooms = []
        for row in rows:
            rooms.append(
                Room(row["room_num"], row["hotel_id"], row["price"], row["capacity"], row["view"], row["amenities"],
                     row["problems"], row["extendable"]))
        return rooms

class Rent:

    def __int__(self, rent_id, room_num, customer_id, start_date, end_date):
        self.book_id = rent_id
        self.room_num = room_num
        self.customer_id = customer_id
        self.start_date = start_date
        self.end_date = end_date

class Room(ExecutesSQL):

    def __init__(self, room_num, hotel_id, price, capacity, view, amenities, problems, extendable):
        self.room_num = room_num
        self.hotel_id = hotel_id
        self.price = price
        self.capacity = capacity
        self.view = view
        self.amenities = amenities
        self.problems = problems
        self.extendable = extendable

    def __repr__(self):
        return str(self.__dict__)

    def get_hotel(self) -> Hotel:
        sql = f"SELECT * FROM Hotel WHERE hotel_id = '{self.hotel_id}'"
        row = self.execute(sql, one=True)
        hotel = Hotel(row["hotel_id"], row["chain_name"], row["hotel_name"], row["star_num"], row["street"],
                      row["city"], row["postal_code"], row["country"], row["email"], row["phone_number"])
        return hotel


if __name__ == '__main__':
    pass