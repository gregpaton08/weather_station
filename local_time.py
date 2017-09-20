#!/usr/bin/env python

import datetime
import pytz


def get_est_time():
    return datetime.datetime.now(pytz.timezone('US/Eastern'))

def get_est_time_dict():
    current_time = get_est_time()
    return {
        'year' : current_time.year,
        'month' : current_time.month,
        'day' : current_time.day,
        'hour' : current_time.hour,
        'minute' : current_time.minute
    }