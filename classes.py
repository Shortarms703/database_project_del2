import datetime

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


class Chain(ExecutesSQL):

    def __init__(self, name=None, street=None, city=None, postal_code=None, country=None, email=None,
                 phone_number=None):
        self.name = name
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.email = email
        self.phone_number = phone_number


class Customer(ExecutesSQL):

    def __init__(self, customer_id, SIN, hotel_id, first_name, last_name, registration_date, street=None, city=None,
                 postal_code=None, country=None, password=None):
        self.customer_id = customer_id
        self.password = password
        self.hotel_id = hotel_id
        self.SIN = SIN
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.registration_date = registration_date

    def create_cust(self):
        sql = f" insert into Customer values (NULL, '{self.password}', '{self.hotel_id}', '{self.SIN}', '{self.first_name}', '{self.last_name}', " \
              f"'{self.street}', '{self.city}', '{self.postal_code}', '{self.country}', '{self.registration_date}')"
        self.execute(sql)

    def update(self):
        sql = f"UPDATE Customer SET password = '{self.password}', hotel_id = '{self.hotel_id}', SIN = '{self.SIN}', first_name = '{self.first_name}', last_name = '{self.last_name}', street = '{self.street}', city = '{self.city}', postal_code = '{self.postal_code}', country = '{self.country}', registration_date = '{self.registration_date}' WHERE customer_id='{self.customer_id}'"
        self.execute(sql)

    def get_currently_booked_rooms(self):
        sql = f"SELECT * FROM Book WHERE customer_id='{self.customer_id}' AND room_num IS NOT NULL"
        rows = self.execute(sql)
        booked_rooms = []
        for row in rows:
            booking = Book(row["book_id"], row["room_num"], row["customer_id"], row["start_date"], row["end_date"], row["active"])
            if not booking.ended() and booking.active:
                booked_rooms.append(booking)
        return booked_rooms

    def get_rented_currently_rooms(self):
        sql = f"SELECT * FROM Rent WHERE customer_id='{self.customer_id}' AND room_num IS NOT NULL"
        rows = self.execute(sql)
        rented_rooms = []
        for row in rows:
            rented = Rent(row["rent_id"], row["room_num"], row["customer_id"], row["start_date"], row["end_date"])
            if not rented.ended():
                rented_rooms.append(rented)
        return rented_rooms


class Employee(ExecutesSQL):

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

    def create_emp(self):
        sql = f" insert into Employee values (NULL, '{self.password}', '{self.hotel_id}', '{self.SIN}', '{self.first_name}', '{self.last_name}', '{self.street}', '{self.city}', '{self.postal_code}', '{self.country}', '{self.position}')"
        self.execute(sql)

    def update(self):
        sql = f"UPDATE Employee SET password = '{self.password}', hotel_id = '{self.hotel_id}', SIN = '{self.SIN}', first_name = '{self.first_name}', last_name = '{self.last_name}', street = '{self.street}', city = '{self.city}', postal_code = '{self.postal_code}', country = '{self.country}', position = '{self.position}' WHERE employee_id='{self.employee_id}'"

        self.execute(sql)

    def get_chain(self):
        sql = f"SELECT chain_name FROM Hotel WHERE hotel_id= '{self.hotel_id}'"
        result = self.execute(sql)
        chain_name = None
        if result:
            chain_name = result[0][0]
        return chain_name

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

    def create_hotel(self):
        sql = "INSERT INTO Hotel (chain_name, hotel_name, star_num, street, city, postal_code, country, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = (self.chain_name, self.hotel_name, self.star_num, self.street, self.city, self.postal_code, self.country, self.email, self.phone_number)
        self.execute(sql, values)

    def update(self):
        sql = f"UPDATE Hotel SET hotel_name = '{self.hotel_name}', star_num = '{self.star_num}', street = '{self.street}', city = '{self.city}', postal_code = '{self.postal_code}', country = '{self.country}', email = '{self.email}', phone_number = '{self.phone_number}' WHERE hotel_id='{self.hotel_id}'"
        self.execute(sql)

    def get_chain(self):
        # from classes.chain import Chain
        sql = f"SELECT * FROM Chain WHERE name = '{self.chain_name}'"
        row = self.execute(sql, one=True)
        if row:
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

    def get_num_rooms(self):
        num_rooms = len(self.get_rooms())
        return num_rooms


