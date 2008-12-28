# Script to take readings from an Agilent E4416A Power Meter of an PETE NDMU

import os, sys, csv
#from visa import *
from time import *
from random import *
from datetime import *

ResultsTo = "TC4500-readings.csv"
ResultFile = open(ResultsTo, "wb")
writer = csv.writer(ResultFile, dialect = 'excel')

os.system("cls")
print "TC4500 NDMU Output Stability Test.\nTest results are written to: %s\n\n" % ResultsTo
ReadingTime = raw_input("Time as ddhhmmss please, leading zero values can be ommited\nHow long to test the NDMU (6 readings/minute).? ")
if len(ReadingTime) == 8:
    Days = int(ReadingTime[:2])
    Hours = int(ReadingTime[2:4])
    Minutes = int(ReadingTime[4:6])
    Seconds = int(ReadingTime[6:])
elif len(ReadingTime) == 6:
    Days = 0
    Hours = int(ReadingTime[:2])
    Minutes = int(ReadingTime[2:4])
    Seconds = int(ReadingTime[4:6])
elif len(ReadingTime) == 4:
    Days = 0
    Hours = 0
    Minutes = int(ReadingTime[:2])
    Seconds = int(ReadingTime[2:4])
else:
    Days = 0
    Hours = 0
    Minutes = 0
    Seconds = int(ReadingTime)
print "Running for %s days, %s hours, %s minutes, %s seconds" % (Days,Hours,Minutes,Seconds)
#PwrMtr = instrument("GPIB1::13::INSTR")
#PwrMtr.write("*RST")
#PwrMtr.write("CONF:POW:AC -30,0.01,(@1)")
#PwrMtr.write("AVER:COUNT 64")
#PwrMtr.write("SENS:FREQ:FIX 70MHz")
#sleep(5)

Now = datetime.now()
StartTestAt = mktime(Now.timetuple())
Interval = timedelta(seconds=Seconds, minutes=Minutes, hours=Hours, days=Days)
print "Interval: ", Interval
StopTestAt = mktime((Now + Interval).timetuple())
Readings = int((StopTestAt - StartTestAt)/10)
print; print "Taking %d samples\n\n" % Readings
#print time.time()
#print "Start Time: %s" % (StartTime)
for Reading in range(Readings):
   RelTimeOfSample = "%.5f" % clock()
   #SampleTime = time()
   #print "Sample Time: %s" % (SampleTime)
   #RelTimeOfSample = SampleTime - StartTime
   #PwrMtr.write("READ?")
   Sample = "%.3f" % (uniform(8.9,9.3))
   print "Sample %s, at %s seconds from start; Output power is: %s dBm" % (Reading+1, RelTimeOfSample, Sample)
   writer.writerow([RelTimeOfSample, Sample])
   ResultFile.flush()
   sleep(6.6)

ResultFile.close()
