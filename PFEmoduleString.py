#! /usr/bin/env python

import sys  

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(1)

def toModulesString():
    modules = raw_input("Please input the modules-layout in the PFE (seen on the backpanel)\nfrom left to right as 1's and 0' :")
    modList = list(modules)
    modList.reverse()
    return hex(int(''.join(modList),2)), modList.count("1")

# Main program: parse command line and start processing
def main():
    modulesString, numModules = toModulesString()
    print "Modules String is: %s\nLimiters = %d\n" % (modulesString,numModules)
    
if __name__ == '__main__':
    main()
