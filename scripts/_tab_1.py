from __future__ import annotations

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
        self.queries[1] = self.query

    def tab_1_widgets(self:Union[SpotifyAnalyzer, Mixin_TabMethods]):
        self.Button1:Button = self.tab_1.addWidget(Button(self.mainWindow,"pushButton", self.pshButton))
        self.List1:ListWidget = self.tab_1.addWidget(ListWidget(self.mainWindow,"listWidget"))
        self.Plot1:MatplotlibFigure = self.tab_1.addWidget(MatplotlibFigure(self.mainWindow,"plot1"))
        self.Label1:Label = self.tab_1.addWidget(Label(self.mainWindow,"label"))
        self.LineEdit1:LineEdit = self.tab_1.addWidget(LineEdit(self.mainWindow,"lineEdit"))
        self.spinBox1:SpinBox = self.tab_1.addWidget(SpinBox(self.mainWindow,"spinBox"))

       
        pass

    def tab_1_callbacks(self:SpotifyAnalyzer):
        self.List1.setCallbackClicked(lambda: self.Label1.setText(self.List1.getSelectedText()))
        self.spinBox1.connectCallbackValueChanged(lambda: print(f"Spinbox val changed to {self.spinBox1.value}"))
        self.LineEdit1.setCallback(lambda filter: self.List1.filterItems(filter))
        pass

    def clickedItem(self,item:QListWidgetItem):
            print(f"Clicked list item = [{item.text()}]")

    def query(self:SpotifyAnalyzer):
        session_stmt = self.session.query(Artist)
        session_results = session_stmt.all()
        for result in session_results:
            self.List1.addItem(result.name)
        pass

    def pshButton(self):
        self.Plot1.clearFigure()
        ax = self.Plot1.addSubplot(1,1,1)
        ax.plot([1,2,3],[1,4,9])
        self.Plot1.plotAxes()
        self.LineEdit1.clear()
        pass