#!/usr/bin/python

import string, sys, math

f=open('number.txt','r')

while 1:
    try:
        sNum = f.readline()
        if sNum == '':
            break
        iNum = int(sNum) 
        print '%9.1f' % iNum
    except IOError, (errno, strerror):
        print  "I/O error(%s): %s" % (errno, strerror)
