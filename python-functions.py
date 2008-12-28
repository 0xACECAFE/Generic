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

def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    
    # Uses list comprehension which is a fractionally faster implementation than
    # the alternative, more readable, implementation below
    #   
    #    hex = []
    #    for aChar in byteStr:
    #        hex.append( "%02X " % ord( aChar ) )
    #
    #    return ''.join( hex ).strip()        

    return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

# Decimal to binary
def dec2bin(x): return x and (dec2bin(x/2)+str(x%2)) or ''

a = range(256)

for i in xrange(0, 256, 16):
	print ' '.join('%02x' % n for n in a[i:i+16])


import gmpy
int('aaa',36)
13330

for n in xrange(13330,13330+1000):
	print gmpy.digits(n,36),

aaa aab aac aad aae aaf aag aah aai aaj aak aal
aam aan aao aap aaq aar aas aat aau aav aaw aax
aay aaz ab0 ab1 ab2 ab3 ab4 ab5 ab6 ab7 ab8 ab9
aba abb abc abd abe abf abg abh abi abj abk abl
abm abn abo abp abq abr abs abt abu abv abw abx
aby abz ac0 ac1 ac2 ac3 ac4 ac5 ac6 ac7 ac8 ac9

#Python 2.3+
import datetime
d = datetime.date.today()
d.isoformat()
'2007-06-15'

#Python -2.3
import time
time.strftime( "%Y-%m-%d" )
'2007-06-15'

countries = ["india","africa","atlanta","artica","nigeria"]
filtered = filter(lambda item: item.startswith('a'), l)


import struct

def f2b(f):
    return struct.unpack('I',struct.pack('f',f))[0]

def b2f(b):
    return struct.unpack('f',struct.pack('I',b))[0]

>>> f2b(1.0)
1065353216
>>> hex(f2b(1.0))
'0x3f800000'
>>> b2f(0x3f800000)
1.0
>>> b2f(0x3f800001)
1.0000001192092896
>>> b2f(0x3f7fffff)
0.99999994039535522
