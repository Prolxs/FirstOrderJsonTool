import wx
import jsonread


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='114514', size=(800, 600))
        MainPanel = wx.Panel(self)
        self.Centre()
        self.ChoiceFile = wx.LoadFileSelector('nihao', parent=MainPanel, extension='.*', default_name='en_us.json')
        # print(self.ChoiceFile)
        # 选择部分
        self.StaText = wx.StaticText(MainPanel, label='选择目标文件')
        self.DownList = wx.Choice(MainPanel, size=(100, 23), choices=[str(x) for x in range(11)])
        self.DownList.SetColumns(n=10)
        self.ReloadButton = wx.Button(MainPanel, id=1, label='刷新')
        self.Pickup = wx.Button(MainPanel, id=2, label='提取')
        self.tip = wx.StaticText(MainPanel, label='选择文件')
        # JsonValue文本框
        self.JsonTitle = wx.StaticText(MainPanel, label='源文件')
        self.ShiftButton1 = wx.RadioButton(MainPanel, id=1, label='源文件', style=wx.RB_GROUP)
        self.ShiftButton2 = wx.RadioButton(MainPanel, id=2, label='值')
        self.JsonValue = wx.TextCtrl(MainPanel, id=-1, value='值', style=wx.TE_MULTILINE | wx.HSCROLL, size=(200, 300))
        # JsonClass
        self.JsonClassTitle = wx.StaticText(MainPanel, label='翻译内容')
        self.JsonClassValue = wx.TextCtrl(MainPanel, id=1, value='待翻译', style=wx.TE_MULTILINE | wx.HSCROLL,
                                          size=(200, 300))
        # TJson
        self.TJsonTitle = wx.TextCtrl(MainPanel, value='zh_ch.json')
        self.CreateButton = wx.Button(MainPanel, id=3, label='生成')
        self.TJsonValue = wx.TextCtrl(MainPanel, id=2, value='lang', style=wx.TE_MULTILINE | wx.HSCROLL,
                                      size=(200, 300))
        self.CreateFileBox = wx.BoxSizer()
        self.CreateFileBox.Add(self.TJsonTitle, proportion=0, flag=wx.TOP)
        self.CreateFileBox.Add(self.CreateButton, proportion=0, flag=wx.TOP)
        # 盒子管理器
        self.filebox = wx.BoxSizer()  # 水平盒子
        # 三个文本显示
        self.ShiftBox = wx.BoxSizer()
        self.JsonValueBox = wx.BoxSizer(wx.VERTICAL)  # 垂直盒子
        self.JsonClassBox = wx.BoxSizer(wx.VERTICAL)  # 垂直盒子
        self.TJsonBox = wx.BoxSizer(wx.VERTICAL)  # 垂直盒子
        self.JsonBox = wx.BoxSizer()
        # json盒子纵向管理
        self.ShiftBox.Add(self.JsonTitle, 0, flag=wx.LEFT, border=5)
        self.ShiftBox.Add(self.ShiftButton1, 0, flag=wx.LEFT, border=5)
        self.ShiftBox.Add(self.ShiftButton2, 0, flag=wx.LEFT, border=5)
        self.JsonValueBox.Add(self.ShiftBox, 0, flag=wx.LEFT)
        self.JsonValueBox.Add(self.JsonValue, 0, flag=wx.LEFT)
        self.JsonClassBox.Add(self.JsonClassTitle, 0, flag=wx.LEFT)
        self.JsonClassBox.Add(self.JsonClassValue, 0, flag=wx.LEFT)
        self.TJsonBox.Add(self.CreateFileBox, 0, flag=wx.LEFT)
        self.TJsonBox.Add(self.TJsonValue, 0, flag=wx.LEFT)
        # json盒子横向管理
        self.JsonBox.Add(self.JsonValueBox, 1, flag=wx.ALIGN_TOP | wx.LEFT | wx.RIGHT, border=10)
        self.JsonBox.Add(self.JsonClassBox, 0, flag=wx.ALIGN_TOP | wx.RIGHT | wx.LEFT, border=10)
        self.JsonBox.Add(self.TJsonBox, 1, flag=wx.ALIGN_TOP | wx.LEFT, border=10)

        self.VsizeBox = wx.BoxSizer(wx.VERTICAL)  # 垂直盒子
        # 水平盒子 第一行
        self.filebox.Add(self.StaText, 0, flag=wx.TOP | wx.LEFT, border=14)
        self.filebox.Add(self.DownList, 0, flag=wx.TOP | wx.LEFT, border=11)
        self.filebox.Add(self.ReloadButton, 0, flag=wx.TOP, border=10)
        self.filebox.Add(self.Pickup, 0, flag=wx.TOP, border=10)
        self.filebox.Add(self.tip, 0, flag=wx.TOP | wx.LEFT, border=14)
        self.VsizeBox.Add(self.filebox, 0, flag=wx.TOP | wx.LEFT)  # 垂直盒子
        self.VsizeBox.Add(self.JsonBox, 0, flag=wx.TOP, border=20)

        MainPanel.SetSizer(self.VsizeBox)
        self.Bind(wx.EVT_BUTTON, handler=self.OnButton, id=1, id2=3)
        self.Bind(wx.EVT_RADIOBUTTON, handler=self.OnShiftButton, id=1, id2=2)
        # self.Bind(wx.EVT_CHOICE, handler=self.OnChoice, source=self.DownList)

    def OnButton(self, event):
        EventId = event.GetId()
        EventObject = event.GetEventObject()
        json = jsonread.JsonRead()
        file = jsonread.OpenFile()
        if EventId == 1:  # 刷新
            n = 0
            for x in json.GetPathJsonValue():
                self.DownList.SetString(n=n, string=x)
                n += 1

        if EventId == 2:  # 提取
            self.DisplayerValue()

        if EventId == 3:
            filename = self.TJsonTitle.GetValue()  # 文件名
            filedata = self.JsonClassValue.GetValue()  # 数据
            try:
                filedir = file.GetFileValue(json.GetPathJsonDir()[self.DownList.GetStringSelection()], True)  # 获得源文件字典
                filedirkeys = list(filedir)
                filevalue = file.StringZList(filedata)  # 带\n的字符串转列表
                n = 0
                for x in filedirkeys:
                    try:
                        filedir[x] = filevalue[n]
                        n += 1
                    except IndexError:
                        break
                file.CreateFile(filename, filedir)
                self.TJsonValue.SetValue(file.DictZJson(filedir))
            except KeyError:
                self.tip.SetLabelText('请先先提取')
                print('请先先提取')

    def OnShiftButton(self, event):
        EventId = event.GetId()
        if EventId == 1:
            self.DisplayerValue()
        if EventId == 2:
            self.DisplayerValue2()

    def DisplayerValue(self):
        file = jsonread.OpenFile()
        json = jsonread.JsonRead()
        try:
            value = file.GetFileValue(json.GetPathJsonDir()[self.DownList.GetStringSelection()], None)
            self.JsonValue.SetValue(value)
        except KeyError:
            self.tip.SetLabelText('重新选择文件！')
            print('重新选择文件！')

    def DisplayerValue2(self):
        file = jsonread.OpenFile()
        json = jsonread.JsonRead()
        self.JsonValue.SetValue('\0')
        try:
            value = file.GetFileValue(json.GetPathJsonDir()[self.DownList.GetStringSelection()], True)
            list1 = list(value)
            for x in list1:
                self.JsonValue.write(value[x] + '\n')
        except KeyError:
            self.tip.SetLabelText('重新选择文件！')
            print('重新选择文件！')


class app(wx.App):
    def __init__(self):
        super().__init__()

    def OnPreInit(self):
        frame = MyFrame()
        frame.Show()
        return
