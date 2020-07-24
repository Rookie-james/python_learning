import wx
import wx.lib.buttons as wxbutton
# import os
import subprocess
#import win32api

class MainFrame(wx.Frame):
    def __init__(
            self, parent=None, id=-1, title='', size=(600,400),
            style=wx.DEFAULT_FRAME_STYLE ^ (wx.MAXIMIZE_BOX | wx.RESIZE_BORDER), UpdateUI=None
    ):
        wx.Frame.__init__(self, parent, id, title=title, size=size, style=style)

        self.data = []  # 数据初始化
        self.UpdateUI = UpdateUI
        self.InitUI()  # 绘制UI界面
        self.Center()

    def InitUI(self):
        # 绘制面板
        self.panel = wx.Panel(self)
        # 软件图标
        self.Buttons()
        # 控件容器
        self.Boxsizer()
        # 程序事件处理
        self.Event_deal()


    def Buttons(self):
        '按钮控件初始化'
        self.button_SNchange = wxbutton.GenButton(self.panel, -1, 'SNchange',pos=(20, 20))
        self.button_upScript = wxbutton.GenButton(self.panel, -1, 'upScript',pos=(130, 20))
        self.button_Obs = wxbutton.GenButton(self.panel, -1, 'Obstacle',pos=(240, 20))
        self.button_notebook = wxbutton.GenButton(self.panel, -1, 'Notebook', pos=(350, 20))
        self.button_calc = wxbutton.GenButton(self.panel, -1, 'Calculator', pos=(460, 20))
        self.button_hydra = wxbutton.GenButton(self.panel, -1, 'Hydra', pos=(20, 70))
        self.button_notepad2 = wxbutton.GenButton(self.panel, -1, 'Notepad++', pos=(130, 70))
        self.button_upgradetool2 = wxbutton.GenButton(self.panel, -1, 'UpgradeTool2', pos=(240, 70))
        self.button_capture = wxbutton.GenButton(self.panel, -1, 'Capture', pos=(350, 70))
        self.button_aegisub = wxbutton.GenButton(self.panel, -1, 'Aegisub', pos=(460, 70))

    def Boxsizer(self):
    #     '容器设定'
        box = wx.BoxSizer(wx.HORIZONTAL)  # 放置水平的box sizer
        # box.Add(self.button_SNchange, 0, wx.ALL, 10)
        # box.Add(self.button_upScript, 0, wx.ALL, 10)
        # box.Add(self.button_Obs, 0, wx.ALL, 10)
        # box.Add(self.button_Jsb, 0, wx.ALL, 10)
        # box.Add(self.button_calc, 0, wx.ALL, 10)
        # box.Add(self.button_hydra, 0, wx.ALL, 10)
        # box.Add(self.button_notepad2, 0, wx.ALL, 10)
        self.panel.SetSizerAndFit(box)

    def Event_deal(self):
        '程序事件处理'
        self.Bind(wx.EVT_BUTTON, self.SNchange, self.button_SNchange)
        self.Bind(wx.EVT_BUTTON, self.upScript, self.button_upScript)
        self.Bind(wx.EVT_BUTTON, self.Obstacle, self.button_Obs)
        self.Bind(wx.EVT_BUTTON, self.Notebook, self.button_notebook)
        self.Bind(wx.EVT_BUTTON, self.Calculator, self.button_calc)
        self.Bind(wx.EVT_BUTTON, self.Hydra, self.button_hydra)
        self.Bind(wx.EVT_BUTTON, self.Notepad2, self.button_notepad2)
        self.Bind(wx.EVT_BUTTON, self.UpgradeTool2, self.button_upgradetool2)
        self.Bind(wx.EVT_BUTTON, self.Capture, self.button_capture)
        self.Bind(wx.EVT_BUTTON, self.Aegisub, self.button_aegisub)

    def SNchange(self,event):
        subprocess.call('Write_PN_SN_V0.2\Write_PN_SN_V0.2.exe')

    def upScript(self,event):
        subprocess.call('UpdateTestTool_v0.3\\tools_to_upgrade.exe')

    def Obstacle(self,event):
        subprocess.call("E:\workspace\SDK\ObstacleInfoDemo.exe")

    def Notebook(self,event):
        subprocess.call("C:\windows\system32\\notepad.exe")

    def Calculator(self,event):
        subprocess.call("C:\Windows\System32\calc.exe")

    def Hydra(self,event):
        subprocess.call("D:\Program Files\SmarterEye\Hydra\Hydra.exe")

    def Notepad2(self,event):
        subprocess.call("C:\Program Files (x86)\\Notepad++\\notepad++.exe")

    def UpgradeTool2(self,event):
        subprocess.call("C:\Program Files\SmarterEye\\UpdateCameraTool\\UpdateCameraTool.exe")

    def Capture(self,event):
        subprocess.call("D:\Program Files (x86)\录屏工具\Captura\Captura.UI.exe")

    def Aegisub(self,event):
        subprocess.call("C:\Program Files\Aegisub\\aegisub64.exe")

if __name__ == '__main__':
    app=wx.App()
    frame=MainFrame(parent=None,id=-1,title='Test Tool')
    frame.Show()
    app.MainLoop()