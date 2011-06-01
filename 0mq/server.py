#!/usr/bin/python

import zmq
import time
from random import choice

def main():
    """ main method """

    context = zmq.Context(1)

    # Socket facing clients
    frontend = context.socket(zmq.SUB)
    frontend.bind("tcp://*:5000")
    frontend.setsockopt(zmq.SUBSCRIBE, '')

    # Socket facing services
    backend  = context.socket(zmq.PUB)
    backend.bind("tcp://*:5001")

    zmq.device(zmq.QUEUE, frontend, backend)

    # We never get here
    frontend.close()
    backend.close()
    context.term()


if __name__ == "__main__":
    main()