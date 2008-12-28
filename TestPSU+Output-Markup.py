#! /usr/bin/env python
# This program runs a test sequence with an Agilent 6060B electronic load, an Agilent 34980A
# Multiplexed Switchmatrix and a remote controlled SSR to test the on/off properties of a Schroff AC/DC
# convertor module.
# Sequence:
# 1. load off, module off
# 2. module on
# 3. Measure Output Voltage during 60 sec.; If the Output falls below 80% nominal: report and exit
#       otherwise continue.
# 4. Switch off load and module
# 5. Set load to 25% of max.
# 6. Switch on module and load
# 7. repeat steps 3 and 4
# 8. Set load to 50% of max
# 9. repeat steps 3 and 4
#10. Set load to 75% of max
#11. repeat steps 3 and 4
#12. Set load to 100% of max
#13. repeat steps 3 and 4

'''
Usage:
TestPSU.py [-o resultfile] [-h]
This script will look for a file called testpsu.cfg, in the same directory
as where the script runs from, and take test parameters from that file.
If an option -o plus argument is supplied on the command line, this will
be used for an alternate Results filename.
'''
import os
import sys
import csv
import markup
from visa import *
from time import *
from ConfigParser import *

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(1)

def cls():
        os.system("cls")
        return

def UserParams(config):
    cls()
    LocalList = []
    print "If no input is supplied, the data is gathered from the testpsu.ini file\n"

    Model = raw_input("What is the model-number of the device under test? ")
    if len(Model) > 0:
        LocalList.append(Model)
    else:
        Model = config.get('dut','Model')
        print "From config file: %s\n" % Model
        LocalList.append(Model)

    SerialNumber = raw_input("What is the serial number of the DUT? ")
    if len(SerialNumber) > 0:
        LocalList.append(SerialNumber)
    else:
        SerialNumber = config.get('dut','SN')
        print "From config file: %s\n" % SerialNumber
        LocalList.append(SerialNumber)

    Volt = raw_input("What is the Voltage output of the DUT? ")
    if len(Volt) > 0:
        LocalList.append(Volt)
    else:
        Volt = config.get('dut','Voltage')
        print "From config file: %s V\n" % Volt
        LocalList.append(Volt)

    MaxCur = raw_input("What is the maximum load of the DUT in Amperes? ")
    if len(MaxCur) > 0:
        LocalList.append(MaxCur)
    else:
        MaxCur = config.get('dut','Current')
        print "From config file: %s A\n" % MaxCur
        LocalList.append(MaxCur)

    Repeats = raw_input("How many times to repeat the sequence? ")
    if len(Repeats) > 0:
        LocalList.append(Repeats)
    else:
        Repeats = config.get('test','Repeats')
        print "From config file: %s repeats\n" % Repeats
        LocalList.append(Repeats)
    return LocalList

def PreTest(Loaded,Volt,ResPage):
    Failed = 0
    Volt = float(Volt)
    MinVolt = Volt - Volt/20
    MaxVolt = Volt + Volt/20
    test = {'loaded':'1','unloaded':'0'}[Loaded]
    ResPage.p("PSU module %s Pre-test\nTest criterium: %1.1f +/- %1.1f Volt" % (test,Volt,Volt/20))
    ResPage('')
    for n in range(10):
        HP34980.write("READ?")
        Voltage = float(HP34980.read())
        if Voltage < MinVolt or Voltage > MaxVolt:
            Res = "Pre-test %s Failed at step %d of 10. Output was %1.2f Volt" % (n,Voltage)
            print Res
            ResPage.p(Res)
            Failed = 1
            break
        sleep(1)
    if Failed != 0:
        return 1
    else:
        Res = "Pre-test Passed. Voltage: %1.3f Volt" % (Voltage)
        print Res
        ResPage.p(Res)
        ResPage.hr()
        ResPage.p('')
        return 0

