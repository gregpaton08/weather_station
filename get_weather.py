#!/usr/bin/env python

import urllib2
import json

def get_temperature():
    api_key = None
    with open('api_key.txt') as file:
        api_key = file.read()

    url = 'http://api.wunderground.com/api/' + api_key + '/conditions/q/NJ/Collingswood.json'

    response = urllib2.urlopen(url)
    weather_data = json.loads(response.read())
    temperature = weather_data['current_observation']['temp_f']

    return temperature

if __name__ == '__main__':
    print(get_temperature())