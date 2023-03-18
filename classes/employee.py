class Employee:

    def __init__(self, SIN, first_name, last_name, hotel_id, password = None, employee_id = None, street = None, city = None, postal_code = None, country = None, position = None):
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