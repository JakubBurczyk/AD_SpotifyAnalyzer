from __future__ import annotations
from gui import GUI
import os
import widgets as widgets
from widgets import *
import window as window
from widgets import Tab
from PyQt5.QtWidgets import QListWidgetItem
import _tabMethods as tabMethods

class SpotifyAnalyzer(GUI, tabMethods.Mixin_TabMethods):
    mainWindow: window.Window

    def __init__(self):
        super().__init__()
        tabMethods.Mixin_TabMethods.__init__(self)
        self.uisDir = os.path.abspath(os.path.join(os.path.realpath(__file__), "../"*2, "uis"))
        self.initWindows()
        self.initWidgets()
        self.initCallbacks()
        self.initTabs()

    def initWindows(self):
        self.mainWindow = self.addWindow("mainWindow","mainWindow.ui")    
        pass

    def initWidgets(self):
        self.mainTabWidget:TabWidget = self.mainWindow.addTabWidget("tabWidget_main")
        self.tab_0: Tab = self.mainTabWidget.addTab("tab_0",0)
        self.tab_1: Tab = self.mainTabWidget.addTab("tab_1",1)
        self.tab_2: Tab = self.mainTabWidget.addTab("tab_2",2)
        pass

    def initCallbacks(self):
        self.mainTabWidget.connectChange(self.changedTab)
    
    def hello(self):
        print(f"Hello ~[{type(self)}]")

    def start(self):
        if not self.mainWindow.isOpened:
            print("Opening main window")
            self.mainWindow.open()

        while self.isOpened:
            self.update()
        pass
    
    def changedTab(self,index):
        self.createEngine()
        self.queryTab(index)

if __name__ == "__main__":
    app = SpotifyAnalyzer()
    app.start()