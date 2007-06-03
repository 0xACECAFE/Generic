#!/usr/bin/env python
"""
Programma om bitstreams naar een SE0993 LED board test opstelling te sturen,
zodat alle LEDs 1 keer worden aangezet.
Byte waarden 0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40 en 0x80 wordt achtereenvolgens
gestuurd naar byte offsets w, w-1, w-2 enz t/m 0, waarbij w de word-lengte van de
stream is.
De word-lengte is afhankelijk van het aantal 74HC595 registers, dat nodig is om
alle LEDS aan te sturen op een board variant.
"""

import os
import sys  
import time
import getopt
import string
import re

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(1)

def Nibble2Byte(nibble):
    if len(nibble) < 2:
        return '0' + `nibble`
    else:
        return `nibble`
    
NUM = 1
for byte in range(12,0,-1):
    for dummy in range(8,0,-1):
        NIBBLE=hex(NUM)[2:]
        print (14 - len(NIBBLE)) * '0' + NIBBLE
        NUM = NUM << 1
        print NUM
