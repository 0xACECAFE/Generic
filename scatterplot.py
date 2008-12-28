#! /usr/bin/env python
#
'''
Usage:

'''
import os
import sys
import csv
import re
from time import *
from pylab import *

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(1)


def main():
    '''
    main() handles the arguments to the script and calls the the other functions with
    arguments from the command line if they are supplied, or calls the UserInput function first
    if no argument are supplied.
    Arguments: none
    Returns: none
    '''
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:h')
    except getopt.error, msg:
        usage(msg)
    for o, a in opts:
        if o == '-h': usage()
        if o == '-o':
            option = a
    if args:
        arg = args[0]
    PipeIn = open('/home/theo/tmp/E4416A_data','r')
    s = 1
    XData = []
    YData = []
    scatter([0],[0],1)
    show()
    while PipeIn:
        DataLine = PipeIn.readline()
        XData.append(float(DataLine.split('\t')[0]))
        YData.append(float(DataLine.split('\t')[1]))
        #clf()
        scatter(XData,YData,len(XData))
        draw()
        sleep(10)
        #close()
    return

if __name__ == '__main__':
    main()
