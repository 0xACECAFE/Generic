#! /usr/bin/env python
# Dit programma leest een Tab Seperated Value (TSV) file met route info voor het maken van route-
# beschrijvingen.
# De data in de file is ge-organiseerd als:
# [tussen-afstand]<tab>[totaal-afstand]<tab>route aanwijzing<tab>opmerking
# Een regel die begint met een '#' in rij 3 of 4 wordt schuin weer gegeven.
# Een plaatsnaam in rij 2, die met allemaal uppercase letter is geschreven, wordt vet afgedrukt.
# Het programma schrijft de data weg als een LaTeX longtable file, die direct ge-compileerd kan worden
# naar een Acrobat pdf of postscript file.
# Voorbeeld van een text file voor een rit:
#
# 0[tab]0[tab]Via A4, A10-zuid, A10-oost ri Amsterdam[tab]
# 46.5[tab][tab]RE bij afrit S114 Zeeburg[tab]
# 1.2[tab][tab]Einde weg LI[tab]S114, Zuiderzeeweg
# 1.1[tab][tab]2e VKL RE ri Noord (wit bord)[tab]
# 1.3[tab]50[tab]ROT RE en direct SPL LI ri Durgerdam[tab]Liergouw
# 2.0[tab][tab]Einde weg LI ri Ransdorp[tab]Dorpsweg Ransdorp
# [tab][tab]RANSDORP[tab]
# [tab][tab]# commentaar in rij 3[tab]# of 4 wordt schuin afgedrukt
#
# De [tab] characters moeten 'echte' tabs zijn, geen 'soft-tabs' met spaties.
# De laatste, derde, [tab] kan eventueel worden weggelaten, het programma maakt hier melding van en
# past, waar nodig, de interne file structuur aan. Als er te weinig velden worden gelezen in een rij
# maakt het programma hier ook melding van, maar dan wordt de betreffende rij niet gebruikt.
# Bij teveel velden in een rij worden alleen de eerste 4 gebruikt.
'''
Gebruik:
FormatRoutes [-s N.N] [-h] [-t "titel"] [-z NN] [TSV file]
Opties: -h          deze help
        -s N.N      relatieve hoogte van tabel rijen, tussen 0.7 en 3.0
        -t "titel"  Optionele titel voor de route
        -d          Draft vesie; lijnen voor afstanden in de tabel opgevuld met puntjes, -s wordt 2.0 bij
                    gebruik van -d.
        -z NN       Editie nummer voor een Zeepaardjesrit-versie; de file "ZPR-Voorpagina.tex" wordt
                    geladen en gebruikt om de voorpagina mee te maken.
De file die geschreven wordt is de naam van de invoerfile, met het deel achter
'.' vervangen door 'tex'.
De titel wordt ook uit de naam van de input file gehaald, tenzij de gebruiker
een aparte titel aangeeft met -t
'''
import os
import sys
import csv
import re

# Print usage message and exit
def usage(*args):
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(1)

def UserInput():
    '''
    UserInput asks for the filename of the Tab Seperated Route File to parse.
    Arguments: none
    Returns: name of input file in RouteFile and name of formatted output file to be written in FmtRouteFile
    '''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    try:
        RouteFile = raw_input("De naam van de TSV route file svp: ")
        f = open(RouteFile, 'r')
    except IOError, msg:
        usage("Kan %s niet lezen.\n %s" % (repr(RouteFile), str(msg)))
    f.close()
    UserTitle = str(raw_input("Een titel voor de route svp (<Enter> voor gebruik van input filenaam): "))
    if UserTitle:
        Title = UserTitle
    else:
        Title = RouteFile.rpartition('.')[0] #rpartition('.')[0] returns the stuff before the last .
    FmtRouteFile = RouteFile.rpartition('.')[0] + '.tex'
    return RouteFile, FmtRouteFile, Title