class Rent(ExecutesSQL):

    def __init__(self, rent_id, room_num, customer_id, start_date, end_date):
        self.book_id = rent_id
        self.room_num = room_num
        self.customer_id = customer_id
        self.start_date = start_date
        self.end_date = end_date

    def get_room(self):
        import db
        return db.get_room_from_num(self.room_num)

    def create_rental(self):
        sql = f"INSERT INTO Rent VALUES (NULL, '{self.room_num}', '{self.customer_id}', '{self.start_date}', '{self.end_date}')"
        self.execute(sql)

    def ended(self):
        today = datetime.datetime.today().date()
        end = datetime.datetime.strptime(self.end_date, '%Y-%m-%d').date()
        if end < today:
            return True
        else:
            return False

    def starts_in_past(self):
        today = datetime.datetime.today().date()
        start = datetime.datetime.strptime(self.start_date, '%Y-%m-%d').date()
        if start < today:
            return True
        else:
            return False

    def start_date_before_end(self):
        start = datetime.datetime.strptime(self.start_date, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(self.end_date, '%Y-%m-%d').date()
        if end < start:
            return True
        else:
            return False


class Book(ExecutesSQL):

    def __init__(self, book_id, room_num, customer_id, start_date, end_date, active=True):
        self.book_id = book_id
        self.room_num = room_num
        self.customer_id = customer_id
        self.start_date = start_date
        self.end_date = end_date
        self.active = active

    def get_room(self):
        import db
        return db.get_room_from_num(self.room_num)

    def create_booking(self):
        sql = f"INSERT INTO Book VALUES (NULL, '{self.room_num}', '{self.customer_id}', '{self.start_date}', '{self.end_date}', '{self.active}')"
        self.execute(sql)


    def starts_in_past(self):
        today = datetime.datetime.today().date()
        start = datetime.datetime.strptime(self.start_date, '%Y-%m-%d').date()
        if start < today:
            return True
        else:
            return False

    def start_date_before_end(self):
        start = datetime.datetime.strptime(self.start_date, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(self.end_date, '%Y-%m-%d').date()
        if end < start:
            return True
        else:
            return False

    def ended(self):
        today = datetime.datetime.today().date()
        end = datetime.datetime.strptime(self.end_date, '%Y-%m-%d').date()
        if end < today:
            return True
        else:
            return False

    def convert_to_rental(self):
        rental = Rent(self.book_id, self.room_num, self.customer_id, self.start_date, self.end_date)
        rental.create_rental()
        self.active = False
        sql = f"UPDATE Book SET active=False WHERE book_id='{self.book_id}'"
        self.execute(sql)


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

    def create_room(self):
        sql = f" insert into Room values (NULL, '{self.hotel_id}', '{self.price}', '{self.capacity}', '{self.view}', '{self.amenities}', " \
              f"'{self.problems}', '{self.extendable}')"
        self.execute(sql)

    def update(self):
        sql = f"UPDATE Room SET price = '{self.price}', capacity = '{self.capacity}', view = '{self.view}', amenities = '{self.amenities}', problems = '{self.problems}', extendable = '{self.extendable}' WHERE room_num='{self.room_num}'"
        self.execute(sql)

    def get_hotel(self) -> Hotel:
        sql = f"SELECT * FROM Hotel WHERE hotel_id = '{self.hotel_id}'"
        row = self.execute(sql, one=True)
        hotel = Hotel(row["hotel_id"], row["chain_name"], row["hotel_name"], row["star_num"], row["street"],
                      row["city"], row["postal_code"], row["country"], row["email"], row["phone_number"])
        return hotel

    def get_bookings(self) -> [Book]:
        sql = f"SELECT * FROM Book WHERE room_num='{self.room_num}'"
        rows = self.execute(sql)
        bookings = []
        for row in rows:
            booking = Book(row["book_id"], row["room_num"], row["customer_id"], row["start_date"], row["end_date"], row["active"])
            if booking.active:
                bookings.append(booking)
        return bookings

    def get_unavailable_days_for_room(self):
        sql = f"""SELECT start_date, end_date FROM Book WHERE room_num = '{self.room_num}' 
                  UNION 
                  SELECT start_date, end_date FROM Rent WHERE room_num = '{self.room_num}'"""
        return [{"start_date": x["start_date"], "end_date": x["end_date"]} for x in self.execute(sql)]

    def check_room_available(self, start_date, end_date):
        unavailable_intervals = self.get_unavailable_days_for_room()
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for interval in unavailable_intervals:
            other_start, other_end = interval.values()
            other_start = datetime.datetime.strptime(other_start, '%Y-%m-%d').date()
            other_end = datetime.datetime.strptime(other_end, '%Y-%m-%d').date()
            if start_date <= other_end and other_start <= end_date:
                return False
        return True


if __name__ == '__main__':
    pass
