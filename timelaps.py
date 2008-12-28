#!/usr/bin/python
from datetime import *
from os import *

#elapsed = int(getenv("numsec"))
d = timedelta(seconds=int(getenv("numsec")))
print "%sd%sh%sm%ss" % (d.days, d.seconds // 3600, 
        (d.seconds % 3600) // 60, (d.seconds % 3600) % 60)

