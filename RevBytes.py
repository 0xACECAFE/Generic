Python 2.2.2 (#1, Mar 17 2003, 15:17:58) 
[GCC 3.3 20030226 (prerelease) (SuSE Linux)] on linux2
Type "copyright", "credits" or "license" for more information.
IDLE 0.8 -- press F1 for help
>>> range90,10)
SyntaxError: invalid syntax
>>> range(0,10)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> import hex
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in ?
    import hex
ImportError: No module named hex
>>> print 0x0a
10
>>> print '0x'.'a'
SyntaxError: invalid syntax
>>> print '0x'+'a'
0xa
>>> print eval('0x'+'a')
10
>>> for line in open("file1.tek",'r').readline():
	print line

	
\
0
0
1
0
0
0
2
3
0
0
7
9
7
0
1
0
2
0
3
0
4
0
5
0
6
0
7
0
8
0
9
0
C


>>> >>>
SyntaxError: invalid syntax
>>> for line in open("file1.tek",'r').readline():
	Byte[]=line
	
SyntaxError: invalid syntax
>>> for line in open("file1.tek",'r').readlines():
	print line

	
\00100023007970102030405060708090C

\xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

\yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

\zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz

>>> print line[0]
\
>>> close(()

      
KeyboardInterrupt
>>> close()
Traceback (most recent call last):
  File "<pyshell#17>", line 1, in ?
    close()
NameError: name 'close' is not defined
>>> close("file1.tek")
Traceback (most recent call last):
  File "<pyshell#18>", line 1, in ?
    close("file1.tek")
NameError: name 'close' is not defined
>>> f=open('file1.tek','r')
>>> line=f.readline()
>>> print line[2]
0
>>> for a in line:
	print a

	
\
0
0
1
0
0
0
2
3
0
0
7
9
7
0
1
0
2
0
3
0
4
0
5
0
6
0
7
0
8
0
9
0
C


>>> line2=line[-3]
>>> print line2
0
>>> line2=line[,-3]
SyntaxError: invalid syntax
>>> line2=line[0,-3]
Traceback (most recent call last):
  File "<pyshell#28>", line 1, in ?
    line2=line[0,-3]
TypeError: sequence index must be integer
>>> line2=line[0,3]
Traceback (most recent call last):
  File "<pyshell#29>", line 1, in ?
    line2=line[0,3]
TypeError: sequence index must be integer
>>> line2=line[0-3]
>>> print line2
0
>>> print line
\00100023007970102030405060708090C

>>> print line[0,3]
Traceback (most recent call last):
  File "<pyshell#33>", line 1, in ?
    print line[0,3]
TypeError: sequence index must be integer
>>> print line[0-3]
0
>>> print line[-3]
0
>>> print line[0:3]
\00
>>> print line[:5]
\0010
>>> line2=line[:5]
>>> line2
'\\0010'
>>> line2=line[:7]
>>> line2
'\\001000'
>>> SESN='98503001'
>>> sesn
Traceback (most recent call last):
  File "<pyshell#43>", line 1, in ?
    sesn
NameError: name 'sesn' is not defined
>>> SESN
'98503001'
>>> NameError: name 'sesn' is not defined
SyntaxError: invalid syntax
>>> SESN[1]
'8'
>>> for i in range(1,4):
	NewSESN[i:i+1]=SESN[5-i]

	
Traceback (most recent call last):
  File "<pyshell#49>", line 2, in ?
    NewSESN[i:i+1]=SESN[5-i]
NameError: name 'NewSESN' is not defined
>>> NewSESN=[]
>>> for i in range(1,4):
	NewSESN[i:i+1]=SESN[5-i]

	
Traceback (most recent call last):
  File "<pyshell#52>", line 2, in ?
    NewSESN[i:i+1]=SESN[5-i]
TypeError: must assign list (not "str") to slice
>>> for i in range(1,4):
	NewSESN=SESN[5-i]

	
>>> NewSESN
'5'
>>> SESN
'98503001'
>>> for i in range(8,1,-2

	       ):
	NewSESN=SESN[5-i]
KeyboardInterrupt
>>> >>> for i in range(8,1,-2):
	
SyntaxError: invalid syntax
>>> for i in range(8,1,-2):
	NewSESN=SESN[5-i]

	
>>> NewSESN
'0'
>>> for i in range(8,1,-2):
	print SESN[5-i]

	
0
1
8
0
>>> SESN[8]
Traceback (most recent call last):
  File "<pyshell#63>", line 1, in ?
    SESN[8]
IndexError: string index out of range
>>> SESN
'98503001'
>>> SESN[7]
'1'
>>> for i in range(7,1,-2):
	print SESN[i]

	
1
0
0
>>> range(
KeyboardInterrupt
>>> for i in range(7,1,-2):
	print i, SESN[i]

	
7 1
5 0
3 0
>>> for i in range(7,0,-2):
	print i, SESN[i], SESN[i-1]

	
7 1 0
5 0 3
3 0 5
1 8 9
>>> for i in range(7,0,-2):
	NewSESN=SESN[i]+SESN[i-1]

	
>>> NewSESN
'89'
>>> for i in range(7,0,-2):
	NewSESN=.+SESN[i]+SESN[i-1]
	
SyntaxError: invalid syntax
>>> for i,j in range(7,0,-2),range(1,8):
	NewSESN=SESN[i]+SESN[i-1]

	
Traceback (most recent call last):
  File "<pyshell#77>", line 1, in ?
    for i,j in range(7,0,-2),range(1,8):
ValueError: unpack list of wrong size
>>> help string
SyntaxError: invalid syntax
>>> split()
Traceback (most recent call last):
  File "<pyshell#79>", line 1, in ?
    split()
NameError: name 'split' is not defined
>>> import readline
>>> raw_input()
aldsdskasl
'aldsdskasl'
>>> slice(0,3)
slice(0, 3, None)
>>> for i in range(3,0):
	NewSESN=SESN[i*2]+SESN[(i*2)+1]

	
>>> NewSESN
'89'
>>> for i in range(3,0):
	SESN[i*2]+SESN[(i*2)+1]

	
>>> for i in range(3,0):
	print SESN[i*2]+SESN[(i*2)+1]

	
>>> for i in range(3,0):
	print SESN[i*2],SESN[(i*2)+1]

	
>>> SESN
'98503001'
>>> for i in range(3,0):
	print i,SESN[i*2],SESN[(i*2)+1]

	
>>> for i in range(3,0,-1):
	print i,SESN[i*2],SESN[(i*2)+1]

	
3 0 1
2 3 0
1 5 0
>>> for i in range(3,-1,-1):
	print i,SESN[i*2],SESN[(i*2)+1]

	
3 0 1
2 3 0
1 5 0
0 9 8
>>> for i in range(3,-1,-1):
	print i,SESN[i*2],SESN[(i*2)+1]
	NewSESN.append(3-i)=[SESN[i*2],SESN[(i*2)+1]]
	
SyntaxError: can't assign to function call
>>> for i in range(3,-1,-1):
	print i,SESN[i*2],SESN[(i*2)+1]
	NewSESN.append(3-i,[SESN[i*2],SESN[(i*2)+1])
		       
SyntaxError: invalid syntax
>>> for i in range(3,-1,-1):
	print i,SESN[i*2],SESN[(i*2)+1]
	NewSESN.append(3-i,SESN[i*2],SESN[(i*2)+1])

	
3 0 1
Traceback (most recent call last):
  File "<pyshell#103>", line 3, in ?
    NewSESN.append(3-i,SESN[i*2],SESN[(i*2)+1])
AttributeError: 'str' object has no attribute 'append'
>>> for i in range(3,-1,-1):
	print i,SESN[i*2],SESN[(i*2)+1]
	NewSESN.insert(3-i,SESN[i*2],SESN[(i*2)+1])

	
3 0 1
Traceback (most recent call last):
  File "<pyshell#105>", line 3, in ?
    NewSESN.insert(3-i,SESN[i*2],SESN[(i*2)+1])
AttributeError: 'str' object has no attribute 'insert'
>>> reverse SESN
SyntaxError: invalid syntax
>>> reverse(SESN)
Traceback (most recent call last):
  File "<pyshell#107>", line 1, in ?
    reverse(SESN)
NameError: name 'reverse' is not defined
>>> SESN.reverse()
Traceback (most recent call last):
  File "<pyshell#108>", line 1, in ?
    SESN.reverse()
AttributeError: 'str' object has no attribute 'reverse'
>>> NewSESN=SESN
>>> NewSESN
'98503001'
>>> newssesn=[]
>>> newsesn.append(SESN)
Traceback (most recent call last):
  File "<pyshell#112>", line 1, in ?
    newsesn.append(SESN)
NameError: name 'newsesn' is not defined
>>> newsesn=[]
>>> newsesn.append(SESN)
>>> newsesn
['98503001']
>>> NewSESN
'98503001'
>>> newsesn=[]
>>> for i in range(3,-1,-1):
	print i,SESN[i*2],SESN[(i*2)+1]
	newsesn.insert(3-i,SESN[i*2],SESN[(i*2)+1])

	
3 0 1
Traceback (most recent call last):
  File "<pyshell#119>", line 3, in ?
    newsesn.insert(3-i,SESN[i*2],SESN[(i*2)+1])
TypeError: insert() takes exactly 2 arguments (3 given)
>>> for i in range(3,-1,-1):
	print i,SESN[i*2],SESN[(i*2)+1]
	newsesn.insert(3-i,SESN[i*2]+SESN[(i*2)+1])

	
3 0 1
2 3 0
1 5 0
0 9 8
>>> newsesn
['01', '30', '50', '98']
>>> for i in range(3,-1,-1):
	print i,SESN[i*2],SESN[(i*2)+1]
	newsesn.insert(3-i,SESN[i*2]+SESN[(i*2)+1])

	
3 0 1
2 3 0
1 5 0
0 9 8
>>> newsesn
['01', '30', '50', '98', '01', '30', '50', '98']
>>> newsesn=[]
>>> for i in range(3,-1,-1):
	print i,SESN[i*2],SESN[(i*2)+1]
	newsesn.insert(3-i,SESN[i*2]+SESN[(i*2)+1])

	
3 0 1
2 3 0
1 5 0
0 9 8
>>> newsesn
['01', '30', '50', '98']
>>> for line in open("file1.tek",'r').readline():
	print line

	
\
0
0
1
0
0
0
2
3
0
0
7
9
7
0
1
0
2
0
3
0
4
0
5
0
6
0
7
0
8
0
9
0
C


>>> for line in open("file1.tek",'r').readline():
	linelist
KeyboardInterrupt
>>> linelist=[]
>>> >>> for line in open("file1.tek",'r').readline():
	
SyntaxError: invalid syntax
>>> >>> for line in open("file1.tek",'r').readline():
	
SyntaxError: invalid syntax
>>> 
>>> for line in open("file1.tek",'r').readline():
	linelist=line

	
>>> linelist
'\n'
>>> for line in open("file1.tek",'r').readline():
	linelist.append(line)

	
Traceback (most recent call last):
  File "<pyshell#141>", line 2, in ?
    linelist.append(line)
AttributeError: 'str' object has no attribute 'append'
>>> linelist
'\n'
>>> linelist=[]
>>> for line in open("file1.tek",'r').readline():
	linelist.append(line)

	
>>> linelist
['\\', '0', '0', '1', '0', '0', '0', '2', '3', '0', '0', '7', '9', '7', '0', '1', '0', '2', '0', '3', '0', '4', '0', '5', '0', '6', '0', '7', '0', '8', '0', '9', '0', 'C', '\n']
>>> linelist[0]=[]
>>> linelist
[[], '0', '0', '1', '0', '0', '0', '2', '3', '0', '0', '7', '9', '7', '0', '1', '0', '2', '0', '3', '0', '4', '0', '5', '0', '6', '0', '7', '0', '8', '0', '9', '0', 'C', '\n']
>>> linelist[0]='\'
SyntaxError: invalid token
>>> linelist[0]='\\'
>>> linelist
['\\', '0', '0', '1', '0', '0', '0', '2', '3', '0', '0', '7', '9', '7', '0', '1', '0', '2', '0', '3', '0', '4', '0', '5', '0', '6', '0', '7', '0', '8', '0', '9', '0', 'C', '\n']
>>> Exception in Tkinter callback
Traceback (most recent call last):
  File "/var/tmp/python-2.2.2-build//usr/lib/python2.2/lib-tk/Tkinter.py", line 1343, in __call__
    return apply(self.func, args)
  File "/usr/lib/idle/SearchBinding.py", line 73, in find_selection_event
    SearchDialog.find_selection(self.editwin.text)
  File "/usr/lib/idle/SearchDialog.py", line 20, in find_selection
    return _setup(text).find_selection(text)
  File "/usr/lib/idle/SearchDialog.py", line 67, in find_selection
    return self.find_again(text)
  File "/usr/lib/idle/SearchDialog.py", line 36, in find_again
    self.open(text)
  File "/usr/lib/idle/SearchDialogBase.py", line 18, in open
    self.create_widgets()
  File "/usr/lib/idle/SearchDialog.py", line 25, in create_widgets
    f = SearchDialogBase.create_widgets(self)
  File "/usr/lib/idle/SearchDialogBase.py", line 45, in create_widgets
    self.create_entries()
  File "/usr/lib/idle/SearchDialogBase.py", line 72, in create_entries
    self.ent = self.make_entry("Find:", self.engine.patvar)
  File "/usr/lib/idle/SearchDialogBase.py", line 52, in make_entry
    l.grid(row=self.row, col=0, sticky="w")
  File "/var/tmp/python-2.2.2-build//usr/lib/python2.2/lib-tk/Tkinter.py", line 1735, in grid_configure
    self.tk.call(
TclError: ambiguous option "-col": must be -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky
