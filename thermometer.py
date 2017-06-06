#!/usr/bin/env python

import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-000004abf982/w1_slave'

def __read_sensor():
    with open(temp_sensor, 'r') as file:
        lines = file.readlines()
    return lines


def read_temp_c():
    if not os.path.isfile(temp_sensor):
        return -200.0

    data = __read_sensor()
    while 'YES' not in data[0]:
        time.sleep(0.2)
        data = read_sensor()
    temperature = data[1][data[1].find('=') + 1:]
    temperature = float(temperature) / 1000.0
    return temperature


def read_temp_f():
    return convert_celsius_to_fahrenheit(read_temp_c())


def convert_celsius_to_fahrenheit(celsius):
    return celsius * 9.0 / 5.0 + 32.0


if __name__ == '__main__':
    temperature = read_temp()
    print(temperature)
    print(convert_celsius_to_fahrenheit(temperature))