#!/usr/bin/python

import zmq
import sys
import time
from random import choice

def main(sport="soccer"):
    """docstring for main"""
    context = zmq.Context()

    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:5000")

    countries = ['netherlands','brazil','germany','portugal', 'united states', 'france']
    events = ['yellow card', 'red card', 'goal', 'corner', 'foul']

    while True:
        msg = "%(sport)s.%(country)s: %(sport)s %(country)s %(event)s" % {'sport': sport, 'country': choice( countries ), 'event': choice( events )}
        print("->" + msg)
        socket.send(msg)
        time.sleep(.5)
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()