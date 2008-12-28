#! /usr/bin/env python
#
#This program draws I and Q binary patterns for a given ASCII or HEX string and saves these in two png files.
#
import os
import sys
import Image,  ImageDraw

def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    bytes = []
    hexStr = ''.join( hexStr.split(" ") )
    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )
    return ''.join( bytes )

def demultiplex(string):
    """
    Tear a string apart in two lists, one for the even numbered bits (msb to lsb), i.e. the I bits,
    and one for the uneven numbered bits, i.e. the Q bits.
    """
    def dec2bin(x):
        return x and (dec2bin(x/2)+str(x%2)) or ''
    binrep = []
    Ibits = []
    Qbits = []
    for x in string:
        for bit in dec2bin(ord(x)).rjust(8,'0'):
            binrep.append(bit)
    for bit in range(0, len(binrep), 2):
        Ibits.append(int(binrep[bit]))
        Qbits.append(int(binrep[bit+1]))
    return Ibits,  Qbits

def cnt_same_bits(bits, startbit):
    """
    Count the number of bits in a list of 0s and 1s, that do not change from the startbit to the next bit(s)
    """
    nrbits = 1
    endbit = startbit
    bitlevel = bits[startbit]
    for bit in range(startbit, len(bits) - 1):
        if bits[bit+1] == bitlevel:
            nrbits += 1
            endbit += 1
        else:
            break
    return nrbits, endbit,  bitlevel

def draw_bits(bits_draw, nrbits, startbit, bitlevel, Y_offset, horpix = 20,  vertpix = 50):
    """
    Draw the rising edge, low- or high level and falling edge of a number of bits that remain the same.
    """
    def line(x1, y1, x2, y2):
        line_list = [x1, (Y_offset+ vertpix) - y1, x2, (Y_offset+ vertpix) - y2]
        bits_draw.line(line_list)
    y2 = vertpix if bitlevel == 1 else 0
    x_inc = nrbits * horpix
    x1 = startbit * horpix
    x2 = x1
    y1 = 0
    line(x1, y1, x2, y2)
    y1 = y2
    x1 = x2
    x2 = x2 + x_inc
    line(x1, y1, x2, y2)
    x1 = x2
    y2 = 0
    line(x1, y1, x2, y2)

def main():
    '''
    main() handles the arguments to the script and calls the the other functions with
    arguments from the command line if they are supplied, or calls the UserInput function first
    if no argument are supplied.
    Arguments: none
    Returns: none
    '''
    usage = "usage: %prog [-v|--verbose] [-x|--hex] \"<hexstring>\" [-a|--ascii] \"text\"\nOutput will be written to Ibits.png and Qbits.png"
    from optparse import OptionParser
    parser = OptionParser(usage=usage)
    parser.add_option('-x', '--hex',
                                    dest="hexLine", 
                                    help = "Input hex string, e.g. 0xa5a5")
    parser.add_option('-a', '--ascii', 
                                    dest = "asciiLine", 
                                    help = "Input ascii string")
    parser.add_option('-v', '--verbose',
                                    action = "store_true", 
                                    dest = "verbose", 
                                    default = "false", 
                                    help = "Show some bits & bobs")
    (options,  args) = parser.parse_args()
    if options.hexLine:
        hexStr = options.hexLine if options.hexLine[1].lower() != 'x' else options.hexLine[2:]
        string = HexToByte(hexStr)
    elif options.asciiLine:
        string = options.asciiLine
    if options.verbose:
        print "String as hexadecimal:\n%s" % (ByteToHex(string))
    Ibits,  Qbits = demultiplex(string)
    if options.verbose:
        print "I bits: %s" % Ibits
        print "Q bits: %s" % Qbits

    bit_width=800//len(Ibits)
    bits_im = Image.new('L', (800, 131), "lightgrey")
    bits_draw = ImageDraw.Draw(bits_im)
    
    startbit = 0
    while startbit < len(Qbits):
        nrbits, endbit, bitlevel = cnt_same_bits(Ibits, startbit)
        draw_bits(bits_draw, nrbits, startbit, bitlevel, 0, bit_width) # Set the I data at the top
        startbit += nrbits

    startbit = 0
    while startbit < len(Qbits):
        nrbits, endbit, bitlevel = cnt_same_bits(Qbits, startbit)
        draw_bits(bits_draw, nrbits, startbit, bitlevel, 80, bit_width) # Set the Q data below the I data
        startbit += nrbits

    # Generate the clock ticks between the I and Q patterns. Offset the ticks half a bit.
    for bit in range(len(Ibits)+1):
        x1 = x2 = (bit * bit_width) - (bit_width / 2)
        y1 = 60
        y2 = 70
        line_list = [x1, y1, x2, y2]
        bits_draw.line(line_list)

    # Put the text in the drawing
    bits_draw.text((790,25), "I")
    #bits_draw.text((783,60), "Clk")
    bits_draw.text((790,105), "Q")
    
    if options.verbose:
        bits_im.show()

    bits_im.save("DemultiplexedBits.png", 'PNG')
    return

if __name__ == '__main__':
    main()
