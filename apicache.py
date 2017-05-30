#!/usr/bin/env python

import pickle
import os

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
    cache_data[key] = data
    pickle.dump(cache_data, open(api_cache_file, 'wb'))


def get_cache_data(key):
    cache_data = __load_cache_data()
    return cache_data.get(key, None)