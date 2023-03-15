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
    return result


def execute_file(file):
    with open(file) as f:
        conn = sl.connect(config.database)
        conn.executescript(f.read())
        conn.commit()
        conn.close()


def init_db():
    execute_file(config.schema_file)
    execute_file(config.sample_data_file)
    execute_file(config.sql_index_file)
    execute_file(config.sql_views_file)

if __name__ == '__main__':
    execute_file(config.schema_file)