#!/usr/bin/env python

import re, os, sys

f1 = open(os.argv[1],rb)
f2 = open(os.argv[2],wb)
call = re.compile('^call\s+(.*)')
preCall = "echo (options) something >> logfile"
postCall = "echo (options) out of something >> logfile"

for line in f1:
	if call.match(line):
		f2.write(preCall)
		f2.write(line)
		f2.write(postCall)
	else:
		f2.write(line)

f1.close()
f2.close()
