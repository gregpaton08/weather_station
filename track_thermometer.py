#!flask/bin/python

import sqlite3
import time
import thermometer


def does_table_exist(connection, table_name):
    cursor = connection.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'{0}\';'.format(table_name))
    result = cursor.fetchone()
    return result is not None and table_name == result[0]


if __name__ == '__main__':
    conn = sqlite3.connect('test.db')

    # time = int(round(time.time(), 0))
    # temperature = int(thermometer.read_temp_c() * 100)
    # sqlite_command = 'INSERT INTO INDOOR_TEMPERATURE (TIME, TEMPERATURE) VALUES ({0}, {1});'.format(time, temperature)
    # print(sqlite_command)
    # conn.execute(sqlite_command)
    # conn.commit()

    print does_table_exist(conn, 'INDOOR_TEMPERATURE')

    cursor = conn.execute('SELECT * FROM INDOOR_TEMPERATURE')
    for row in cursor:
        print(row)

    conn.close()