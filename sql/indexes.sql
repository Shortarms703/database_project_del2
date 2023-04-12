-- unsure about indexes as we only just saw them in lecture recently
CREATE UNIQUE INDEX login
ON Employee (first_name, password);

CREATE INDEX hotel_area
ON Hotel(city, country);

CREATE INDEX price_idx
ON Room (price);