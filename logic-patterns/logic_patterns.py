#! /usr/bin/env python
#
# This program draws I and Q binary patterns for a given ASCII or HEX
# string and saves these in a png file.
#
import os
import sys
import Image,  ImageDraw, ImageFont

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
    # Make one long list of 1s and 0s from the complete string.
    for x in string:
        for bit in dec2bin(ord(x)).rjust(8,'0'):
            binrep.append(bit)
    # Put the even bits in the Ibits list and the even bits in the Qbits list.
    for bit in range(0, len(binrep), 2):
        Ibits.append(int(binrep[bit]))
        Qbits.append(int(binrep[bit+1]))
    return Ibits,  Qbits

def cnt_same_bits(bits, startbit):
    """
    Count the number of bits in a list of 0s and 1s, that do not change from the startbit to the next bit(s)
    """
    nrbits = 1
    # start between the 0th and the Nth (= startbit) bit in the bits list,
    endbit = startbit
    bitlevel = bits[startbit] # The startbit in the list is the level to compare with,
    for bit in range(startbit, len(bits) - 1):
        if bits[bit+1] == bitlevel:
            nrbits += 1
            endbit += 1
        else:
            break
    return nrbits, endbit,  bitlevel

def draw_bits(bits_draw, nrbits, startbit, bitlevel, Y_offset, horpix = 20,  vertpix=50):
    """
    Draw the rising edge, low- or high level and falling edge of a number of bits that remain the same.
    """
    def line(x1, y1, x2, y2):
        # 0,0 in draw.line is top-left
        # Y_offset + vertpix puts the bottom of the patterns on the right place.
        line_list = [x1, (Y_offset + vertpix - y1), x2, (Y_offset + vertpix - y2)]
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
    usage = "usage: %prog [-v|--verbose] [-x|--hex] \"<hexstring>\" [-a|--ascii] \"text\" [-g|--geometry] <horxver> [-G|--graph] <s|d|b> [-o|--output] <filename>"
    from optparse import OptionParser
    parser = OptionParser(usage=usage)
    parser.add_option('-a', '--ascii',
                                    dest = "asciiLine",
                                    help = "Input ascii string")
    parser.add_option('-x', '--hex',
                                    dest="hexLine",
                                    help = "Input hex string, e.g. 0xa5a5")
    parser.set_defaults(geom = '800x131',
                                    output_file = "DemultiplexedBits.png", 
                                    graph_type = 'd')
    parser.add_option('-G','--graph',
                                    dest = 'graph_type',
                                    help = 'Graph type: stream pattern (s), demultiplexed patterns (d) or both (b)')
    parser.add_option('-g','--geometry',
                                    dest = 'geom',
                                    help = 'Picture geometry, e.g. 100x50. Default = 800x131')
    parser.add_option('-v', '--verbose',
                                    action = "store_true",
                                    dest = "verbose",
                                    help = "Show some bits & bobs")
    parser.add_option('-o','--output',
                                    dest = 'output_file',
                                    help = 'Input filename for generated graphic. Default = DemultiplexedBits.png')
    (options,  args) = parser.parse_args()
    if  not (options.hexLine or options.asciiLine):
        parser.error("Either an ascii text line or a line in hex code is required")
    if options.graph_type not in ['s', 'd', 'b']:
        parser.error("Supply one of args s, d or b to  option -g")
    else:
        graph_type = options.graph_type
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
    pic_width = int(options.geom.split("x")[0])
    pic_height = int(options.geom.split("x")[1])
    if pic_width < 10 or pic_height < 10:
        parser.error("Please supply sensible values for the picture\'s geometry")
    bit_height = (pic_height - 30) // 2
    if options.verbose:
      print "Bit height: %s pixels" % bit_height
    output_file = options.output_file

    bit_width=pic_width//len(Ibits)
    bits_im = Image.new('L', (pic_width, pic_height), "lightgrey")
    bits_draw = ImageDraw.Draw(bits_im)

    startbit = 0
    while startbit < len(Qbits):
        nrbits, endbit, bitlevel = cnt_same_bits(Ibits, startbit)
        draw_bits(bits_draw, nrbits, startbit, bitlevel, 0, bit_width, bit_height) # Set the I data at the top
        startbit += nrbits

    startbit = 0
    while startbit < len(Qbits):
        nrbits, endbit, bitlevel = cnt_same_bits(Qbits, startbit)
        draw_bits(bits_draw, nrbits, startbit, bitlevel, (pic_height - bit_height - 1), bit_width, bit_height) # Set the Q data below the I data
        startbit += nrbits

    # Generate the clock ticks between the I and Q patterns. Offset the ticks half a bit.
    for bit in range(len(Ibits)+1):
        x1 = x2 = (bit * bit_width) - (bit_width / 2)
        y1 = (pic_height // 2) - (pic_height // 26)
        y2 = (pic_height // 2) + (pic_height // 26)
        line_list = [x1, y1, x2, y2]
        bits_draw.line(line_list)

    # Put the text in the drawing
    font = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSans.ttf",12)
    posX = pic_width - 10
    IposY = bit_height // 2
    QposY = pic_height - bit_height // 2
    bits_draw.text((posX,IposY), "I",font = font)
    #bits_draw.text((783,60), "Clk")
    bits_draw.text((posX,QposY), "Q",font = font)

    if options.verbose:
        bits_im.show()

    bits_im.save(output_file, 'PNG')
    return

if __name__ == '__main__':
    main()
