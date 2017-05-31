#!/usr/bin/env python

import urllib2
import json
import apicache


def get_api_key():
    with open('api_key.txt') as file:
        return file.read()
    return ''


def __get_data_for_url_path(url_path):
    cache_data = apicache.get_cache_data(url_path)
    if cache_data:
        return cache_data

    url = 'http://api.wunderground.com/api/' + get_api_key() + url_path

    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    apicache.save_cache_data(url_path, data)

    return data


def get_temperature():
    url_path = '/conditions/q/NJ/Collingswood.json'
    weather_data = __get_data_for_url_path(url_path)
    return weather_data['current_observation']['temp_f']


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