#!/usr/bin/env python

import os
import time
import subprocess

temp_sensor = '/sys/bus/w1/devices/28-000004abf982/w1_slave'


def __load_drivers():
    output = subprocess.check_output('modprobe -c | grep w1_gpio -c', stderr=subprocess.STDOUT, shell=True)
    if int(output) == 0:
        os.system('modprobe w1-gpio')

    output = subprocess.check_output('modprobe -c | grep w1_therm -c', stderr=subprocess.STDOUT, shell=True)
    if int(output) == 0:
        os.system('modprobe w1-therm')


def __read_sensor():
    with open(temp_sensor, 'r') as file:
        lines = file.readlines()
    return lines


def read_temperature_c():
    if not os.path.isfile(temp_sensor):
        return -200.0

    __load_drivers()

    data = __read_sensor()
    while 'YES' not in data[0]:
        time.sleep(0.2)
        data = read_sensor()
    temperature = data[1][data[1].find('=') + 1:]
    temperature = float(temperature) / 1000.0
    return temperature


if __name__ == '__main__':
    temperature = read_temperature_c()
    print(temperature)