# Get Frontpage matter for a "Zeepaardjesrit" or default.
def MakeFrontMatter(ZPRedition):
    '''
    MakeFrontMatter: makes a list containing default or extended frontpage
    Argumenten: ZPRedition; greater than 0 for usage of extended "Zeepaardjes-rit" fontpage
                            The extended page is read from file "ZPR-Voorpagina.tex".
                            this file has to be present in the directory the program
                            is run in.
                            ZPRedition is also put in the LaTeX frontpage
    returns: FrontMatter; list of LaTeX commands and text to make frontpage
    '''
    if ZPRedition:
        NewCommand = '\\vspace{0.25cm}\n\\newcommand{\\ZPReditie}{' + ZPRedition + '}\n'
        try:
            f = open("ZPR-Voorpagina.tex")
            FrontMatter = NewCommand + ''.join(f.readlines())
            f.close()
        except IOError, msg:
            usage("Kan %s niet lezen.\n %s" % (repr(f), str(msg)))
    else:
        FrontMatter = [
        '\\hspace*{0.5cm}\\underline{Gebruikte afkortingen:}\\\\\n',
        '\\textbf{\\begin{tabular}{ll}\n',
        'KRS: & Kruising\\\\\n',
        'LI: & Links\\\\\n',
        'PNB: & PlaatsNaamBord\\\\\n',
        'RE: & Rechts\\\\\n',
        'ri: & richting\\\\\n',
        'ROT: & Rotonde\\\\\n',
        'SPL: & Splitsing\\\\\n',
        'VKL: & Verkeerslicht\\\\\n',
        'VRK: & Voorrangskruising\\\\\n',
        'VRW: & Voorrangsweg\\\\\n',
        '\\underline{NOORDWIJK}: & Plaatsnaambord\\\\\n',
        '\\end{tabular}}\n']
    return FrontMatter

# Take route file in.
def ReadTSVRoute(RouteFile):
    '''
    Uses csv module to read fileds from Tab Seperate value route file
    Arguments: RouteFile name of input file
    Returns:   RouteList list of raw route text
    '''
    TSVRouteRead = csv.reader(open(RouteFile, "rb"), delimiter='\t', quoting=csv.QUOTE_NONE)
    RouteList = []
    InvalidLines = 0
    for row in TSVRouteRead:
        if len(row) < 3:
            print "Rij wordt niet gebruikt.\nAantal velden in deze rij is %d (minimaal 3), aanpassen svp." % len(row)
            print `row`
            InvalidLines += 1
        elif len(row) == 3:
            print "Aantal velden in deze rij is 3, de rij wordt opgevuld."
            print "Oud:\t%s" % `row`
            row.append('')
            print "Nieuw:\t%s" % `row`
            RouteList.append(row)
        elif len(row) > 4:
            print "Aantal velden in deze rij is %d, aanpassen svp\n (eerste 4 velden van de rij worden gebruikt)." % len(row)
            print `row`
            RouteList.append(row)
        else:
            RouteList.append(row)
    return RouteList, InvalidLines

# Add LaTeX longtable formats and divide in blocks of 5
def FormatRoute(RouteList, FrontMatter, Title, Stretch, Draft):
    '''
    FormatRoute gets the raw TSV date and formats this in to LaTeX.
    Arguments: RouteList   list with route text fields
               FrontMatter LaTeX frontpage stuff.
               Title       Title to write on top of the route
               Stretch     Relative distance between rows
               Draft       boolean to make spaces under distance columns fill with dots.
    Returns:   NewRouteList list with LaTeX formatted text
    '''
    NewRouteList = []
    RowNum = 0
    # match all names in capitals, 4 chars or longer, maybe followed by a whitespace and another name in capitals
    #PlaatsNaam = re.compile(r'^[A-Z]{4,}\s?[A-Z]*')
    # Match all names starting with '@'
    PlaatsNaam = re.compile(r'^@(.*)$')
    # match a string that starts with a hash
    Comment =   re.compile(r'^#(.*)$')
    EmptyRow = '& & & \\\\\n'
    ArrayStretch = '\\renewcommand{\\arraystretch}{' + Stretch + '}\n'
    TitleRow = '\\begin{center}\\framebox[10cm]{\\begin{LARGE}\\textbf{' + Title + '}\\end{LARGE}}\\end{center}\n'

    PreAmble = [
    '\\documentclass[a4paper,12pt]{article}\n',
    '\\usepackage{longtable}\n',
    '\\usepackage[T1]{fontenc}\n',
    '\\usepackage[latin1]{inputenc}\n',
    '\\usepackage[]{times}\n',
    '\\usepackage[noheadfoot,margin=1cm,centering]{geometry}\n',
    '\\pagestyle{plain}\n',
    '\\begin{document}\n',
    TitleRow]

    BeginTable = [
    ArrayStretch,
    '\\begin{longtable}{p{0.5cm}p{1.2cm}p{1.0cm}p{9cm}p{6cm}}\n',
    '& verschil (km) & totaal (km) & \\newline Aanwijzing & \\newline Straatnaam/Opmerking\\\ \hline \endhead\n']

    PostAmble = [
    '\\hfill\n',
    '\\end{longtable}\n',
    '\\end{document}\n']

    for Row in PreAmble:
        NewRouteList.append(Row)
    for Row in FrontMatter:
        NewRouteList.append(Row)
    for Row in BeginTable:
        NewRouteList.append(Row)
    for Row in RouteList:
        RowNum += 1
        RowNumStr = '\\textit{' +`RowNum` +'}'
        DepDF = DF = '\\dotfill & '
        if PlaatsNaam.match(Row[1]):
            Row[1] = '\\underline{\\textbf{' + Row[1][1:] + '}}'
            RowNumStr = '' # No linenumbers together with town-names
            DepDF = '& '
            RowNum -=1
        if Comment.match(Row[2]):
            Row[2] = '\\underline{\\emph{' + Row[2][1:] + '}}' #[1:] om de hash kwijt te raken
            DepDF = '& '
            RowNumStr = '' # No linenumbers together with comments in 2nd field
            RowNum -=1
        if Comment.match(Row[3]):
            Row[3] = '\\underline{\\emph{' + Row[3][1:] + '}}'
        if Draft == 1:
            DraftDF = DF
        else:
            DraftDF = '& '
        NewRow =  RowNumStr + ' & ' + Row[0] + DraftDF + Row[1] + DraftDF + Row[2] + DepDF + Row[3] + '\\\\\n'
        NewRouteList.append(NewRow)
        if RowNum % 5 == 0: # Make nice 5 row parts
            NewRouteList.append(EmptyRow)
    for Row in PostAmble:
        NewRouteList.append(Row)
    return NewRouteList

