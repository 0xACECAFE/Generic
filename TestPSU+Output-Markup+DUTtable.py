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

def duttable(tabledict):
    '''This funxtion makes a HTML table with the DUT info from the ini file or from the user\'s input '''
    def newrow():
        Table.td.close()
        Table.tr.close()
        Table.tr.open()
        Table.td.open()

    Table = markup.page(case='upper')
    Table.table.open(width='50%', border='1')
    Table.tr.open()
    Table.td.open()
    Table.b('Manufacturer')
    Table.td.close()
    Table.td.open()
    Table.b(tabledict['manuf'])
    newrow()
    Table.b("Model:")
    Table.td.close()
    Table.td.open()
    Table.b(tabledict['model'])
    newrow()
    Table.b("Serialnumber:")
    Table.td.close()
    Table.td.open()
    Table.b(tabledict['sn'])
    newrow()
    Table.b("Voltage:")
    Table.td.close()
    Table.td.open()
    Table.b(tabledict['volt'])
    newrow()
    Table.b("Maximal Current:")
    Table.td.close()
    Table.td.open()
    Table.b(tabledict['cur'])
    Table.td.close()
    Table.tr.close()
    Table.table.close()
    return Table

def UserParams(config):
    '''
    Gets Tests parameters from the tester, or from the DUT section in the ini file if
    the tester only hits the Enter key.

    Params:
    config :: instance of ConfigParser() with DUT and Test data from ini file

    Returns:
    LocalList:: list with config data, either copied from ini file or filled in by user.
    '''
    cls()
    LocalList = []
    print "If no input is supplied, the data is gathered from the testpsu.ini file\n"

    Manuf = raw_input("Who is the manufacturer of the device under test? ")
    if Manuf:
        LocalList.append(Manuf)
    else:
        Manuf = config.get('dut','Manuf')
        print "From config file: %s\n" % Manuf
        LocalList.append(Manuf)

        Model = raw_input("What is the model-number of the device under test? ")
    if Model:
        LocalList.append(Model)
    else:
        Model = config.get('dut','Model')
        print "From config file: %s\n" % Model
        LocalList.append(Model)

    SerialNumber = raw_input("What is the serial number of the DUT? ")
    if SerialNumber:
        LocalList.append(SerialNumber)
    else:
        SerialNumber = config.get('dut','SN')
        print "From config file: %s\n" % SerialNumber
        LocalList.append(SerialNumber)

    NomVolt = raw_input("What is the Voltage output of the DUT? ")
    if NomVolt:
        LocalList.append(NomVolt)
    else:
        NomVolt = config.get('dut','Voltage')
        print "From config file: %s V\n" % NomVolt
        LocalList.append(NomVolt)

    MaxCur = raw_input("What is the maximum load of the DUT in Amperes? ")
    if MaxCur:
        LocalList.append(MaxCur)
    else:
        MaxCur = config.get('dut','Current')
        print "From config file: %s A\n" % MaxCur
        LocalList.append(MaxCur)

    Repeats = raw_input("How many times to repeat the sequence? ")
    if Repeats:
        LocalList.append(Repeats)
    else:
        Repeats = config.get('test','Repeats')
        print "From config file: %s repeats\n" % Repeats
        LocalList.append(Repeats)

    Time = raw_input("How long to run the test in minutes? ")
    if Time:
        LocalList.append(Time)
    else:
        Time = config.get('test','Minutes')
        print "From config file: %s minutes\n" % Time
        LocalList.append(Time)

    return LocalList

