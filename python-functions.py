# Decimal to binary
def dec2bin(x): return x and (dec2bin(x/2)+str(x%2)) or ''
