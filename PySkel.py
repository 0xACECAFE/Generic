#! /usr/bin/env python
#
'''
Usage:

'''
import os
import sys
import csv
import time
import markup
from ConfigParser import *

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(1)

def testfunc(page):
    for i in 1,2,3:
        page.p("line %d of 3" % i)
        page.p('')
    time.sleep(3)
    footer = "Stop time: " + time.strftime('%x %X')
    return footer

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
    
    config = ConfigParser()
    config.readfp(open('/home/theo/Devel/Python/testpsu.ini'))
    title = config.get('results','Title')
    header = "Tested module type: " + config.get('dut','Model') + "\tSerial Number: " + config.get('dut','SN') + "\n"
    header = header + "Start time: " + time.strftime('%x %X')
    page = markup.page()
    footer = testfunc(page)
    page.init(title = title, header = header, footer = footer)
    #n = 3
    #result = "result 1 of %d" % n
    #page.p(result)
    print page
    return

if __name__ == '__main__':
    main()