def pretest(NomVolt,HTMLfile,Loaded):
    '''
    Runs Pre-test on the DUT during 10 seconds. If this test fails, the whole procedure is aborted and is reported as Failed.
    Criteria: the measured Voltage must be within 6.5 % of the nominal value.
    Params:
    Loaded :: boolean to mark a test with the elec. load in 'On' or 'Off' state.
    NomVolt :: Integer representing the nominal output voltage of the DUT.
    HTMLfile :: pointer to the output HTML file.

    Returns:
    1 if the test failes
    0 if the test passes
    '''
    CRITERIUM = 0.065
    TestFailed = False
    HTMLpage = markup.page(case = 'upper')
    NomVolt = float(NomVolt)
    CritVolt = NomVolt * CRITERIUM
    MinVolt = NomVolt - CritVolt
    MaxVolt = NomVolt + CritVolt
    test = {True:'loaded',False:'unloaded'}[Loaded]
    HTMLpage.p('')
    HTMLpage.hr()
    HTMLpage.p("PSU module %s Pre-test.\nTest criterium: %1.1f +/- %1.1f Volt" % (test,NomVolt,CritVolt))
    HTMLpage.p('')
    for n in range(10):
        HP34980.write("READ?")
        Voltage = float(HP34980.read())
        if not MinVolt <= Voltage <= MaxVolt:
            Res = "%s Pre-test Failed at sample %d of 10. Output was %1.2f Volt" % (test,n,Voltage)
            print Res
            HTMLpage.p(Res)
            Failed = True
            break
        sleep(1)
    if TestFailed:
        HTMLfile.write(HTMLpage)
        return 1
    else:
        Res = "Pre-test Passed. Voltage: %1.3f Volt" % (Voltage)
        print Res
        HTMLpage.p(Res)
        HTMLpage.hr()
        HTMLpage.p('')
        HTMLfile.write(HTMLpage)
        return 0

