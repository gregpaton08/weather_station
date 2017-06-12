#!flask/bin/python

import sqlite3
import time
import thermometer

conn = sqlite3.connect('test.db')

time = int(round(time.time(), 0))
temperature = int(thermometer.read_temp_c() * 100)
sqlite_command = 'INSERT INTO INDOOR_TEMPERATURE (TIME, TEMPERATURE) VALUES ({0}, {1});'.format(time, temperature)
print(sqlite_command)
conn.execute(sqlite_command)
conn.commit()

cursor = conn.execute('SELECT * FROM INDOOR_TEMPERATURE')
for row in cursor:
    print(row)

conn.close()