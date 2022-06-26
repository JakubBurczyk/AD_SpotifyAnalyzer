from __future__ import annotations

from threading import Thread, Lock
from matplotlib import artist

from pyparsing import Char
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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    from _tabMethods import Mixin_TabMethods


class Mixin_Tab_2():

    def __init__(self:Union[SpotifyAnalyzer, Mixin_TabMethods]):
        print("tab2 init")
        self.queries[2] = self.tab_2_query
        self.t2_lock = Lock()
        self.tab_2_widgets()
        self.tab_2_callbacks()
        self.t2_queryInitalized = False

    def tab_2_widgets(self:SpotifyAnalyzer):
        self.t2_plot:MatplotlibFigure = self.tab_2.addWidget(MatplotlibFigure(self.mainWindow, "plot2"))
        self.t2_ax = self.t2_plot.addSubplot(1, 1, 1)

        self.t2_button_plot:Button = self.tab_2.addWidget(Button(self.mainWindow,"pushButton_plot_2",self.tab_2_plots))
        self.t2_button_clear:Button = self.tab_2.addWidget(Button(self.mainWindow,"pushButton_plot_clear_2",self.tab_2_clearPlot))

        self.t2_list_artists:ListWidget = self.tab_2.addWidget(ListWidget(self.mainWindow, "listWidget_artist_2"))

        self.t2_lineEdit_search_artist:LineEdit = self.tab_2.addWidget(LineEdit(self.mainWindow, "lineEdit_search_artist_2"))
        
        self.t2_spinBox_number_songs:SpinBox = self.tab_1.addWidget(SpinBox(self.mainWindow, "spinBox_number_songs_2"))
        pass

    def tab_2_callbacks(self:SpotifyAnalyzer):
        #self.t2_list_artists.setCallbackClicked(lambda: self.t1_label_song.setText(self.t1_list_songs.getSelectedText()))
        self.t2_lineEdit_search_artist.setCallback(lambda filter: self.t2_list_artists.filterItems(filter))
        pass

    def tab_2_query(self):
        if not self.t2_queryInitalized:
            q1 = self.session.query(Artist.name).filter(
                #SongArtist.song_id == Chart.song_id,
                #SongArtist.artist_id == Artist.artist_id,
                #Chart.category_id == Category.category_id,
                #Category.name == 'top200'
            )

            thread_artists = Thread(target=self.threadQuery, args=(q1,'name',self.t2_list_artists))
            thread_artists.setDaemon(True)
            thread_artists.start()
            self.t2_queryInitalized = True
        pass

    def tab_2_plots(self:SpotifyAnalyzer):
        name = self.t2_list_artists.getSelectedText()
        songLimit = self.t2_spinBox_number_songs.value

        region = "Global"
        q = self.session.query(Song.title, func.sum(Chart.streams)).filter(
                    Artist.name == name,
                    Artist.artist_id == SongArtist.artist_id,
                    SongArtist.song_id == Song.song_id,
                    Song.song_id == Chart.song_id,
                    Region.name == region,
                    Region.region_id == Chart.region_id,
                    Chart.category_id == Category.category_id,
                    Category.name == "top200"
                    ).group_by(Song.title).order_by(func.sum(Chart.streams).desc()).limit(songLimit)

        df = pd.read_sql(q.statement, self.session.bind)
        
        self.tab_2_clearPlot()
        self.t2_ax.tick_params(axis='x', labelrotation=45)
        self.t2_ax.bar(df.title, df.sum_1)
        self.t2_ax.grid()
        self.t2_ax.set_axisbelow(True)
        self.t2_ax.set_xlabel("Title")
        self.t2_ax.set_ylabel("Streams")
        self.t2_ax.set_title(f"Distribution of streams for Top{songLimit} of {name} songs")
        self.t2_plot.plotAxes()

        self.t2_lineEdit_search_artist.clear()
        pass

    def tab_2_clearPlot(self:SpotifyAnalyzer):
        self.t2_plot.clearFigure()
        self.t2_ax = self.t2_plot.addSubplot(1, 1, 1)
        pass

    pass