def Measure(Test,RepeatTests,Volt,Load,Minutes,Readings,ResPage):
    ResPage.p("Start of measurement cycle %s of %s.\nTesting with a load of %s A.\nDuration: %s minutes\nTaking %s readings per minute.\n" % (Test,RepeatTests,Load,Minutes,Readings))
    ResPage.p('')
    Volt = float(Volt)
    MinVolt = Volt - Volt/20
    MaxVolt = Volt + Volt/20
    Failed = 0
    print "\nStarting Load test."
    print "This test will take %s minutes\n" % Minutes
    TotReadings = Minutes * Readings
    for Reading in range(TotReadings):
        print "Reading %s of %s" % (n,TotReadings)
        HP34980.write("READ?")
        HP6060.write("MEAS:CURR?")
        Current = float(HP6060.read()
        print "Current through Load: %1.3f A" % Current
        Voltage = float(HP34980.read())
        if Voltage < MinVolt or Voltage > MaxVolt:
            Res = "Test Failed at step %d of %d. Output was %1.3f Volt" % (n,Voltage,n,TotReadings)
            ResPage.p(Res)
            print Res
            Failed = 1
            break
        print "Measured: %1.3f Volt\n" % Voltage
        sleep(60/Readings)
        ResPage.p("Reading %d of %d.\tMeasured Current: %s A\tMeasured Voltage: %1.3f V" % (Reading,TotReadings,Current,Voltage))
    ResPage.hr()
    if Failed:
        return 1
    else:
        return 0

class Control:
    '''
    This class defines three methods:
    LOAD, for the Agilent 6060B Electronic Load.
        Parameters:
            State: <ON>/<OFF> Input state
            Current: string with Curreent setting.
    SSR, for the Solid State Switch attached to the Agilent 34980A MultiFunction Unit
        Parameters:
            Stat: <ON>/<OFF>
            PSUrly: designation on the 34921 Mux board for the SSR switch contacts.
    RST, to Reset the SSR and the Load to the OFF state.
    '''
    def LOAD(self,State,Current):
        LoadSCPI = "CURR " + str(Current)
        HP6060.write(LoadSCPI)
        LoadSCPI = "INPUT " + State
        HP6060.write(LoadSCPI)
        return

    def SSR(self,Stat,PSUrly):
      # Translate between logic and physical relay states.
        State = {'ON':'CLOSE','OFF':'OPEN'}[Stat]
        print "Switching the SSR %s" % Stat
        MuxSCPI = "ROUTE:" + State + " (@" + PSUrly + ")"
        HP34980.write(MuxSCPI)
        return

    def RST(self):
        HP6060.write("*RST")
        HP6060.write("*CLS")
        HP34980.write("*RST")
        HP34980.write("*CLS")
        return

def main():
    import getopt
    global HP34980, HP6060
    ResultFile = "PSUtestResults.html"
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:h')
    except getopt.error, msg:
        usage(msg)
    for o, a in opts:
        if o == '-h': usage()
        if o == '-o':
            ResultFile = a

    if args:
        arg = args[0]

    cls()
    print "This script will test a PSU (module) by switching the PSU on"
    print "and off, under loads ranging from 25% to 100% of the maximum"
    print "current that a typical module can handle.\n"
    print "Make the following connections please:"
    print "- Insert the two 50 pin D break-out connectors SE2186/1-0 Var1 in"
    print "  the 34921A connectors of the 34980A Multifunction switch/measure"
    print "  Unit.\n"
    print "- A short between busses COM-H and COM-L of Bank 2 (RHS from the back)\n"
    print "- Busses 3H and 3L of Bank 2 to the 'Switch Contacts' busses of the"
    print "  SE1575/1-0 Remote Controlled Mains Switch.\n"
    print "- The output of the Device under Test, to the Input of the 6060B"
    print "  Electronic Load and to busses COM-H(+) and COM-L(-) of Bank 1 (LHS from the"
    print "  back).\n"
    print "- A 5V PSU to the 5V DC input of SE1575/1-0.\n"
    print "- Connect the Remote Controlled Mains Switch between the mains and the"
    print "  Device Under Test.\n"
    print "- Make sure the Controlling PC is connected to the 6060B via GPIB and the"
    print "  34980A is connected to the same LAN as the Controlling PC.\n"
    print "The test can be interrupted with Ctrl-C.\n"
    dummy = raw_input("Press a key when all connection are done.")

    try:
        config = ConfigParser()
        config.readfp(open('testpsu.ini'))
        HP6060 = instrument(config.get('instruments','HP6060B'))
        HP34980 = instrument(config.get('instruments','HP34980A'))
        file = open(ResultFile,'w')
        EquipCtrl = Control()
        ResPage = markup.page()
        Readings = int(config.get('test','Readings'))
        Minutes = int(config.get('test','Minutes'))
        PSUrly = config.get('channels','OnOff')
        MuxConf = "CONF:VOLT:" + config.get('conf','DMM') # +", DEF," + "(@" + config.get('channels','Vin') + ")"
        EquipCtrl.RST()
        HP6060.write("MODE:CURRENT")
        HP6060.write("CURR:PROT 6")
        HP6060.write("CURR:PROT:STAT ON")
        HP34980.write(MuxConf)
        Manuf, Model, SN, Voltage, MaxCur, RepeatTests  = UserParams(config)
        ResHead = "Tested module mnufacturer: " + config.get('dut','Manuf') + "\tModel: " + config.get('dut','Model')
        Reshead = ResHead  + "\tSerial Number: " + config.get('dut','SN') + "\n"
        Reshead = ResHead + "Start time: " + time.strftime('%x %X')
        ResTitle = config.get('Results','Title')
        ResCSS = config.get('Results','css')
        ResPage.init(header = ResHead, title = ResTitle, css = ResCSS)
        Redir = raw_input("Do you want to save the test sequence output to a file? (y/n) ")
        if Redir in ['y','Y']:
            RedirFile = Model+"-"+SN+".txt"
            print "The output will be redirected to %s" % RedirFile
            sys.stdout = open(RedirFile,'w')
#        # PSU module and Load OFF
#        EquipCtrl.SSR('OFF',PSUrly)
#        EquipCtrl.LOAD('OFF',0)
        # Switch ON the PSU module
        EquipCtrl.SSR('ON',PSUrly)
        sleep(1)
        # Switch ON the DMM
        DMMrly = config.get('channels','IntMM')
        MuxConf = "ROUTE:CLOSE (@" + DMMrly + ")"
        HP34980.write(MuxConf)
        # Run 10 sec unloaded pre-test first
        print "Running unloaded pre-test"
        PreTestResults = PreTest(Loaded=0,Voltage,ResPage)
        EquipCtrl.SSR('OFF',PSUrly)
        sleep(5)
        if PreTestResult == 0:
            for Test in RepeatTests:
                for Perc in 0.25, 0.5, 0.75, 1.0:
                    Load = float(Perc) * float(MaxCur)
                    print "Load set to: %s A" % (Load)
                    print "Switching the Load ON"
                    EquipCtrl.LOAD('ON',Load)
                    sleep(1)
                    EquipCtrl.SSR('ON',PSUrly)
                    sleep(1)
                    print "Running loaded pre-test"
                    PreTestResult = PreTest(Loaded=1,Voltage,ResPage)
                    if PreTestResult == 0:
                        Measure(Test,RepeatTests,Load,Minutes,Readings,ResPage)
                        EquipCtrl.LOAD('OFF',0)
                    else:
                        EquipCtrl.SSR('OFF',PSUrly)
                        EquipCtrl.LOAD('OFF',0)
                        print "Loaded pre-test Failed. See html file for results"
                        break
                    EquipCtrl.SSR('OFF',PSUrly)
            ResPage.p("Overall Test Result: Passed")
        else:
            print "Unloaded pre-test Failed. See html file for results"
            ResPage.p("Overall Test Result: Failed")
            EquipCtrl.SSR('OFF',PSUrly)
            EquipCtrl.LOAD('OFF',0)
            EquipCtrl.RST()
    except KeyboardInterrupt:
        pass
    finally:
          print "Interrupt by User or by Un-expected error."
          EquipCtrl.RST()
          sys.stdout = sys.__stdout__
    return

if __name__ == '__main__':
    main()
