#!flask/bin/python

import sqlite3
import time
import thermometer


DATABASE_FILE_NAME = 'test.db'
INDOOR_TEMPERATURE_TABLE_NAME = 'INDOOR_TEMPERATURE'


def does_table_exist(connection, table_name):
    cursor = connection.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'{0}\';'.format(table_name))
    result = cursor.fetchone()
    return result is not None and table_name == result[0]


def get_newest_temperature():
    connection = sqlite3.connect(DATABASE_FILE_NAME)
    cursor = connection.execute('SELECT MAX(TIME), TEMPERATURE FROM {0};'.format(INDOOR_TEMPERATURE_TABLE_NAME))
    result = cursor.fetchone()
    connection.close()
    if result is not None:
        return result
    return [ -1, -1 ]


if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE_FILE_NAME)

    # time = int(round(time.time(), 0))
    # temperature = int(thermometer.read_temp_c() * 100)
    # sqlite_command = 'INSERT INTO {0} (TIME, TEMPERATURE) VALUES ({1}, {2});'.format(INDOOR_TEMPERATURE_TABLE_NAME, time, temperature)
    # print(sqlite_command)
    # conn.execute(sqlite_command)
    # conn.commit()

    # print does_table_exist(conn, INDOOR_TEMPERATURE_TABLE_NAME)
    print get_newest_temperature()

    # cursor = conn.execute('SELECT * FROM {0}'.format(INDOOR_TEMPERATURE_TABLE_NAME))
    # for row in cursor:
    #     print(row)

    conn.close()