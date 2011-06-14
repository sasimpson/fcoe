from random import randrange
import pywhois
import re
import os
import csv
import sys

def get_bit():
    regex = re.compile(r'[a|e|i|o|u]')
    foo = False
    while(foo == False):
        blob = []
        bit = ''.join([chr(randrange(97, 122)) for x in range(randrange(2,4))])
        if regex.search(bit):
            foo = True
    return bit

def find_name():
    name = "%s%s.com" % (get_bit(), get_bit())
    t = os.popen('pywhois %s' % name).read()
    if re.compile('.*Available.*').search(t):
        return name
    else:
        return None
        
if __name__ == '__main__':
    nameWriter = csv.writer(open('names.csv', 'wb'))
    for x in range(100):
        print(".")
        if x%10 == 0:
            print(x)
        name = find_name()
        if name:
            # print name
            nameWriter.writerow([name])


