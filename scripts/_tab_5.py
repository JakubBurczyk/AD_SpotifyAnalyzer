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
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    from _tabMethods import Mixin_TabMethods

import globals

class Mixin_Tab_5():

    def __init__(self:Union[SpotifyAnalyzer, Mixin_TabMethods]):
        print("tab5 init")
        self.queries[5] = self.tab_5_query
        self.t5_lock = Lock()
        self.tab_5_widgets()
        self.tab_5_callbacks()
        self.t5_queryInitalized = False
        self.category = globals.CATEGORY_200

    def tab_5_widgets(self:SpotifyAnalyzer):
        self.t5_plot:MatplotlibFigure = self.tab_5.addWidget(MatplotlibFigure(self.mainWindow, "plot6"))
        self.t5_ax = self.t5_plot.addSubplot(1, 1, 1)

        self.t5_button_plot:Button = self.tab_5.addWidget(Button(self.mainWindow,"pushButton_plot_7",self.tab_5_plots))
        self.t5_button_clear:Button = self.tab_5.addWidget(Button(self.mainWindow,"pushButton_plot_clear_7",self.tab_5_clearPlot))

        self.t5_button_category:Button = self.tab_5.addWidget(Button(self.mainWindow,"pushButton_category_6",self.tab_5_switch_category))
        self.t5_label_category:Label = self.tab_5.addWidget(Label(self.mainWindow,"label_category_6"))
        #self.t5_button_add:Button = self.tab_5.addWidget(Button(self.mainWindow,"pushButton_add_6",self.tab_5_add_region))
        #self.t5_button_remove:Button = self.tab_5.addWidget(Button(self.mainWindow,"pushButton_remove_6",self.tab_5_remvoe_region))

        #self.t5_list_regions:ListWidget = self.tab_5.addWidget(ListWidget(self.mainWindow, "listWidget_region_6"))
        #self.t5_list_selected_regions:ListWidget = self.tab_5.addWidget(ListWidget(self.mainWindow, "listWidget_selected_regions_6"))

        #self.t5_lineEdit_search_region:LineEdit = self.tab_5.addWidget(LineEdit(self.mainWindow, "lineEdit_search_region_6"))

        self.t5_spinBox_year:SpinBox = self.tab_5.addWidget(SpinBox(self.mainWindow, "spinBox_year_6"))
        
        pass

    def tab_5_callbacks(self:SpotifyAnalyzer):
        #self.t5_lineEdit_search_region.setCallback(lambda filter: self.t5_list_regions.filterItems(filter))
        pass


    def tab_5_query(self):
        if not self.t5_queryInitalized:
            #q1 = self.session.query(Region.name).filter(
            #)

            #thread_regions = Thread(target=self.threadQuery, args=(q1,'name',self.t5_list_regions))
            #thread_regions.setDaemon(True)
            #thread_regions.start()
            self.t5_queryInitalized = True

            #self.t5_list_regions.removeByText("Hong Kong")
            #self.t5_list_regions.removeByText("Singapore")
            #self.t5_list_regions.removeByText("Andorra")
        pass

    def tab_5_switch_category(self:SpotifyAnalyzer):
        self.category = self.switch_category(self.category)
        self.t5_label_category.setText(self.category)
        pass

    def tab_5_plotThread(self):
        year = self.t5_spinBox_year.value
        q = self.session.query(Region.name, func.count(func.distinct(Artist.name))).filter(
                    Day.day_id == Chart.day_id,
                    extract('year', Day.date) == year,
                    Artist.artist_id == SongArtist.artist_id,
                    SongArtist.song_id == Song.song_id,
                    Song.song_id == Chart.song_id,
                    Region.region_id == Chart.region_id,
                    Region.name != "Global",
                    Chart.category_id == Category.category_id,
                    Category.name == self.category
                    ).group_by(Region.name)

        df = pd.read_sql(q.statement, self.session.bind)
        print(df)
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        isoDict = {'Czech Republic': 'Czechia', 'Dominican Republic':'Dominican Rep.', 'United States':'United States of America'}
        df = df.replace({"name": isoDict})
        df = df.drop(df[df.name == "Hong Kong"].index)
        df = df.drop(df[df.name == "Singapore"].index)
        df = df.drop(df[df.name == "Andorra"].index)

        world = world.merge(df,on='name',how="left")
        columns = ['name', 'count_1', 'geometry']
        world = pd.DataFrame(world, columns=columns)
        world = gpd.GeoDataFrame(world)

        self.tab_5_clearPlot()

        divider = make_axes_locatable(self.t5_ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        world.plot(column='count_1', ax=self.t5_ax, legend=True, cax=cax, missing_kwds={'color': 'lightgrey'})
        self.t5_ax.set_xlabel("Longitude")
        self.t5_ax.set_ylabel("Latitude")
        self.t5_ax.set_title(f"Unique artists reaching Top200 by country")

        
        self.t5_plot.plotAxes()
        pass

    def tab_5_plots(self:SpotifyAnalyzer):
        self.thread5 = Thread(target=self.tab_5_plotThread)
        self.thread5.setDaemon(True) 
        self.thread5.start()  
        pass

    def tab_5_clearPlot(self:SpotifyAnalyzer):
        self.t5_plot.clearFigure()
        self.t5_ax = self.t5_plot.addSubplot(1, 1, 1)
        pass
    """
    def tab_5_add_region(self:SpotifyAnalyzer):
        region = self.t5_list_regions.removeSelected()
        self.t5_list_selected_regions.addItem(region.text())
        pass

    def tab_5_remvoe_region(self:SpotifyAnalyzer):
        region = self.t5_list_selected_regions.removeSelected()
        self.t5_list_regions.addItem(region.text())
        pass
    """
    pass