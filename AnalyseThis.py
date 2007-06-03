#! /usr/bin/env python
"""
This program parses a directory with TC_ALL_5200 txt files for errors, and outputs
the relevant bits from those files.
Usage: AnalyseThis.py dir [-o Outputfile]
Arguments: directory with files to be parsed
Options: -o Filename : Outputfile to save results to, otherwise stdout.
"""
import os
import sys
import getopt
import re
from glob import glob

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(1)

# Main program: parse command line and start processing
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:')
    except getopt.error, msg:
        usage(msg)

    outputfile = ''
    Output = []
    FailedTC = 0
    SepLine = '+'*120+'\n'

    if not args: usage('args missing')
    filedir = args[0]

    if os.path.exists(filedir):
        os.chdir(filedir)
        inputfiles = glob('./TC_ALL*.txt')
        for inputfile in inputfiles:
            try:
                f = file(inputfile, "r")
            except IOError, msg:
                usage("can't open %s\n %s" % (repr(inputfile), str(msg)))
            FileLines = f.readlines()
            f.close()

            line = len(FileLines) - 1
            while line > 0:
                if re.search('FAILED', FileLines[line]):
                    FailedTC = FailedTC + 1
                    Output.append(SepLine)
                    Output.append(FileLines[line])
                    while not re.search('TC End', FileLines[line]) and line >= 0:
                        line -= 1
                        Output.append(FileLines[line])
                    Output.append('\n')
                    Output.append(inputfile)
                    Output.append(SepLine)
                    Output.append('\n')
                    Output.append('\n')
                line -= 1
        Output.append('\n')
        Output.reverse()
        Output.append('\n')
        Output.append("Total TC fails: %d" % FailedTC)
        for line in Output:
            print line,
    else:
        print "No such path"

    for o, a in opts:
        if o == '-o':
            outputfile = a
            try:
                f = open(outputfile, "w")
            except IOError, msg:
                usage("can't open %s\n %s" % (repr(outputfile), str(msg)))
            for line in Output:
                f.write(line)
            f.close()
if __name__ == '__main__':
    main()
