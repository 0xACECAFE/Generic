#!/usr/bin/python

# spinctrl.py

import wx

class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(350, 310))

        wx.StaticText(self, -1, 'Convert Fahrenheit temperature to Celsius', (20,20))
        wx.StaticText(self, -1, 'Fahrenheit: ', (20, 80))
        wx.StaticText(self, -1, 'Celsius: ', (20, 150))

        self.celsius =  wx.StaticText(self, -1, '', (150, 150))
        self.sc = wx.SpinCtrl(self, -1, '',  (150, 75), (60, -1))
        self.sc.SetRange(-459, 1000)
        self.sc.SetValue(0)

        compute_btn = wx.Button(self, 1, 'Compute', (70, 250))
        compute_btn.SetFocus()
        clear_btn = wx.Button(self, 2, 'Close', (185, 250))

        self.Bind(wx.EVT_BUTTON, self.OnCompute, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=2)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnCompute(self, event):
        fahr = self.sc.GetValue()
        cels = round((fahr-32)*5/9.0, 2)
        self.celsius.SetLabel(str(cels))

    def OnClose(self, event):
        self.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        dlg = MyDialog(None, -1, 'spinctrl.py')
        dlg.Show(True)
        dlg.Centre()
        return True

app = MyApp(0)
app.MainLoop()