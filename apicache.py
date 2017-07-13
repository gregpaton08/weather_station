#!/usr/bin/env python

import pickle
import os
import datetime

'''
Module to cache the data received from the Weather Underground API. Since the API calls are limited to 500/day the number of calls must be throttled. So, the data is cached and update periodically.
'''

api_cache_file = 'apicache.p'


def __load_cache_data():
    cache_data = None
    if os.path.isfile(api_cache_file):
        cache_data = pickle.load(open(api_cache_file, 'rb'))
    if not cache_data:
        cache_data = {}
    return cache_data


def save_cache_data(key, data):
    cache_data = __load_cache_data()
    cache_data[key] = {
        'data' : data,
        'time' : datetime.datetime.now()
    }
    pickle.dump(cache_data, open(api_cache_file, 'wb'))


# Return the cached data if it is less than 10 minutes old. Limited to 500 API calls per day (one per 2.88 minutes).
def get_cache_data(key, within_last_num_seconds=600):
    cache_data = __load_cache_data()
    if not cache_data.get(key, None):
        return None
    time = cache_data[key].get('time', None)
    time_diff = (datetime.datetime.now() - time).seconds
    if time_diff > within_last_num_seconds:
        return None
    return cache_data[key].get('data', None)