#! /usr/bin/env python

import os
import sys  
import string
import re

# Main program: parse command line and start processing
def main():
    inputfile = sys.argv[1]
    Trusted = '192.168.2.1'
    SourceAddress=[]
    UniqList=[]

    f = file(inputfile, "r")
    LogLines = f.readlines()
    f.close()
    
    for line in LogLines:
        match=re.match('.*SRC=(\d+\.\d+\.\d+\.\d+).*DST=192\.168\.2\.1.*PROTO=(TCP|UDP)',line)
        if match:
            SourceAddress.append(match.group(1))
            
    for Address in SourceAddress:
        if Address != Trusted:
            try:
                if UniqList.count(Address) == 0:
                    UniqList.append(Address)
            except ValueError:
                break

    for line in UniqList:
        print line

if __name__ == '__main__':
    main()
