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


def read_temperature_c():
    if not os.path.isfile(temp_sensor):
        return -200.0

    data = __read_sensor()
    while 'YES' not in data[0]:
        time.sleep(0.2)
        data = read_sensor()
    temperature = data[1][data[1].find('=') + 1:]
    temperature = float(temperature) / 1000.0
    return temperature


def read_temperature_f():
    return __convert_celsius_to_fahrenheit(read_temperature_c())


def __convert_celsius_to_fahrenheit(celsius):
    return celsius * 9.0 / 5.0 + 32.0


if __name__ == '__main__':
    temperature = read_temperature_c()
    print(temperature)
    print(__convert_celsius_to_fahrenheit(temperature))