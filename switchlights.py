#!/usr/bin/python
# This redirects errors to the web browser.
# Normally stderr goes to the web server errors log, but
# this will cause the message to go to the user's browser.
import string, sys, cgi, cgitb; cgitb.enable()
from os import system

sys.stderr = sys.stdout

def InitCard():
    return system("/usr/local/bin/setrelays.sh -i")

def MakeCommand(sw, set2):
    return system("/usr/local/bin/setrelays.sh -r 1 -f "+sw+set2)

def GetParms():
    cgiParameters = cgi.FieldStorage()
    switch = cgiParameters.getlist("switch")[0]
    setto = cgiParameters.getlist("setto")[0]
    return switch, setto

try:
    import traceback
    sys.stderr = sys.stdout
    switch, setto = GetParms()
    print 'Content-type: text/html'
    print
    print "<html><head><title>Untitled</title></head><body>"
    #print switch, setto
    InitCard()
    MakeCommand(switch,setto)
    print "</body></html>"
        
except Exception, e:
    print 'Content-type: text/html'
    print
    print '<html><head><title>'
    print str(e)
    print '</title>'
    print '<meta name="ROBOTS" content="NOINDEX, NOFOLLOW">'
    print '</head><body>'
    print '<h1>TRACEBACK</h1>'
    print '<pre>'
    traceback.print_exc()
    print '</pre>'
    print '</body></html>'
