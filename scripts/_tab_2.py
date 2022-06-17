from __future__ import annotations

from gui import GUI
import os
import widgets as widgets
from widgets import *
import window as window
from widgets import Tab
from PyQt5.QtWidgets import QListWidgetItem

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    from _tabMethods import Mixin_TabMethods


class Mixin_Tab_2():

    def tab_2_widgets(self:SpotifyAnalyzer):
        self.Button2:Button = self.tab_2.addWidget(Button(self.mainWindow,"pushButton_2",self.pshButton2))
        pass

    def tab_2_callbacks(self:SpotifyAnalyzer):
        pass

    def pshButton2(self:SpotifyAnalyzer):
        print("Button 2")
        self.hello()
    pass