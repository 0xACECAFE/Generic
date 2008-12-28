#!/usr/bin/env python
'''
This script computes a table of possible resistance values one can get from switching on -and off
resistors in a parallel network. The table is made for a Agilent 34980A with a Multiplexer module.
Usage:
GMFE_Thermistor_calc (<output filename>)
'''
import re
import csv
import os
import sys

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(1)


def bit_is_set(n, num): return (1 << n) & num != 0

def Decimal2Binary(dec_num):
        """ Return the binary representation of dec_num """
        if dec_num == 0: return '0'
        return (Decimal2Binary(dec_num >> 1) + str(dec_num % 2))

def Decimal2BinaryBits(dec_num, bits):
        res = Decimal2Binary(dec_num)[:bits].zfill(bits)
        return res

def calcRes(decs=1):
    '''
    calcRes calculates all the possible total resistances from the states of the relay switches
    Arguments: decs: number of decimals to round off the resulting resistance to. Default = 1
    Returns: resistorList (resistorvalue, "[relay1,relay2,..]")
    '''
    # dictionary of used resistors in switch network
    res  = {0:2,
            1:4,
            2:8,
            3:16.2,
            4:32.4,
            5:63.4,
            6:127,
            7:255,
            8:511,
            9:1020,
            10:2050,
            11:4120,
            12:8160,
            13:16400,
            14:32792,
            15:65600,
            16:131000,
            17:262100,
            18:523700,
            19:1048700}
    
    resistorList = list()
    for num in xrange(1,2**20):
            bits = Decimal2BinaryBits(num,22)
            resTot =    str(round(1/(
                                    (int(bits[21]) * 1/float(res[0]))
                                    + (int(bits[20]) * 1/float(res[1]))
                                    + (int(bits[19]) * 1/float(res[2]))
                                    + (int(bits[18]) * 1/float(res[3]))
                                    + (int(bits[17]) * 1/float(res[4]))
                                    + (int(bits[16]) * 1/float(res[5]))
                                    + (int(bits[15]) * 1/float(res[6]))
                                    + (int(bits[14]) * 1/float(res[7]))
                                    + (int(bits[13]) * 1/float(res[8]))
                                    + (int(bits[12]) * 1/float(res[9]))
                                    + (int(bits[11]) * 1/float(res[10]))
                                    + (int(bits[10]) * 1/float(res[11]))
                                    + (int(bits[9]) * 1/float(res[12]))
                                    + (int(bits[8]) * 1/float(res[13]))
                                    + (int(bits[7]) * 1/float(res[14]))
                                    + (int(bits[6]) * 1/float(res[15]))
                                    + (int(bits[5]) * 1/float(res[16]))
                                    + (int(bits[4]) * 1/float(res[17]))
                                    + (int(bits[3]) * 1/float(res[18]))
                                    + (int(bits[2]) * 1/float(res[19]))
                                    ),decs))
            channels= list()
            for bit in range(0,21):
                    if bit_is_set(bit,num):
                            channels.append((1001 + bit))
            resistorList.append([resTot,channels])
    return resistorList

def main():
    '''
    main() handles the arguments to the script and calls the the other functions with
    arguments from the command line if they are supplied, or calls the UserInput function first
    if no argument are supplied.
    Arguments: <filename of outputfile> (optional)
             -h help
    Returns: none
    '''
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h')
    except getopt.error, msg:
        usage(msg)
    for o, a in opts:
        if o == '-h': usage()
    if args:
        outputFile = args[0]
    else:
        outputFile = "ResistorTable.csv"
    return

    resistorFile = open(outputFile, "wb")
    writer = csv.writer(resistorFile, dialect = 'excel')
    calcRes
    writer.writerows(resistorList)
    resistorFile.close()

if __name__ == '__main__':
    main()
