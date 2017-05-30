#!/usr/bin/env python

import pickle

api_cache_file = 'apicache.p'


def save_cache_data(key, data):
    cache_data = pickle.load(open(api_cache_file, 'rb'))
    if not cache_data:
        cache_data = {}
    cache_data[key] = data
    pickle.dump(cache_data, open(api_cache_file, 'wb'))


def get_cache_data(key):
    cache_data = pickle.load(open(api_cache_file, 'rb'))
    if not cache_data:
        cache_data = {}
    return cache_data.get(key, None)