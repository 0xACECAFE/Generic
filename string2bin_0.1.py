#! /usr/bin/env python
from pylab import *

def dec2bin(x):
    return x and (dec2bin(x/2)+str(x%2)) or ''

binrep = []
Ibits = []
Qbits = []
for x in 'ssbv':
    for bit in dec2bin(ord(x)).rjust(8,'0'):
        binrep.append(bit)
for bit in range(0, len(binrep), 2):
    Ibits.append(int(binrep[bit])+2)
    Qbits.append(int(binrep[bit+1]))
print Ibits
print Qbits

t = list(range( 16))
scatter(t, Ibits, linewidth=1.0)
scatter(t, Qbits, linewidth=1.0)
show()
