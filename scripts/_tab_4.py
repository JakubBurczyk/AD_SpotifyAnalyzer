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
from wordcloud import WordCloud

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    from _tabMethods import Mixin_TabMethods

import globals

class Mixin_Tab_4():

    def __init__(self:Union[SpotifyAnalyzer, Mixin_TabMethods]):
        print("tab4 init")
        self.queries[4] = self.tab_4_query
        self.t4_lock = Lock()
        self.tab_4_widgets()
        self.tab_4_callbacks()
        self.t4_queryInitalized = False
        self.category = globals.CATEGORY_200

    def tab_4_widgets(self:SpotifyAnalyzer):
        self.t4_plot:MatplotlibFigure = self.tab_4.addWidget(MatplotlibFigure(self.mainWindow, "plot5"))
        self.t4_ax = self.t4_plot.addSubplot(1, 1, 1)

        self.t4_button_plot:Button = self.tab_4.addWidget(Button(self.mainWindow,"pushButton_plot_6",self.tab_4_plots))
        self.t4_button_clear:Button = self.tab_4.addWidget(Button(self.mainWindow,"pushButton_plot_clear_6",self.tab_4_clearPlot))
        self.t4_button_category:Button = self.tab_4.addWidget(Button(self.mainWindow,"pushButton_category_5",self.tab_4_switch_category))

        self.t4_label_category:Label = self.tab_4.addWidget(Label(self.mainWindow,"label_category_5"))

        self.t4_list_regions:ListWidget = self.tab_4.addWidget(ListWidget(self.mainWindow, "listWidget_region_5"))

        self.t4_lineEdit_search_region:LineEdit = self.tab_4.addWidget(LineEdit(self.mainWindow, "lineEdit_search_region_5"))
        
        self.t4_spinBox_year_start:SpinBox = self.tab_4.addWidget(SpinBox(self.mainWindow, "spinBox_year_start_5"))
        self.t4_spinBox_year_end:SpinBox = self.tab_4.addWidget(SpinBox(self.mainWindow, "spinBox_year_end_5"))
        self.t4_spinBox_limit_artists:SpinBox = self.tab_4.addWidget(SpinBox(self.mainWindow, "spinBox_limit_artists_5"))
        pass

    def tab_4_callbacks(self:SpotifyAnalyzer):
        #self.t2_list_artists.setCallbackClicked(lambda: self.t1_label_song.setText(self.t1_list_songs.getSelectedText()))
        self.t4_lineEdit_search_region.setCallback(lambda filter: self.t4_list_regions.filterItems(filter))
        self.t4_spinBox_year_start.connectCallbackValueChanged(self.tab_4_correctYearRange)
        self.t4_spinBox_year_end.connectCallbackValueChanged(self.tab_4_correctYearRange)
        pass

    def tab_4_correctYearRange(self, year):
        if self.t4_spinBox_year_start.value > self.t4_spinBox_year_end.value:
            self.t4_spinBox_year_end.setValue(self.t4_spinBox_year_start.value)
        pass

    def tab_4_query(self):
        if not self.t4_queryInitalized:
            q1 = self.session.query(Region.name).filter(
            )

            thread_songs = Thread(target=self.threadQuery, args=(q1,'name',self.t4_list_regions))
            thread_songs.setDaemon(True)
            thread_songs.start()
            self.t4_queryInitalized = True
        pass

    def tab_4_switch_category(self:SpotifyAnalyzer):
        self.category = self.switch_category(self.category)
        self.t4_label_category.setText(self.category)
        pass

    def tab_4_plots(self:SpotifyAnalyzer):
        
        region = self.t4_list_regions.getSelectedText()
        start  = self.t4_spinBox_year_start.value
        end = self.t4_spinBox_year_end.value
        limit = self.t4_spinBox_limit_artists.value
        q = self.session.query(Artist.name, func.count(Chart.chart_id)).filter(
                    Artist.artist_id == SongArtist.artist_id,
                    SongArtist.song_id == Song.song_id,
                    Song.song_id == Chart.song_id,
                    Region.name == region,
                    Region.region_id == Chart.region_id,
                    Day.day_id == Chart.day_id,
                    extract('year', Day.date) >= start,
                    extract('year', Day.date) <= end,
                    Chart.category_id == Category.category_id,
                    Category.name == self.category
                    ).group_by(Artist.name).order_by(func.count(Chart.chart_id).desc()).limit(limit)

        df = pd.read_sql(q.statement, self.session.bind)
        self.t0_textBrowser.appendLineTimed(str(q.statement.compile(self.engine)))
        data = df.set_index('name').to_dict()['count_1']
        wc = WordCloud(max_font_size=200, min_font_size=25, colormap='tab20', background_color=None, mode='RGBA',
                         width=2000, height=1500, random_state=int(datetime.datetime.now().timestamp()))
        cloud = wc.generate_from_frequencies(data)

        self.tab_4_clearPlot()

        self.t4_ax.imshow(cloud, interpolation='bilinear')
        self.t4_ax.axis('off')
        self.t4_plot.plotAxes()

        self.t4_lineEdit_search_region.clear()
        pass

    def tab_4_clearPlot(self:SpotifyAnalyzer):
        self.t4_plot.clearFigure()
        self.t4_ax = self.t4_plot.addSubplot(1, 1, 1)
        pass

    pass