def WriteFormattedRoute(NewRouteList,FmtRouteFile):
    '''
    WriteFormattedRoute writes the data back to disk.
    Arguments: NewRouteList list with the LaTeX formatted route
               FmtRouteFile file-name to write data to.
    Returns:   none
    '''
    try:
        f = open(FmtRouteFile, 'w')
        for Row in NewRouteList:
            f.write(Row)
        f.close()
    except IOError, msg:
        usage("Kan niet schrijven naar %s.\n %s" % (repr(FmtRouteFile), str(msg)))

# Main program: parse command line and start processing
def main():
    '''
    main() handles the arguments to the script and calls the the other functions with
    arguments from the command line if they are supplied, or calls the UserInput function first
    if no argument are supplied.
    Arguments: none
    Returns: none
    '''
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:t:z:dh')
    except getopt.error, msg:
        usage(msg)
    Stretch = '1.0'
    OptTitle = ''
    Draft = 0
    ZPRedition = ''
    for o, a in opts:
        if o == '-h': usage()
        if o == '-s':
            Stretch = a
        if o == '-t':
            OptTitle = a
        if o == '-d':
            Draft = 1
            Stretch = '2.0'
        if o == '-z':
            ZPRedition = a
    try:
        if float(Stretch) < 0.7 or float(Stretch) > 3.0:
            print "Relatieve afstand -s %s niet geldig. -s wordt 1.0" % Stretch
            Stretch = '1.0'
    except ValueError, msg:
        usage(msg)
    if args:
        RouteFile = args[0]
        if OptTitle:
            Title = OptTitle
        else:
            Title = RouteFile.rpartition('.')[0]
        FmtRouteFile = RouteFile.rpartition('.')[0] + '.tex'
    else:
        RouteFile, FmtRouteFile, Title = UserInput()
    if ZPRedition:
        print "Dit is een Zeepaardjes versie"
        Title = ZPRedition + 'e ' + Title
    RouteList, InvalidLines = ReadTSVRoute(RouteFile)
    print "De TSV route file is gelezen uit %s (%d regels, %d ongeldig)\n" % (RouteFile,len(RouteList),InvalidLines)
    print "De titel wordt: \'%s\'\n" % Title
    print "De afstand tussen de rijen wordt %sx groter" % Stretch
    FrontMatter = MakeFrontMatter(ZPRedition)
    NewRouteList = FormatRoute(RouteList, FrontMatter, Title, Stretch, Draft)
    print; print "De LaTeX route file wordt geschreven in %s\n" % FmtRouteFile
    WriteFormattedRoute(NewRouteList,FmtRouteFile)
    print "Gedaan.."
    print "Edit de LaTeX file eventueel om lege regels te verwijderen ed., en compileer"
    print "de gegenereerde file met:  pdflatex %s.\n" % FmtRouteFile
    return

if __name__ == '__main__':
    main()
