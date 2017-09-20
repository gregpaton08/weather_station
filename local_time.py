#!/usr/bin/env python

import datetime
import pytz


def get_est_time():
    return datetime.datetime.now(pytz.timezone('US/Eastern'))