#!/usr/bin/env python

import urllib2
import json
import apicache
import os

'''
Module to get weather data from the Weather Underground API.
'''


API_URL_LOCATION = 'NJ/Collingswood.json'


def get_api_key():
    key = os.environ.get('WU_API_KEY', None)
    if key:
        return key
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
    url_path = '/conditions/q/' + API_URL_LOCATION
    weather_data = __get_data_for_url_path(url_path)
    return weather_data.get('current_observation', {}).get(key, None)


def get_temperature_f():
    return __get_current_observation_for_key('temp_f')


def get_temperature_c():
    return __get_current_observation_for_key('temp_c')


def get_condition():
    return __get_current_observation_for_key('weather')


def get_hourly_forecast(num_hours=-1):
    url_path = '/hourly/q/' + API_URL_LOCATION
    weather_data = __get_data_for_url_path(url_path)
    return weather_data.get('hourly_forecast', [])[:num_hours]


def __get_astronomy_data():
    url_path = '/astronomy/q/' + API_URL_LOCATION
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
