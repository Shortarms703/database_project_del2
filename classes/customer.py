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

