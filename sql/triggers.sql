CREATE TRIGGER delete_rooms_trigger
AFTER DELETE ON Hotel
FOR EACH ROW
BEGIN
    DELETE FROM Room WHERE hotel_id = OLD.hotel_id;
END;

CREATE TRIGGER delete_room_booking_renting
AFTER DELETE ON ROOM
BEGIN  
    UPDATE Book SET room_num = NULL WHERE room_num = OLD.room_num;
    UPDATE Rent SET room_num = NULL WHERE room_num = OLD.room_num;
END;