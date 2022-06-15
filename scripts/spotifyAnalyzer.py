from gui import GUI
import os
import widgets as widgets
from widgets import *
import window as window
from widgets import Tab
from PyQt5.QtWidgets import QListWidgetItem

class SpotifyAnalyzer(GUI):
    mainWindow: window.Window
    mainTabWidget: TabWidget

    def __init__(self):
        super().__init__()
        self.uisDir = os.path.abspath(os.path.join(os.path.realpath(__file__), "../"*2, "uis"))
        self.initWindows()
        self.initWidgets()
        self.initCallbacks()

    def initWindows(self):
        self.mainWindow = self.addWindow("mainWindow","mainWindow.ui")    
        pass

    def initWidgets(self):
        self.mainTabWidget:TabWidget = self.mainWindow.addTabWidget("tabWidget_main")
        self.tab_0: Tab = self.mainTabWidget.addTab("tab_0",0)
        self.tab_1: Tab = self.mainTabWidget.addTab("tab_1",1)

        self.Button1:Button = self.mainTabWidget.addToTab(self.tab_0, widgets.Button(self.mainWindow,"pushButton", self.pshButton))
        self.Button2:Button = self.mainTabWidget.addToTab(self.tab_1, widgets.Button(self.mainWindow,"pushButton_2",self.pshButton2))
        
        self.List1:ListWidget = self.mainTabWidget.addToTab(self.tab_0, widgets.ListWidget(self.mainWindow,"listWidget"))
        
        self.Plot1:MatplotlibFigure = self.mainTabWidget.addToTab(self.tab_0, widgets.MatplotlibFigure(self.mainWindow,"plot1"))
        self.Label1:Label = self.mainTabWidget.addToTab(self.tab_0, widgets.Label(self.mainWindow,"label"))
        pass

    def initCallbacks(self):
        self.List1.setCallbackClicked(lambda: self.Label1.setText(self.List1.getSelectedText()))

    def pshButton(self):
        print("Button 1")
        self.Plot1.plotRandom()

    def pshButton2(self):
        print("Button 2")

    def clickedItem(self,item:QListWidgetItem):
        print(f"Clicked list item = [{item.text()}]")

    def start(self):
        if not self.mainWindow.isOpened:
            print("Opening main window")
            self.mainWindow.open()

        while self.isOpened:
            self.update()
        pass

    pass


if __name__ == "__main__":
    app = SpotifyAnalyzer()
    app.start()