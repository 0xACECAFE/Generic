#!/usr/bin/python

# checkbox.py

import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(200, 150))
        panel = wx.Panel(self, -1)
        self.cb1 = wx.CheckBox(panel, -1, 'Red', (10, 10))
        self.cb2 = wx.CheckBox(panel, -1, 'Green', (10, 30))
        self.cb3 = wx.CheckBox(panel, -1, 'Blue', (10, 50))
        self.Centre()

        self.Bind(wx.EVT_CHECKBOX, self.SetRed, id=self.cb1.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetGreen, id=self.cb2.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetBlue, id=self.cb3.GetId())

    def SetRed(self, event):
        self.SetBackgroundColour(wx.RED)
        self.cb2.SetValue(False)
        self.cb3.SetValue(False)
        self.Refresh()

    def SetGreen(self, event):
        self.SetBackgroundColour(wx.GREEN)
        self.cb1.SetValue(False)
        self.cb3.SetValue(False)
        self.Refresh()

    def SetBlue(self, event):
        self.SetBackgroundColour(wx.BLUE)
        self.cb1.SetValue(False)
        self.cb2.SetValue(False)
        self.Refresh()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'checkbox.py')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()
