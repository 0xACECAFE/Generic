#!/usr/bin/python

# checkbox.py

import wx

class MyFrame(wx.Frame):
    LCLused=[]
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(200, 150))
        panel = wx.Panel(self, -1)
        self.cb1 = wx.CheckBox(panel, -1, 'LCL1', (10, 10))
        self.cb2 = wx.CheckBox(panel, -1, 'LCL2', (20, 10))
        self.cb3 = wx.CheckBox(panel, -1, 'LCL3', (30, 10))
        self.cb4 = wx.CheckBox(panel, -1, 'LCL4', (40, 10))
        self.cb5 = wx.CheckBox(panel, -1, 'LCL5', (50, 10))
        self.cb6 = wx.CheckBox(panel, -1, 'LCL6', (60, 10))
        self.cb7 = wx.CheckBox(panel, -1, 'LCL7', (70, 10))
        self.cb8 = wx.CheckBox(panel, -1, 'LCL8', (80, 10))
        self.cb9 = wx.CheckBox(panel, -1, 'LCL9', (90, 10))
        self.cb10 = wx.CheckBox(panel, -1, 'LCL10', (100, 10))
        self.cb11 = wx.CheckBox(panel, -1, 'LCL11', (110, 10))
        self.cb12 = wx.CheckBox(panel, -1, 'LCL12', (120, 10))
        self.cb13 = wx.CheckBox(panel, -1, 'LCL13', (130, 10))
        self.cb14 = wx.CheckBox(panel, -1, 'LCL14', (140, 10))
        self.Centre()

        self.Bind(wx.EVT_CHECKBOX, self.SetLCL1, id=self.cb1.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL2, id=self.cb2.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL3, id=self.cb3.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL4, id=self.cb4.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL5, id=self.cb5.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL6, id=self.cb6.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL7, id=self.cb7.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL8, id=self.cb8.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL9, id=self.cb9.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL10, id=self.cb10.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL11, id=self.cb11.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL12, id=self.cb12.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL13, id=self.cb13.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetLCL14, id=self.cb14.GetId())

    def SetLCL1(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL2(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL3(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL4(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL5(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL6(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL7(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL8(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL9(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL10(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL11(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL12(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL13(self, event):
        LCLused.append(1)
        self.Refresh()

    def SetLCL14(self, event):
        LCLused.append(1)
        self.Refresh()

    

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'checkbox.py')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()
