from __future__ import annotations

from threading import Thread, Lock
from gui import GUI
import os
import widgets as widgets
from widgets import *
import window as window
from widgets import Tab
from PyQt5.QtWidgets import QListWidgetItem
from typing import Union
from dbClasses import *
import pandas as pd
from sqlalchemy.sql import func
from sqlalchemy import extract
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    from _tabMethods import Mixin_TabMethods


class Mixin_Tab_3():

    def __init__(self:Union[SpotifyAnalyzer, Mixin_TabMethods]):
        print("tab3 init")
        self.queries[3] = self.tab_3_query
        self.t3_lock = Lock()
        self.tab_3_widgets()
        self.tab_3_callbacks()
        self.t3_queryInitalized = False

    def tab_3_widgets(self:SpotifyAnalyzer):
        self.t3_plot:MatplotlibFigure = self.tab_3.addWidget(MatplotlibFigure(self.mainWindow, "plot3"))
        self.t3_ax = self.t3_plot.addSubplot(1, 1, 1)

        self.t3_button_plot:Button = self.tab_3.addWidget(Button(self.mainWindow,"pushButton_plot_5",self.tab_3_plots))
        self.t3_button_clear:Button = self.tab_3.addWidget(Button(self.mainWindow,"pushButton_plot_clear_5",self.tab_3_clearPlot))

        self.t3_list_songs:ListWidget = self.tab_3.addWidget(ListWidget(self.mainWindow, "listWidget_song_5"))

        self.t3_lineEdit_search_song:LineEdit = self.tab_3.addWidget(LineEdit(self.mainWindow, "lineEdit_search_song_5"))
        
        self.t3_spinBox_year_start:SpinBox = self.tab_3.addWidget(SpinBox(self.mainWindow, "spinBox_year_start_3"))
        self.t3_spinBox_year_end:SpinBox = self.tab_3.addWidget(SpinBox(self.mainWindow, "spinBox_year_end_3"))
        pass

    def tab_3_callbacks(self:SpotifyAnalyzer):
        #self.t2_list_artists.setCallbackClicked(lambda: self.t1_label_song.setText(self.t1_list_songs.getSelectedText()))
        self.t3_lineEdit_search_song.setCallback(lambda filter: self.t3_list_songs.filterItems(filter))
        self.t3_spinBox_year_start.connectCallbackValueChanged(self.tab_3_correctYearRange)
        self.t3_spinBox_year_end.connectCallbackValueChanged(self.tab_3_correctYearRange)
        pass

    def tab_3_correctYearRange(self, year):
        if self.t3_spinBox_year_start.value > self.t3_spinBox_year_end.value:
            self.t3_spinBox_year_end.setValue(self.t3_spinBox_year_start.value)
        pass

    def tab_3_query(self):
        if not self.t3_queryInitalized:
            q1 = self.session.query(Song.title).filter(
            )

            thread_songs = Thread(target=self.threadQuery, args=(q1,'title',self.t3_list_songs))
            thread_songs.setDaemon(True)
            thread_songs.start()
            self.t3_queryInitalized = True
        pass

    def tab_3_plots(self:SpotifyAnalyzer):
        title = self.t3_list_songs.getSelectedText()
        start  = self.t3_spinBox_year_start.value
        end = self.t3_spinBox_year_end.value

        q = self.session.query(Region.name, func.sum(Chart.streams)).filter(
                Song.title == title,
                Song.song_id == Chart.song_id,
                Region.region_id == Chart.region_id,
                Day.day_id == Chart.day_id,
                extract('year', Day.date) >= start,
                extract('year', Day.date) <= end,
                Chart.category_id == Category.category_id,
                Category.name == "top200"
            ).group_by(Region.name).order_by(func.sum(Chart.streams).desc())

        df = pd.read_sql(q.statement, self.session.bind)

        df['percent_val'] = df['sum_1']/df['sum_1'].sum()
        df['name'] = df.apply(lambda x: x['name'] if x['percent_val'] >= .01 else 'Other', axis=1)
        df = df.groupby('name')['percent_val'].sum().reset_index().round(3).sort_values(by='percent_val', ascending=False)
        df.reset_index(drop=True, inplace=True)

        self.tab_3_clearPlot()
        patches, texts, autotexts = self.t3_ax.pie(df.percent_val, labels = df.name, autopct='%1.1f%%', startangle = 225)
        [autotext.set_color('black') for autotext in autotexts]
        self.t3_ax.grid()
        self.t3_ax.set_title(f"Streams of {title} by region from {start} to {end}")

        self.t3_plot.plotAxes()
        self.t3_lineEdit_search_song.clear()
        pass

    def tab_3_clearPlot(self:SpotifyAnalyzer):
        self.t3_plot.clearFigure()
        self.t3_ax = self.t3_plot.addSubplot(1, 1, 1)
        pass

    pass