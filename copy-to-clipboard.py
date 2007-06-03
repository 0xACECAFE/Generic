From keesdekoster@gmail.com Sun May 21 19:15:06 2006
Path: news.xs4all.nl!newsspool.news.xs4all.nl!transit3.news.xs4all.nl!newsgate.cistron.nl!news.glorb.com!postnews.google.com!y43g2000cwc.googlegroups.com!not-for-mail
Message-ID: <1148209491.376924.299530@y43g2000cwc.googlegroups.com>
From: "Kees de Koster" <keesdekoster@gmail.com>
Newsgroups: nl.comp.os.linux.programmeren
Subject: Re: Gnome - script output op het clipboard plaatsen
Date: 21 May 2006 04:04:51 -0700
References: <1147947205.674053.247220@u72g2000cwu.googlegroups.com>
Lines: 33
Organization: http://groups.google.com
NNTP-Posting-Host: 213.17.104.91
Mime-Version: 1.0
Content-Type: text/plain; charset="iso-8859-1"
X-Trace: posting.google.com 1148209497 25601 127.0.0.1 (21 May 2006 11:04:57 GMT)
X-Complaints-To: groups-abuse@google.com
NNTP-Posting-Date: Sun, 21 May 2006 11:04:57 +0000 (UTC)
User-Agent: G2/0.2
X-HTTP-UserAgent: Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.3) Gecko/20060425 SUSE/1.5.0.3-7 Firefox/1.5.0.3,gzip(gfe),gzip(gfe)
Complaints-To: groups-abuse@google.com
Injection-Info: y43g2000cwc.googlegroups.com; posting-host=213.17.104.91;
   posting-account=kNUgag0AAABcOr-m5GIxulvGSQSjG-xd
Xref: ferrets4me.xs4all.nl nl.comp.os.linux.programmeren:1815

>Heeft iemand enig idee hoe ik de output van een script op het clipboard
>kan plaatsen? Als ik het zo mag/kan noemen in gnome en danwel
>automatisch/redirect en niet met ctrl+c ;-)

Van Wouter Bolsterlee(http://uwstopia.nl/) , heb ik het ondertstaande
python scriptje gekregen waarmee ik de output van een bash script via
een pipe op het clipboard kan zetten.

$ signature | copy-to-clipboard

##########################################
#!/usr/bin/env python

import sys

import pygtk
pygtk.require('2.0')
import gtk

buffer = []
for line in sys.stdin:
    buffer.append(line)

c = gtk.Clipboard()
c.set_text(''.join(buffer))
c.store()
##########################################

Kees
--
"To err is human, to forgive, beyond the scope of the Operating System"
Linux Registered User #300181  |  ICQ #179658498  -- EOE


