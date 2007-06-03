#! /usr/bin/env python

# Adapts the first line of a .tek file for the Xilinx serial
# prom programmer to a new SE & Sn.
# The <sesn#> given as argument is inserted in the first line
# of the <inputfile>, with byte and word reversed notation,
# e.g. 98503011 -> 30115098.
# Then the checksum is re-calculated and appended.

"""
usage: sesn-in-tek.py [-v] [-o outputfile] inputfile sesn#

-v: verbose
-o: name for outputfile. Default is <sesn#>.tek
inputfile: fil to change first line in.
sesn#: HWCI SE & SN, e.g. 98503011
"""

import os
import sys  
import time
import getopt
import string
from fnmatch import fnmatch

verbose = 0 # 1 for -v

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(2)

def reorder(sesn):
    """
    Changes the notation of the SE & SN, so the positions of the
    high- and low bytes and words are reversed.
    Arg: aabbccdd
    Returns: ddccbbaa
    """
    ReorderedSESN=sesn[6:]+sesn[4:6]+sesn[2:4]+sesn[0:2]
    if verbose:
        print 'Original sesn#:   %s' % sesn
        print 'Re-ordered sesn#: %s' % ReorderedSESN
    return ReorderedSESN

def insertsesn(Line,ReorderedSESN):
    """
    Replaces old SESN with new, reordered SESN in the line.
    Args: code-line, reordered sesn from reorder().
    """
    if verbose:
        print 'Original 1st line: %s' % Line
    NewLine=Line[0:9]+ReorderedSESN+Line[17:41]
    return NewLine

def newchecksum(Line):
    """
    Calculates a new checksum for the 9th to the 41st digit in the line.
    Adds up all nibbles, truncades to 1 byte if neccesary.
    Arg: code-line with reordered sesn sequence from insertsesn()
    Returns: new code-line with calculated checksum appended.
    """
    check=0
    for i in Line[9:41]:
        check=check+eval('0x'+i)
        checksum=hex(check)[2:]
    NewLine=Line[:41]+checksum
    if verbose:
        print 'New checksum: 0x%s' % checksum
        print 'New 1st line:      %s' % NewLine
    return NewLine

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
    ReorderedLine=insertsesn(TekFileLines[0],ReorderedSESN)
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
