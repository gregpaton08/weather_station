#!/usr/bin/env python

import urllib2
import json


def get_api_key():
    with open('api_key.txt') as file:
        return file.read()
    return ''


def get_temperature():
    url_path = '/conditions/q/NJ/Collingswood.json'
    url = 'http://api.wunderground.com/api/' + get_api_key() + url_path

    response = urllib2.urlopen(url)
    weather_data = json.loads(response.read())
    temperature = weather_data['current_observation']['temp_f']

    return temperature


def get_hourly_forecast(num_hours=-1):
    url_path = '/hourly/q/NJ/Collingswood.json'
    url = 'http://api.wunderground.com/api/' + get_api_key() + url_path

    response = urllib2.urlopen(url)
    weather_data = json.loads(response.read())

    return weather_data['hourly_forecast'][:num_hours]


if __name__ == '__main__':
    print(get_temperature())

    data = get_hourly_forecast()
    for item in data:
        print(item['FCTTIME']['hour'], item['temp']['english'], item['condition'])