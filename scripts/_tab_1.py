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
        self.queries[1] = self.tab_1_query
        self.t1_lock = Lock()
        self.t1_plot_labels = []
        self.tab_1_widgets()
        self.tab_1_callbacks()
        self.t1_queryInitalized = False

    def tab_1_widgets(self:Union[SpotifyAnalyzer, Mixin_TabMethods]):
        self.t1_plot:MatplotlibFigure = self.tab_1.addWidget(MatplotlibFigure(self.mainWindow, "plot1"))
        self.t1_ax = self.t1_plot.addSubplot(1, 1, 1)
        self.t1_button_plot:Button = self.tab_1.addWidget(Button(self.mainWindow, "pushButton_plot", self.tab_1_plots))
        self.t1_button_plot_clear:Button = self.tab_1.addWidget(Button(self.mainWindow, "pushButton_plot_clear", self.tab_1_clearPlot))

        self.t1_list_songs:ListWidget = self.tab_1.addWidget(ListWidget(self.mainWindow, "listWidget_song"))
        self.t1_list_regions:ListWidget = self.tab_1.addWidget(ListWidget(self.mainWindow, "listWidget_region"))

        self.t1_label_song:Label = self.tab_1.addWidget(Label(self.mainWindow, "label_song"))
        self.t1_label_region:Label = self.tab_1.addWidget(Label(self.mainWindow, "label_region"))

        self.t1_lineEdit_search_song:LineEdit = self.tab_1.addWidget(LineEdit(self.mainWindow, "lineEdit_search_song"))
        self.t1_lineEdit_search_region:LineEdit = self.tab_1.addWidget(LineEdit(self.mainWindow, "lineEdit_search_region"))

        self.t1_spinBox_year_start:SpinBox = self.tab_1.addWidget(SpinBox(self.mainWindow, "spinBox_year_start"))
        self.t1_spinBox_year_end:SpinBox = self.tab_1.addWidget(SpinBox(self.mainWindow, "spinBox_year_end"))
        pass

    def tab_1_callbacks(self:SpotifyAnalyzer):
        self.t1_list_songs.setCallbackClicked(lambda: self.t1_label_song.setText(self.t1_list_songs.getSelectedText()))
        self.t1_list_regions.setCallbackClicked(lambda: self.t1_label_region.setText(self.t1_list_regions.getSelectedText()))
        self.t1_spinBox_year_start.connectCallbackValueChanged(self.tab_1_correctYearRange)
        self.t1_spinBox_year_end.connectCallbackValueChanged(self.tab_1_correctYearRange)
        self.t1_lineEdit_search_song.setCallback(lambda filter: self.t1_list_songs.filterItems(filter))
        self.t1_lineEdit_search_region.setCallback(lambda filter: self.t1_list_regions.filterItems(filter))
        pass

    def tab_1_correctYearRange(self, year):
        if self.t1_spinBox_year_start.value > self.t1_spinBox_year_end.value:
            self.t1_spinBox_year_end.setValue(self.t1_spinBox_year_start.value)
        pass

    def tab_1_clickedItem(self, item:QListWidgetItem):
        print(f"Clicked list item = [{item.text()}]")

    def tab_1_query(self:SpotifyAnalyzer):
        if not self.t1_queryInitalized:
            q1 = self.session.query(Song.title).filter(
            )

            q2 = self.session.query(Region.name).filter(
            )

            thread_songs = Thread(target=self.threadQuery, args=(q1,'title',self.t1_list_songs))
            thread_region = Thread(target=self.threadQuery, args=(q2,'name',self.t1_list_regions))

            thread_songs.setDaemon(True)
            thread_region.setDaemon(True)

            thread_songs.start()
            thread_region.start()
            self.t1_initialized = True

    def tab_1_clearPlot(self):
        self.t1_plot.clearFigure()
        self.t1_plot_labels = []
        self.t1_ax = self.t1_plot.addSubplot(1, 1, 1)

    def tab_1_plots(self):
        title = self.t1_list_songs.getSelectedText()
        region = self.t1_list_regions.getSelectedText()
        start = self.t1_spinBox_year_start.value
        end = self.t1_spinBox_year_end.value
        self.t1_plot_labels.append(title + " in " + region)

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
            ).order_by(Day.date)

        df = pd.read_sql(q.statement, self.session.bind)

        #df.sort_values(by=['date'], inplace=True)
        dates = list(df.date)
        position = list(df.position)

        #self.plot.clearFigure()
        self.t1_ax.plot(dates, position)
        self.t1_ax.set_title('Trend in Top 200')
        self.t1_ax.set_xlabel('Date')
        self.t1_ax.set_ylabel('Position')
        self.t1_ax.tick_params(axis='x', labelrotation=45)
        #ax.set_ylim(0,200)
        self.t1_ax.legend(self.t1_plot_labels)
        self.t1_plot.plotAxes()

        self.t1_lineEdit_search_song.clear()
        self.t1_lineEdit_search_region.clear()

        pass