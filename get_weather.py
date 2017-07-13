#!/usr/bin/env python

import urllib2
import json
import apicache

'''
Module to get weather data from the Weather Underground API.
'''


def get_api_key():
    with open('api_key.txt') as file:
        return file.read().strip()
    return ''


def __get_data_for_url_path(url_path):
    cache_data = apicache.get_cache_data(url_path)
    if cache_data is not None:
        return cache_data

    url = 'http://api.wunderground.com/api/' + get_api_key() + url_path

    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    apicache.save_cache_data(url_path, data)

    return data


def __get_current_observation_for_key(key):
    url_path = '/conditions/q/NJ/Collingswood.json'
    weather_data = __get_data_for_url_path(url_path)
    return weather_data.get('current_observation', {}).get(key, None)


def get_temperature_f():
    return __get_current_observation_for_key('temp_f')


def get_temperature_c():
    return __get_current_observation_for_key('temp_c')


def get_condition():
    return __get_current_observation_for_key('weather')


def get_hourly_forecast(num_hours=-1):
    url_path = '/hourly/q/NJ/Collingswood.json'
    weather_data = __get_data_for_url_path(url_path)
    return weather_data.get('hourly_forecast', [])[:num_hours]


def __get_astronomy_data():
    url_path = '/astronomy/q/NJ/Collingswood.json'
    return __get_data_for_url_path(url_path)


def get_sunrise():
    data = __get_astronomy_data();
    return data['sun_phase']['sunrise']


def get_sunset():
    data = __get_astronomy_data();
    return data['sun_phase']['sunset']


if __name__ == '__main__':
    print(get_temperature())

    data = get_hourly_forecast()
    for item in data:
        print(item['FCTTIME']['hour'], item['temp']['english'], item['condition'])
