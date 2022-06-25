from __future__ import annotations

from threading import Thread, Lock
from time import sleep
from unittest import result
from winreg import SetValue

from matplotlib.pyplot import axes
from gui import GUI
import os
import widgets as widgets
from widgets import *
import window as window
from widgets import Tab
from PyQt5.QtWidgets import QListWidgetItem
from typing import Union
from dbClasses import *

from sqlalchemy import create_engine, extract
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import numpy as np
from sqlalchemy import Column, Integer, String, Date, SmallInteger, Table, Float, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    from _tabMethods import Mixin_TabMethods


class Mixin_Tab_1():

    def __init__(self:Union[SpotifyAnalyzer, Mixin_TabMethods]):
        print("tab1 init")
        self.queries[1] = self.query
        self.lock = Lock()
        self.plot_labels = []
        self.tab_1_widgets()
        self.tab_1_callbacks()

    def tab_1_widgets(self:Union[SpotifyAnalyzer, Mixin_TabMethods]):

        self.plot:MatplotlibFigure = self.tab_1.addWidget(MatplotlibFigure(self.mainWindow,"plot1"))
        self.ax = self.plot.addSubplot(1,1,1)
        self.button_plot:Button = self.tab_1.addWidget(Button(self.mainWindow,"pushButton_plot", self.plots))
        self.button_plot_clear:Button = self.tab_1.addWidget(Button(self.mainWindow,"pushButton_plot_clear", self.clearPlot))

        self.list_songs:ListWidget = self.tab_1.addWidget(ListWidget(self.mainWindow,"listWidget_song"))
        self.list_regions:ListWidget = self.tab_1.addWidget(ListWidget(self.mainWindow,"listWidget_region"))

        self.label_song:Label = self.tab_1.addWidget(Label(self.mainWindow,"label_song"))
        self.label_region:Label = self.tab_1.addWidget(Label(self.mainWindow,"label_region"))

        self.lineEdit_search_song:LineEdit = self.tab_1.addWidget(LineEdit(self.mainWindow,"lineEdit_search_song"))
        self.lineEdit_search_region:LineEdit = self.tab_1.addWidget(LineEdit(self.mainWindow,"lineEdit_search_region"))

        self.spinBox_year_start:SpinBox = self.tab_1.addWidget(SpinBox(self.mainWindow,"spinBox_year_start"))
        self.spinBox_year_end:SpinBox = self.tab_1.addWidget(SpinBox(self.mainWindow,"spinBox_year_end"))
        pass

    def tab_1_callbacks(self:SpotifyAnalyzer):
        self.list_songs.setCallbackClicked(lambda: self.label_song.setText(self.list_songs.getSelectedText()))
        self.list_regions.setCallbackClicked(lambda: self.label_region.setText(self.list_regions.getSelectedText()))
        self.spinBox_year_start.connectCallbackValueChanged(self.correctYearRange)
        self.spinBox_year_end.connectCallbackValueChanged(self.correctYearRange)
        self.lineEdit_search_song.setCallback(lambda filter: self.list_songs.filterItems(filter))
        self.lineEdit_search_region.setCallback(lambda filter: self.list_regions.filterItems(filter))
        pass

    def correctYearRange(self, year):
        if self.spinBox_year_start.value > self.spinBox_year_end.value:
            self.spinBox_year_end.setValue(self.spinBox_year_start.value)
        pass

    def clickedItem(self,item:QListWidgetItem):
            print(f"Clicked list item = [{item.text()}]")

    def query(self:SpotifyAnalyzer):
        
        q1 = self.session.query(Song.title
            ).filter(
            )

        q2 = self.session.query(Region.name
            ).filter(
            )

        thread_songs = Thread(target=self.threadQuery,args=(q1,'title',self.list_songs))
        thread_region = Thread(target=self.threadQuery,args=(q2,'name',self.list_regions))

        thread_songs.setDaemon(True)
        thread_region.setDaemon(True)

        thread_songs.start()
        thread_region.start()


    def threadQuery(self:SpotifyAnalyzer, q,column, target_list:ListWidget):
        df = pd.read_sql(q.statement, self.session.bind)
        items = df[column].values.tolist()
        target_list.addItems(items)

    def clearPlot(self):
        self.plot.clearFigure()
        self.plot_labels = []
        self.ax = self.plot.addSubplot(1,1,1)

    def plots(self):
        title = self.list_songs.getSelectedText()
        region = self.list_regions.getSelectedText()
        start = self.spinBox_year_start.value
        end = self.spinBox_year_end.value
        self.plot_labels.append(title+" in " +region)

        q = self.session.query(Day.date, Chart.position
            ).filter(
                Song.title == title,
                Song.song_id == Chart.song_id,
                Day.day_id == Chart.day_id,
                extract('year', Day.date) >= start,
                extract('year', Day.date) <= end,
                Region.name == region,
                Region.region_id == Chart.region_id,
                Category.name == "top200"
            )

        df = pd.read_sql(q.statement, self.session.bind)

        df.sort_values(by=['date'], inplace=True)
        dates = list(df.date)
        position = list(df.position)

        #self.plot.clearFigure()
        self.ax.plot(dates, position)
        self.ax.set_title('Trend in Top 200')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Position')
        #ax.set_ylim(0,200)
        self.ax.legend(self.plot_labels)
        self.plot.plotAxes()

        print(df)

        self.lineEdit_search_song.clear()
        self.lineEdit_search_region.clear()

        pass