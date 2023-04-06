-- unsure about indexes as we only just saw them in lecture recently
CREATE UNIQUE INDEX login
ON Employee (first_name, password);

CREATE UNIQUE INDEX rooms
ON Room (room_num);

CREATE INDEX price_idx
ON Room (price);