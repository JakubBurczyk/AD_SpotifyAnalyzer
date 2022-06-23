from __future__ import annotations
import datetime
from tkinter.messagebox import NO
from turtle import end_fill

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import widgets as widgets
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import *
from PyQt5 import QtWidgets, uic, QtGui
import sys
import random
from termcolor import colored
import numpy as np
from typing import Callable, Iterable, List, Dict

import os
from abc import ABC, abstractclassmethod
import window as window


class Widget(ABC):

    def __init__(self, win:window.Window, name: str):
        self._window = win
        self._name = name
        self._widget = self.find(self._window, self._name)
        self.updatable = False
        pass

    def disable(self) -> None:
        self._widget.setEnabled(False)
        return self
        pass

    def enable(self) -> None:
        self._widget.setEnabled(True)
        return self
        pass

    def setEnabled(self, state: bool):
        self._widget.setEnabled(state)
        return self
        pass

    def toggleEnable(self) -> bool:
        """
        Switch button on/off
        :return: bool, Returns resultant state of the button
        """
        state = self.enabled
        self.setEnabled(not state)
        return self.enabled
        pass
    
    @staticmethod
    def find(win: window.Window, name:str):
        return getattr(win, name)
        pass

    def update(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def widget(self):
        return self._widget
        pass

    @property
    def enabled(self):
        return self._widget.isEnabled()
        pass


class Button(Widget):
    _widget: QPushButton

    def __init__(self, win:window.Window, name: str, function: Callable = None):
        super(Button, self).__init__(win, name)
        if function is not None:
            self.setCallback(function)
        pass

    def setCallback(self, callback:Callable):
        self._widget.clicked.connect(callback)

    def update(self):
        print(f"Debug update [{self.name}]")

class Label(Widget):
    _widget: QLabel

    def __init__(self, win: window.Window, name: str):
        super().__init__(win, name)
    
    def setText(self, text:str):
        self._widget.setText(text)

class LineEdit(Widget):
    _widget: QLineEdit

    def __init__(self, win: window.Window, name: str):
        super().__init__(win, name)
    
    def setCallback(self, callback:Callable):
        self._widget.textChanged.connect(callback)

    def clear(self):
        self._widget.clear()
    
    @property
    def text(self):
        return self._widget.text()
    

class SpinBoxAbstract(Widget):
    _widget: QSpinBox

    def __init__(self, win:window.Window, name: str):
        super(SpinBoxAbstract, self).__init__(win, name)
        pass

    def setValue(self, value):
        self._widget.setValue(value)

    def connectCallbackValueChanged(self, callback:Callable):
        self._widget.valueChanged.connect(callback)

    @property
    def value(self):
        return self._widget.value()
        pass


class SpinBox(SpinBoxAbstract):
    _widget: QSpinBox
    value: int

    def __init__(self, win:window.Window, name: str):
        super(SpinBox, self).__init__(win, name)


class DoubleSpinBox(SpinBoxAbstract):
    _widget: QDoubleSpinBox
    value: float

    def __init__(self, win:window.Window, name: str):
        super(DoubleSpinBox, self).__init__(win, name)
        pass


class Pixmap(Widget):
    _widget: QLabel

    def __init__(self, win:window.Window, name: str, imgPath):
        super(Pixmap, self).__init__(win, name)
        self.imgPath = imgPath
        self.pixmap = QPixmap(self.imgPath)
        self._widget.setPixmap(self.pixmap)
        self._widget.setScaledContents(True)

        self.frequency = 1  # Hz
        self.updateDt = 1 / self.frequency
        self.lastUpdate = datetime.datetime.now()
        self.updatable = False
        pass

    def update(self):
        dt_ms = (datetime.datetime.now() - self.lastUpdate).total_seconds()
        if dt_ms >= self.updateDt:
            self.pixmap = QPixmap(self.imgPath)
            self._widget.setPixmap(self.pixmap)
            self._widget.setScaledContents(True)
        else:
            pass


class LCD(Widget):
    _widget: QLCDNumber
    getValue: Callable

    def __init__(self, win:window.Window, name: str):
        super(LCD, self).__init__(win, name)

        self._value = 0
        self.frequency = 1 #Hz
        self.updateDt = 1/self.frequency
        self.lastUpdate = datetime.datetime.now()
        self.getValue = None
        self.updatable = False
        pass

    def setCallback(self, function: Callable):
        self.getValue = function
        pass

    def setValue(self, value):
        #print(f"LCD: {self.name} displaying: {self.value}")
        self._value = value
        self.updateable = True
        pass

    def display(self, value):
        #print(f"LCD: {self.name} displaying: {self.value}")
        if isinstance(value, np.ndarray):
            vlist = value.tolist()
            if len(vlist) > 0:
                value = vlist[0]
            else:
                value = 0

        self._widget.display(value)
        pass

    def update(self):
        dt_ms = (datetime.datetime.now() - self.lastUpdate).total_seconds()
        if dt_ms >= self.updateDt:
            if self.getValue is not None:
                self._value = self.getValue()
                self.lastUpdate = datetime.datetime.now()

            self.display(self.value)
        else:
            pass

    #@property
    #def updateable(self):
    #    print(self.name, self.getValue is not None)
    #    return self.getValue is not None
    #    pass

    @property
    def value(self):
        return self._value
        pass

class TextBrowser(Widget):
    _widget:QTextBrowser

    def __init__(self, win: window.Window, name: str):
        super().__init__(win, name)
        self.savedItems = None
        pass

    def setText(self, text:str):
        self._widget.setText(text)
        pass

    def appendLine(self, line):
        if isinstance(line, str):
            self._widget.append(line)
        elif isinstance(line, List):
            for l in line:
                self._widget.append(l)
        try:
            self._widget.verticalScrollBar().setValue(self._widget.verticalScrollBar().maximum())
            pass
        except:
            pass
        
        pass

    def appendLineTimed(self, line):
        if isinstance(line, str):
            self.appendLine(f"[{datetime.datetime.now()}] {line}")
        else:
            self.appendLine(f"[{datetime.datetime.now()}]")
            self.appendLine(line)


    def clear(self):
        self._widget.clear()
        pass


class ListWidget(Widget):
    _widget: QListWidget

    def __init__(self, win: window.Window, name: str):
        super().__init__(win, name)
        #self._widget.addItems([f"pos {v}" for v in range(20)])

    def addItems(self, items:Iterable[str]):
        if isinstance(items, Iterable[str]):
            self._widget.addItems(items)
        return self

    def addItem(self, item:str):
        if isinstance(item, str):
            self._widget.addItem(item)
        return self

    def setCallbackClicked(self, callback:Callable):
        self._widget.itemClicked.connect(callback)
        return self

    def setCallbackDoubleClicked(self, callback:Callable):
        self._widget.itemDoubleClicked.connect(callback)
        return self

    def getItems(self) -> List[QListWidgetItem]:
        #items = self._widget.items()
        items = []
        for index in range(self._widget.count()):
            items.append(self._widget.item(index))
        return items

    def saveItems(self):
        self.savedItems = self.getItems()
    
    def restoreItems(self):
        if self.savedItems is not None:
            self._widget.clear()
            self._widget.addItmes(self.savedItems)
        pass
    
    def unhideAll(self):
        for item in self.getItems():
            item.setHidden(False)
        pass

    def filterItems(self,filterText:str):
        item:QListWidgetItem
        for item in self.getItems():
            hidden = filterText.lower() not in item.text().lower()
            item.setHidden(hidden)
        pass

    def getItemsText(self):
        item: QListWidgetItem
        itemsText = []
        for item in self.getItems():
            itemsText.append(item.text())
        return itemsText
    
    def getSelected(self) -> QListWidgetItem:
        if self._widget.selectedItems() != []:
            return self._widget.selectedItems()[0]
        else:
            return None

    def getSelectedText(self) -> str:
        #print(self.getSelected())
        selected = self.getSelected()
        if selected is not None:
            return selected.text()
        else:
            return None

    def clear(self):
        self._widget.clear()




class Tab(Widget):
    
    def __init__(self, win: window.Window, name: str, index:int):
        super().__init__(win, name)
        self.index = index
        self._widgets: Dict[str, Widget] = {}
        pass

    def addWidget(self, widget:Widget):
        self._widgets[widget.name] = widget
        return widget
        pass

    def update(self):
        widget: Widget
        for name, widget in self._widgets.items():
            if widget.updatable:
                widget.update()
        pass


class TabWidget(Widget):
    _widget = QTabWidget
    tabs = Dict[int, Tab]

    def __init__(self, win: window.Window, name: str):
        super().__init__(win, name)
        self.tabs: Dict[int, Tab] = {}
        self.updatable = False
        
        pass

    def connectChange(self, callback:Callable):
        self._widget.currentChanged.connect(callback)
    
    def addTab(self,name: str, index: int) -> widgets.Tab:
        self.tabs[index] = Tab(self._window, name, index)
        return self.tabs[index]

    def addToTab(self,tab, widget):
        target_tab:Tab = None

        if isinstance(tab,Tab):
            target_tab = tab
        elif isinstance(tab,str):
            target_tab = self.tabs[tab]

        if target_tab is None:
            raise Exception("No target tab")
        else:
            target_widget:Widget = None

            if isinstance(widget, Widget):
                target_widget = widget
            elif isinstance(widget, str):
                target_widget = Widget.find(self._window, widget)

            if target_widget is None:
                raise Exception("No target widget to add to tab")
            else:
                target_tab.addWidget(target_widget)
        
        return target_widget

    def currentIndex(self) -> int:
        return self._widget.currentIndex()
        pass

    def indexOf(self,name:str):
        idx = -1
        if name in self.tabs:
            tab:Tab = self.tabs[name]
            idx = tab.index
        return idx 
        pass

    def updateCurrentTab(self):
        currentIndex = self.currentIndex()
        tab: Tab
        for index, tab in self.tabs.items():
            if tab.updatable and tab.index == currentIndex:
                #print(f"Current tab [{currentIndex}] Updtbl [{tab.updatable}] Tab idx [{tab.index}]")
                tab.update()
            pass
        pass
    
    def update(self):
        if self.updatable:
            self.updateCurrentTab()


class MatplotlibFigure(Widget):
    _widget:QVBoxLayout

    def __init__(self, win: window.Window, name: str):
        super().__init__(win, name)
        plt.style.use('dark_background')
        
        self.figure = plt.figure()
        self.figure.set_facecolor("none")

        self.canvas = FigureCanvas(self.figure)
        
        self.toolbar = NavigationToolbar(self.canvas, win)
        
        self._widget.addWidget(self.canvas)
        self._widget.addWidget(self.toolbar)

    def addSubplot(self,row,col,idx):
        ax = self.figure.add_subplot(row,col,idx)
        ax.set_facecolor("none")
        return ax
        pass

    def clearFigure(self):
        self.figure.clear()
        self.figure.tight_layout()
        
    def plotAxes(self):
        plt.tight_layout()
        self.canvas.draw()
        pass

    def plotRandom(self):
        data = [random.random() for i in range(10)]
        self.figure.clear()
        self.figure.tight_layout()
        ax = self.figure.add_subplot(1,1,1)
        ax.set_facecolor("none")
        ax.plot(data, 'o-')
        plt.tight_layout()
        self.canvas.draw()
