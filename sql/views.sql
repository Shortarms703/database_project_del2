DROP VIEW IF EXISTS hotel_room_capacities;
DROP VIEW IF EXISTS hotel_count_by_area;

CREATE VIEW hotel_count_by_area AS
SELECT city, COUNT(*) hotel_count
FROM Hotel
GROUP BY city;

CREATE VIEW hotel_room_capacities AS
SELECT hotel_id, SUM(capacity) AS total_capacity
FROM Room
GROUP BY hotel_id;