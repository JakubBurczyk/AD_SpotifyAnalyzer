from __future__ import annotations

from grpc import Call

from gui import GUI
import os
import widgets as widgets
from widgets import *
import window as window
from widgets import Tab
from PyQt5.QtWidgets import QListWidgetItem

from _tab_0 import Mixin_Tab_0
from _tab_1 import Mixin_Tab_1
from _tab_2 import Mixin_Tab_2

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    

class Mixin_TabMethods(Mixin_Tab_0, Mixin_Tab_1, Mixin_Tab_2):
    def __init__(self) -> None:
        print("Mixin init")
        self.queries: dict(int,Callable) = {}
        self.initTabs()
        pass

    def initTabs(self):
        Mixin_Tab_0.__init__(self)
        Mixin_Tab_1.__init__(self)
        Mixin_Tab_2.__init__(self)
        pass

    def queryTab(self:SpotifyAnalyzer,index):
        if index in self.queries:
            self.queries[index]()
        pass
        