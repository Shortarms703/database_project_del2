import config

import sqlite3 as sl


def execute(sql, params=None):
    conn = sl.connect(config.database)
    with conn:
        if params:
            result = conn.execute(sql, params)
        else:
            result = conn.execute(sql)
        conn.commit()
    conn.close()
    return result


def execute_file(file):
    with open(file) as f:
        conn = sl.connect(config.database)
        conn.executescript(f.read())
        conn.commit()
        conn.close()


def init_db():
    execute_file(config.schema_file)
    # uncomment when these arent empty:
    # execute_file(config.sample_data_file)
    # execute_file(config.sql_index_file)
    # execute_file(config.sql_views_file)

def db_room_search(search, start_date, end_date, room_capacity, area, hotel_chain, hotel_stars, num_rooms_in_hotel, price_of_room):
    pass


if __name__ == '__main__':
    pass
    # execute_file(config.schema_file)
    # chains = [row in execute("SELECT name, street, city, postal_code, country FROM Chain")]
    # for chain in chains:
    #     for i in range(1,9):
    #         hotel_name = f"Hotel {i}"
    #         star_num = i % 5 + 1
    #
    #         street_number = str(random.randint(1, 9999))
    #         street_name = random.choice(["Main", "Oak", "Maple", "Elm", "Cedar", "Pine", "Spruce", "Birch"])
    #         street_type = random.choice(["St", "Ave", "Blvd", "Rd", "Ln", "Dr"])
    #         street = f"{street_number} {street_name} {street_type}"
    #
    #         city = chain[2]
    #         postal_code = str(int(chain[3]) + i)
    #         country = chain[4]
    #         email = f"hotel{i}@{chain_name}.com"
    #         phone_number = f"{555 + (i // 3):03d}-{(i % 3) * 3 + 100:03d}"
    #         execute("INSERT INTO Hotel (chain_name, hotel_name, star_num, street, city, postal_code, country, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (chain_name, hotel_name, star_num, street, city, postal_code, country, email, phone_number))

