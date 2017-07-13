#!flask/bin/python

import sqlite3
import time


DATABASE_FILE_NAME = 'test.db'
INDOOR_TEMPERATURE_TABLE_NAME = 'INDOOR_TEMPERATURE'


def does_table_exist(connection, table_name):
    cursor = connection.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'{0}\';'.format(table_name))
    result = cursor.fetchone()
    return result is not None and table_name == result[0]


def get_newest_temperature(connection=None):
    need_to_close_connection = False
    if connection is None:
        connection = get_connection()
        need_to_close_connection = True

    result = None
    if does_table_exist(connection, INDOOR_TEMPERATURE_TABLE_NAME):
        cursor = connection.execute('SELECT MAX(TIME), TEMPERATURE FROM {0};'.format(INDOOR_TEMPERATURE_TABLE_NAME))
        result = cursor.fetchone()

    if need_to_close_connection:
        connection.close()
    if result is not None:
        return float(result[1])
    return None


def get_connection():
    return sqlite3.connect(DATABASE_FILE_NAME)


if __name__ == '__main__':
    conn = get_connection()

    # time = int(round(time.time(), 0))
    # temperature = 95
    # sqlite_command = 'INSERT INTO {0} (TIME, TEMPERATURE) VALUES ({1}, {2});'.format(INDOOR_TEMPERATURE_TABLE_NAME, time, temperature)
    # conn.execute(sqlite_command)
    # conn.commit()

    # print does_table_exist(conn, INDOOR_TEMPERATURE_TABLE_NAME)
    print get_newest_temperature()

    # cursor = conn.execute('SELECT * FROM {0}'.format(INDOOR_TEMPERATURE_TABLE_NAME))
    # for row in cursor:
    #     print(row)

    conn.close()