#!/usr/bin/python

import zmq
import sys

def main(argv=None):
    
    if argv is None:
        argv = sys.argv
        
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    socket.connect("tcp://127.0.0.1:5001")

    if len(argv[1:]):
        for arg in argv[1:]:
            print("subscribing to %s" % arg)
            socket.setsockopt(zmq.SUBSCRIBE, arg)
    else:
        socket.setsockopt(zmq.SUBSCRIBE, "")

    while True:
        print  socket.recv()

if __name__ == "__main__":
    main()