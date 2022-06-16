from __future__ import annotations

from gui import GUI
import os
import widgets as widgets
from widgets import *
import window as window
from widgets import Tab
from PyQt5.QtWidgets import QListWidgetItem

from _tab_1 import Mixin_Tab_1
from _tab_2 import Mixin_Tab_2

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    

class Mixin_TabMethods(Mixin_Tab_1,Mixin_Tab_2):

    def initTab1(self:SpotifyAnalyzer):
        self.tab_1_widgets()
        self.tab_1_callbacks()
        pass

    def initTab2(self:SpotifyAnalyzer):
        self.tab_2_widgets()
        self.tab_2_callbacks()

        