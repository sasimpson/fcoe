#!/usr/bin/python

import sys
from datetime import datetime, timedelta
import argparse

def is_queso_week(today=None):
    if today is None:
        today = datetime.now()
    #get beginning of the week (monday)
    bow = today - timedelta(today.weekday())
    #go back week by week until we get to the previous month's monday
    while(bow.month == today.month):
        bow = bow - timedelta(7)
    #go forward two weeks to get the second monday of the month
    valid_second_week = bow + timedelta(14)
    #does the requested date fit in this week?
    if today >= valid_second_week and today < (valid_second_week + timedelta(7)):
        return True
    else:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='store_true', help="show all days in the year that fall in queso week")
    args = parser.parse_args()
    today = datetime.now()
    if args.a:
        x = datetime(datetime.now().year, 1, 1)
        while(x.year == today.year):
            print "%s: %s" % (x.strftime("%b %d, %Y"), is_queso_week(x))
            x += timedelta(days=1)
    else:
        if is_queso_week(today):
            print "Yep!"
        else:
            print "Nope"
