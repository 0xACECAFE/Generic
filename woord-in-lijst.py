import sys, bisect

f = file("postings.txt","r")
postinglijst = f.readlines()
f.close()
f = file("woordlijst.txt","r")
woordlijst = f.readlines()
f.close()

#for woord in postinglijst:
#    if woord in woordlijst:
#        print woord,

for woord in woordlijst:
    print postinglijst[bisect.bisect_left(postinglijst,woord)],
