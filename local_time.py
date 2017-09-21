#!/usr/bin/env python

import datetime
import pytz


def datetime_to_dict(datetime_object):
    return {
        'year' : datetime_object.year,
        'month' : datetime_object.month,
        'day' : datetime_object.day,
        'hour' : datetime_object.hour,
        'minute' : datetime_object.minute
    }

def get_est_time():
    return datetime.datetime.now(pytz.timezone('US/Eastern'))

def get_est_time_dict():
    return datetime_to_dict(get_est_time())
