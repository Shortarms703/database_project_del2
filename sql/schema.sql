DROP TABLE Chain;
DROP TABLE Employee;

CREATE TABLE Chain (
    name VARCHAR(50) PRIMARY KEY ,
    street VARCHAR(50),
    city VARCHAR(50),
    postal_code VARCHAR(50),
    country VARCHAR(50),
    email VARCHAR(50),
    phone_number VARCHAR(50)
);

CREATE TABLE Employee (
    employee_ID INTEGER PRIMARY KEY,
    name VARCHAR(50),
    password VARCHAR(50)
)