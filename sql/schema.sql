DROP TABLE Book;
DROP TABLE Chain;
DROP TABLE Hotel;
DROP TABLE Room;
DROP TABLE Customer;
DROP TABLE Employee;
DROP TABLE Rent;

CREATE TABLE Chain (
    name VARCHAR(50) PRIMARY KEY,
    street VARCHAR(50),
    city VARCHAR(50),
    postal_code VARCHAR(50),
    country VARCHAR(50),
    email VARCHAR(50),
    phone_number VARCHAR(50)
);

CREATE TABLE Hotel (
    hotel_id INTEGER PRIMARY KEY AUTOINCREMENT, -- unsure
    chain_name VARCHAR(50), -- can be null?
    hotel_name VARCHAR(50) NOT NULL,
    star_num TINYINT,
    street VARCHAR(50),
    city VARCHAR(50),
    postal_code VARCHAR(50),
    country VARCHAR(50),
    email VARCHAR(50),
    phone_number VARCHAR(50),
    FOREIGN KEY(chain_name) REFERENCES Chain(name)
);

CREATE TABLE Room (
    room_num SMALLINT PRIMARY KEY,
    hotel_id VARCHAR(50) NOT NULL,
    price NUMERIC(6, 2) NOT NULL,
    capacity TINYINT NOT NULL,
    view VARCHAR(50) NOT NULL,
    amenities VARCHAR(50),
    problems VARCHAR(50),
    extendable BOOLEAN NOT NULL,
    FOREIGN KEY(hotel_id) REFERENCES Hotel(hotel_id)
);

CREATE TABLE Customer(
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id VARCHAR(50),
    SIN VARCHAR(9) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    street VARCHAR(50),
    city VARCHAR(50),
    postal_code VARCHAR(50),
    country VARCHAR(50),
    registration_date DATE NOT NULL,
    FOREIGN KEY(hotel_id) REFERENCES Hotel(hotel_id)
);

CREATE TABLE Employee(
    employee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(50),
    hotel_id VARCHAR(50), -- can be null?
    SIN VARCHAR(9) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    street VARCHAR(50),
    city VARCHAR(50),
    postal_code VARCHAR(50),
    country VARCHAR(50),
    position VARCHAR(20), -- unsure
    FOREIGN KEY(hotel_id) REFERENCES Hotel(hotel_id)
);

CREATE TABLE Book(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_num SMALLINT NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY(room_num) REFERENCES Room(room_num),
    FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE Rent(
    rent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_num SMALLINT NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
	FOREIGN KEY(room_num) REFERENCES Room(room_num),
    FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
);
