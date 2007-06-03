#! /usr/bin/env python

import os
import sys  
import time
import getopt
import string
import re
from fnmatch import fnmatch

verbose = 0 # 1 for -v

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(1)


# Main program: parse command line and start processing
def main():
    global verbose
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:v')
    except getopt.error, msg:
        usage(msg)
    outputfile = ''
    
    if not args: usage('args missing')
    inputfile = args[0]
    sesn = args[1]
    if len(sesn) != 8:
        usage("sesn must be 8 figures")

    for i in sesn:
        if not re.match('\d' ,i):
            usage("sesn must be only figures")

    for o, a in opts:
        if o == '-o':
            outputfile = a
        else:
            outputfile=sesn+'.tek'
        if o == '-v': verbose = 1
        if args[2:]: usage('too many arguments')

    if verbose:
        print 'Reading .tek file: %s...' % `inputfile`
    try:
        f = file(inputfile, "r")
    except IOError, msg:
        usage("can't open %s\n %s" % (repr(inputfile), str(msg)))
    TekFileLines = f.readlines()
    f.close()

    ReorderedSESN=reorder(sesn)
    ReorderedLine=insertsesn(TekFileLines[0].strip(),ReorderedSESN)
    NewLine=newchecksum(ReorderedLine)+"\n"
    
    if verbose:
        print 'Writing Outputfile: %s...' % `outputfile`
    try:
        f = open(outputfile, "w")
    except IOError, msg:
        usage("can't open %s\n %s" % (repr(outputfile), str(msg)))
    f.write(NewLine)
    for line in TekFileLines[1:]:
        f.write(line)
    f.close()

if __name__ == '__main__':
    main()
