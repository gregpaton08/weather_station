#!/usr/bin/env python

import sqlite3
import time
import thermometer
from datetime import datetime, timedelta
import os
from app import app
import time


IS_PRODUCTION = False
if 'PRODUCTION' in os.environ:
  IS_PRODUCTION = True


DATABASE_FILE_NAME = '/app/test.db' #if IS_PRODUCTION else os.path.join(app.root_path, 'test.db')
# DATABASE_FILE_NAME = '/app/app/test.db' if IS_PRODUCTION else os.path.join(app.root_path, 'test.db')
INDOOR_TEMPERATURE_TABLE_NAME = 'INDOOR_TEMPERATURE'


def __does_table_exist(connection, table_name):
    cursor = connection.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'{0}\';'.format(table_name))
    result = cursor.fetchone()
    return result is not None and table_name == result[0]


def __scale_temperature_for_database(temperature):
    return int(float(temperature) * 10 + 0.5)


def __scale_temperature_for_display(temperature):
    return temperature / 10.0


def __get_current_unix_time():
    return int((datetime.now() - datetime(1970, 1, 1)).total_seconds())


# Get the current time rounded to the nearest hour
def __get_current_hour_datetime():
    time = datetime.now()

    # compute the timezone offset
    offset = time.altzone if (time.localtime().tm_isdst== 1) else time.timezone
    # set timzeone to eastern standard time
    est_offset = 4
    offset = (offset / 60 / 60) - est_offset
    time = time + timedelta(hours=offset)

    if time.minute >= 30:
        time = time.replace(hour=(time.hour + 1) % 24)
    time = time.replace(minute=0, second=0, microsecond=0)
    return time


def __convert_datetime_to_unix_time(time):
    return int((time - datetime(1970, 1, 1)).total_seconds())


def get_newest_temperature(connection=None):
    need_to_close_connection = False
    if connection is None:
        connection = get_connection()
        need_to_close_connection = True

    result = None
    if __does_table_exist(connection, INDOOR_TEMPERATURE_TABLE_NAME):
        cursor = connection.execute('SELECT MAX(TIME), TEMPERATURE FROM {0};'.format(INDOOR_TEMPERATURE_TABLE_NAME))
        result = cursor.fetchone()

    if need_to_close_connection:
        connection.close()
    if result is not None:
        return float(result[1])
    return None


# Return past 13 hours of indoor temperature history
def get_temperature_history():
    history = []
    current_time = __get_current_hour_datetime()

    print('current time: {0}'.format(current_time))

    connection = get_connection()
    if not __does_table_exist(connection, INDOOR_TEMPERATURE_TABLE_NAME):
        connection.close()
        return []
    connection.close()

    for hour in range(-12, 1):
        time = current_time + timedelta(hours=hour)
        connection = get_connection()
        cursor = connection.execute('SELECT * FROM {0} order by abs({1} - time) asc limit 1;'.format(INDOOR_TEMPERATURE_TABLE_NAME, __convert_datetime_to_unix_time(time)))
        result = cursor.fetchone()
        history.append({ 'hour' : time.hour, 'temperature' : (int(result[2]) + 5) / 10 })
        connection.close()
    return history


def get_connection():
    try:
        open(DATABASE_FILE_NAME, 'r')
    except IOError:
        open(DATABASE_FILE_NAME, 'w')
    
    return sqlite3.connect(DATABASE_FILE_NAME)


def get_temperature_c(connection=None):
    print('get_temperature_c')
    need_to_close_connection = False
    if connection is None:
        connection = get_connection()
        need_to_close_connection = True

    db_result = get_newest_temperature(connection)
    if db_result is None:
        db_result = -1000

    if need_to_close_connection:
        connection.close()

    return __scale_temperature_for_display(db_result)


def store_temperature(temperature):
    connection = get_connection()
    cursor = connection.cursor()
    
    # Create the table if it does not exist.
    if not __does_table_exist(connection, INDOOR_TEMPERATURE_TABLE_NAME):
        cursor.execute(open('schema.sql', 'r').read())
        connection.commit()
    
    command = 'INSERT INTO {0} (TIME, TEMPERATURE) VALUES ({1}, {2})'.format(INDOOR_TEMPERATURE_TABLE_NAME, __get_current_unix_time(), __scale_temperature_for_database(temperature))
    cursor.execute(command)
        
    connection.commit()

    connection.close()


def store_current_temperature():
    store_temperature(thermometer.read_temperature_c())


def dump_database():
    connection = get_connection()
    cursor = connection.cursor()
    data = []
    for row in cursor.execute('SELECT * FROM {0}'.format(INDOOR_TEMPERATURE_TABLE_NAME)):
        data.append(row)
    connection.close()
    return data


if __name__ == '__main__':
#    store_current_temperature()

    print(DATABASE_FILE_NAME)


    connection = get_connection()
    cursor = connection.cursor()
    for row in cursor.execute('SELECT * FROM {0}'.format(INDOOR_TEMPERATURE_TABLE_NAME)):
        print(row)
    connection.close()

    # print get_temperature_c(get_connection())
    
#    conn = get_connection()

    # time = int(round(time.time(), 0))
    # temperature = 95
    # sqlite_command = 'INSERT INTO {0} (TIME, TEMPERATURE) VALUES ({1}, {2});'.format(INDOOR_TEMPERATURE_TABLE_NAME, time, temperature)
    # conn.execute(sqlite_command)
    # conn.commit()

    # print does_table_exist(conn, INDOOR_TEMPERATURE_TABLE_NAME)
#    print get_newest_temperature()

    # cursor = conn.execute('SELECT * FROM {0}'.format(INDOOR_TEMPERATURE_TABLE_NAME))
    # for row in cursor:
    #     print(row)

#    conn.close()