#!/usr/bin/env python

f=open('98503011.tek','r')
line=f.readline()
check=0
for i in line[9:41]:
    check=check+eval('0x'+i)
    checksum=hex(check)[2:]
    print checksum
