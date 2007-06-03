#! /usr/bin/env python

# Renumbers an AutoTest file with a user defined start linenumber
# and increment.
# When start linenumber is not defined, it defaults to 10.
# When increment is not defined, it defaults to 10.
#
"""
usage: at-renum.py [-v] [-o outputfile] [-s startline] [-i increment] inputfile

-v: verbose
-o filename: name for outputfile. Default is to overwrite the inputfile.
-s number: linenumber to start with.
-i number: number to increment with.
inputfile: .seq file to renumber.
"""

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
        opts, args = getopt.getopt(sys.argv[1:], 'vo:s:i:')
    except getopt.error, msg:
        usage(msg)
    if not args: usage('args missing')
    inputfile = args[0]
    outputfile = inputfile+'.renum'
    for o, a in opts:
        if o == '-o':
            outputfile = a
        if o == '-v': verbose = 1
        if o == '-s':
            startline = int(a)
#            for i in startline:
#                if not re.match('\d' ,i):
#                    usage("startline must be a number")
        else:
            startline = 10

        if o == '-i':
            increment = int(a)
#            for i in  increment:
#                if not re.match('\d' ,increment):
#                    usage("increment must be a number")
        else:
            increment = 10

    if args[1:]: usage('too many arguments')
    if verbose:
        print 'Reading AutoTest file: %s...' % `inputfile`
    try:
        f = file(inputfile, "r")
    except IOError, msg:
        usage("can't open %s\n %s" % (repr(inputfile), str(msg)))
    ATFile = f.readlines()
    f.close()
    # Main routine ends here
    ln = 0
    RefTable=[]
    NewLine=''
    CurrLine=startline
    for line in ATFile:
        ln = ln + 1
        if line.split()[1] == 'Gosub' or line.split()[1] == 'GotoLine':
            RefTable.append(line.split()[2])
            TmpLine = str(line.split()[0]) + ' **' + str(line.split()[1]) + ' ' + str(line.split()[2])
            line = TmpLine
        OldNum = line.split()[0]
        SaveLine = ln
        NewLine = str(CurrLine) + str(line.split()[1:])
        
        CurrLine = CurrLine + increment
        print NewLine
        
    if verbose:
        print 'Writing Outputfile: %s...' % `outputfile`
    try:
        f = open(outputfile, "w")
    except IOError, msg:
        usage("can't open %s\n %s" % (repr(outputfile), str(msg)))
    f.close()

if __name__ == '__main__':
    main()

