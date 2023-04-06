DROP VIEW IF EXISTS room_capacity_by_hotel;
DROP VIEW IF EXISTS hotel_count_by_area;

CREATE VIEW hotel_count_by_area AS
SELECT city, COUNT(*) hotel_count
FROM Hotel
GROUP BY city;

CREATE VIEW room_capacity_by_hotel AS
SELECT h.hotel_id, r.room_num, r.capacity
FROM Hotel h, Room r
WHERE h.hotel_id = r.hotel_id
-- I do not think this is the correct interpretation of the instructions (View 2: the second view is the capacity of all the rooms of a specific hotel)
-- not sure how meant to specify the specific hotel if parameters aren't allowed here.