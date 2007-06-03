#!/usr/bin/env python

from poplib import *
import re
server = POP3('pop.xs4all.nl')
server.user('chtvanw')
server.pass_('Ua_Lava!')

messages = server.stat()[0]
if messages > 0:
    for mail in range(messages):
        headers = server.top(mail+1,0)[1]
        for header in headers:
            if re.match("^From:.*",header):
                print re.match("^From:.*",header).group()
            if re.match("^Return-Path:.*",header):
                print re.match("^Return-Path:.*",header).group()
            if re.match("^Subject:.*",header):
                print re.match("^Subject:.*",header).group()
            if re.match("^Date:.*",header):
                print re.match("^Date:.*",header).group()
        print
else:
    print "Sorry, no messages"

