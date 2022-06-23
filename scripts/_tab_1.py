from __future__ import annotations

from threading import Thread, Lock
from winreg import SetValue
from gui import GUI
import os
import widgets as widgets
from widgets import *
import window as window
from widgets import Tab
from PyQt5.QtWidgets import QListWidgetItem
from typing import Union
from dbClasses import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    from _tabMethods import Mixin_TabMethods


class Mixin_Tab_1():

    def __init__(self:Union[SpotifyAnalyzer, Mixin_TabMethods]):
        print("tab1 init")
        self.queries[1] = self.query
        self.lock = Lock()

        self.tab_1_widgets()
        self.tab_1_callbacks()

    def tab_1_widgets(self:Union[SpotifyAnalyzer, Mixin_TabMethods]):
        self.button_plot:Button = self.tab_1.addWidget(Button(self.mainWindow,"pushButton_plot", self.pshButton)).disable()
        self.list_songs:ListWidget = self.tab_1.addWidget(ListWidget(self.mainWindow,"listWidget"))
        self.plot:MatplotlibFigure = self.tab_1.addWidget(MatplotlibFigure(self.mainWindow,"plot1"))
        self.label_song:Label = self.tab_1.addWidget(Label(self.mainWindow,"label_song"))
        self.lineEdit_search:LineEdit = self.tab_1.addWidget(LineEdit(self.mainWindow,"lineEdit_search"))
        self.spinBox_year_start:SpinBox = self.tab_1.addWidget(SpinBox(self.mainWindow,"spinBox_year_start"))
        self.spinBox_year_end:SpinBox = self.tab_1.addWidget(SpinBox(self.mainWindow,"spinBox_year_end"))
        pass

    def tab_1_callbacks(self:SpotifyAnalyzer):
        self.list_songs.setCallbackClicked(lambda: self.label_song.setText(self.list_songs.getSelectedText()))
        self.spinBox_year_start.connectCallbackValueChanged(self.correctYearRange)
        self.spinBox_year_end.connectCallbackValueChanged(self.correctYearRange)
        self.lineEdit_search.setCallback(lambda filter: self.list_songs.filterItems(filter))
        pass

    def correctYearRange(self, year):
        if self.spinBox_year_start.value > self.spinBox_year_end.value:
            self.spinBox_year_end.setValue(self.spinBox_year_start.value)
        pass

    def clickedItem(self,item:QListWidgetItem):
            print(f"Clicked list item = [{item.text()}]")

    def query(self:SpotifyAnalyzer):
        thread = Thread(target=self.threadQuery,args=(Song,self.lock))
        thread.start()
        
        
    def threadQuery(self, type, lock:Lock):
        print("Starting thread query")
        session_stmt = self.session.query(type)
        session_results = session_stmt.all()
        try:
            for result in session_results:
                self.list_songs.addItem(bytes(result.title, 'utf-16').decode('utf-16', 'ignore'))
                pass
            pass
        except:
            pass

        self.lock.acquire()
        self.button_plot.enable()
        self.lock.release()

    def pshButton(self):
        self.plot.clearFigure()
        ax = self.plot.addSubplot(1,1,1)
        ax.plot([1,2,3],[1,4,9])
        self.plot.plotAxes()
        self.lineEdit_search.clear()
        pass