def Measure(Test,RepeatTests,NomVolt,Load,Minutes,Readings,HTMLfile):
    '''
    Runs the main test with the Elec. Load 'On'. If the test fails, the procedure is aborted and reported as Failed.
    Criteria: the measured Voltage must be within 6.5 % of the nominal value.

    Params:
    Test :: sequence number for the number of repetitions of the complete procedure.
    RepeatTests :: Total number of repetitions of the whole procedure.
    NomVolt :: Nominal Output voltage of the DUT.
    Load :: float with the requested current for the Elec. Load.
    Minutes :: Total Time to run the test with the requested current.
    Readings :: Number of samples per minute for the voltage and curretn measurements.
    HTMLfile :: Pointer to the output HTML file.
    
    Returns:
    1 if the test failes
    0 if the test passes    
    '''
    CRITERIUM = 0.065
    HTMLpage=markup.page(case='upper')
    HTMLpage.hr()
    HTMLpage.p('')
    HTMLpage.p("Start of measurement cycle %s of %s.\nTesting with a load of %s A.\nDuration: %s minutes\nTaking %s readings per minute.\n" % (Test,RepeatTests,Load,Minutes,Readings))
    HTMLpage.p('')
    HTMLpage.hr()
    NomVolt = float(NomVolt)
    CritVolt = NomVolt * CRITERIUM
    MinVolt = NomVolt - CritVolt
    MaxVolt = NomVolt + CritVolt
    TestFailed = False
    print "\nStarting Load test."
    print "This test will take %s minutes\n" % Minutes
    TotReadings = Minutes * Readings
    LINES_PER_PARAGRAPH = 5
    for Reading in range(TotReadings):
        print "Reading %s of %s" % (Reading,TotReadings)
        HP34980.write("READ?")
        HP6060.write("MEAS:CURR?")
        Current = float(HP6060.read())
        print "Current through Load: %1.3f A" % Current
        Voltage = float(HP34980.read())
        if not MinVolt <= Voltage <= MaxVolt:
            Res = "Test Failed at step %d of %d. Output was %1.3f Volt" % (Reading,TotReadings,Voltage)
            print Res
            HTMLpage.p(Res)
            TestFailed = True
            break
        print "Measured: %1.3f Volt\n" % Voltage
        sleep(60/Readings)
        HTMLpage.p("Reading %d of %d.\tMeasured Current: %s A\tMeasured Voltage: %1.3f V" % (Reading,TotReadings,Current,Voltage))
        LINES_PER_PARAGRAPH -= 1
        if LINES_PER_PARAGRAPH == 0 :
            LINES_PER_PARAGRAPH = 5
            HTMLpage.p('')
    HTMLpage.hr()
    HTMLpage.p('')
    HTMLfile.write(HTMLpage)
    if testFailed:
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
    '''
    Sets up the test and runs the pretest() and measure() function. Determines if the results Pass or Fail.
    
    Params:
    None
    
    Returns:
    None
    '''
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
        TestResult = 0
        config = ConfigParser()
        config.readfp(open('testpsu.ini'))
        HP6060 = instrument(config.get('instruments','HP6060B'))
        HP34980 = instrument(config.get('instruments','HP34980A'))
        HTMLfile = open(ResultFile,'w')
        EquipCtrl = Control()
        Readings = int(config.get('test','Readings'))
        Minutes = int(config.get('test','Minutes'))
        PSUrly = config.get('channels','OnOff')
        MuxConf = "CONF:VOLT:" + config.get('conf','DMM')
        EquipCtrl.RST()
        HP6060.write("MODE:CURRENT")
        HP6060.write("CURR:PROT 6")
        HP6060.write("CURR:PROT:STAT ON")
        HP34980.write(MuxConf)
        Manuf, Model, SN, Voltage, MaxCur, RepeatTests, Time  = UserParams(config)
        DUTDict = {'manuf':Manuf,'model':Model,'sn':SN,'volt':Voltage,'cur':MaxCur}
        HTMLpage = markup.page(case='upper')
        ResTitle = config.get('Results','Title')
        ResCSNomVoltconfig.get('Results','css')
        HTMLpage.init(title = ResTitle, css = ResCSS)
        DUTtable = DUTTable(DUTDict)
        HTMLpage.p('')
        HTMLpage.hr(noshade=None, width="80%", align="center", size="2")
        HTMLpage.p("Start time: %s" % time.strftime('%x %X'))
        HTMLpage.hr(noshade=None, width="80%", align="center", size="2")
        HTMLpage.p('')
        Redir = raw_input("Do you want to save the test sequence output to a HTMLfile? (y/n) ")
        if Redir in ['y','Y']:
            RedirFile = Model+"-"+SN+".txt"
            print "The output will be redirected to %s" % RedirFile
            sys.stdout = open(RedirFile,'w')
        # Switch ON the PSU module
        EquipCtrl.SSR('ON',PSUrly)
        sleep(1)
        # Switch ON the DMM
        DMMrly = config.get('channels','IntMM')
        MuxConf = "ROUTE:CLOSE (@" + DMMrly + ")"
        HP34980.write(MuxConf)
        # Run 10 sec unloaded pre-test first
        print "Running unloaded pre-test"
        PreTestResults = pretest(Voltage,HTMLfile,Loaded=False)
        EquipCtrl.SSR('OFF',PSUrly)
        sleep(5)
        if PreTestResult == 1:
            print "Unloaded pre-test Failed. See html file for results"
            HTMLpage.p('')
            HTMLpage.hr(noshade=None, width="80%", align="center", size="2")
            HTMLpage.p("Overall Test Result: Failed")
            HTMLpage.hr(noshade=None, width="80%", align="center", size="2")
            HTMLpage.p('')
            HTMLfile.write(HTMLpage)
            EquipCtrl.SSR('OFF',PSUrly)
            EquipCtrl.LOAD('OFF',0)
            EquipCtrl.RST()
            RESULT = "Failed"
            return
        for Test in range(RepeatTests):
            for Perc in 0.25, 0.5, 0.75, 1.0:
                Load = float(Perc) * float(MaxCur)
                print "Load set to: %s A" % (Load)
                print "Switching the Load ON"
                EquipCtrl.LOAD('ON',Load)
                sleep(1)
                EquipCtrl.SSR('ON',PSUrly)
                sleep(1)
                print "Running loaded pre-test"
                PreTestResult = pretest(Voltage,HTMLfile,Loaded=True)
                if PreTestResult == 0:
                    RESULT = "Passed"
                    print "Running main test"
                    TestResult = Measure(Test,RepeatTests,Voltage,Load,Minutes,Readings,HTMLfile)
                    if TestResult == 1:
                        RESULT = "Failed"
                        EquipCtrl.SSR('OFF',PSUrly)
                        EquipCtrl.LOAD('OFF',0)
                        break
                else:
                    RESULT = "Failed"
                    EquipCtrl.SSR('OFF',PSUrly)
                    EquipCtrl.LOAD('OFF',0)
                    break
                EquipCtrl.SSR('OFF',PSUrly)
        print "Overall Test Result: %s" % RESULT
        HTMLpage.p('')
        HTMLpage.hr(noshade=None, width="80%", align="center", size="2")
        HTMLpage.p("Overall Test Result: %s" % RESULT)
        HTMLpage.hr(noshade=None, width="80%", align="center", size="2")
        HTMLpage.p('')
        HTMLfile.write(HTMLpage)
    except KeyboardInterrupt:
        pass
    finally:
          print "Program Stopped."
          EquipCtrl.RST()
          HTMLfile.close()
          sys.stdout = sys.__stdout__
    return

if __name__ == '__main__':
    main()
