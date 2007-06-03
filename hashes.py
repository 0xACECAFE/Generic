#! /usr/bin/env python

"""
usage: hashes.py <inputfile>
inputfile: file with dates and numbers
"""

import sys  
import getopt
import string

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(1)

# Main program: parse command line and start processing
def main():
    opts, args = getopt.getopt(sys.argv[1:], '')
    if not args: usage('args missing')
    inputfile=args[0]
    try:
        f = file(inputfile, "r")
    except IOError, msg:
        usage("can't open %s\n %s" % (repr(inputfile), str(msg)))
    DbReadLines = f.readlines()
    f.close()

    for line in DbReadLines:
    	print  line.strip()[:6],line.strip()[7],string.atoi(line.strip()[7])*'#'
if __name__ == '__main__':
    main()
