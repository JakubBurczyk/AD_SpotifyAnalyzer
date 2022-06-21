from __future__ import annotations
from concurrent.futures import thread
from time import sleep
from multiprocessing import Process, Lock
from gui import GUI
import os
import widgets as widgets
from widgets import *
import window as window
from widgets import Tab
from PyQt5.QtWidgets import QListWidgetItem

from sqlalchemy import create_engine
import pandas as pd
import threading
from copy import copy
from dbClasses import *


from typing import TYPE_CHECKING, Text
if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    from _tabMethods import Mixin_TabMethods


class Mixin_Tab_0():

    def tab_0_vars(self):
        self.engine = None
        self.thread_labels = []
        self.threads_num = 4
        self.batch_size = 10000
        self.datapath = ""
        self.lock = Lock()
        pass

    def tab_0_widgets(self:SpotifyAnalyzer):
        self.button_connect:Button = self.tab_0.addWidget(Button(self.mainWindow, "pushButton_db_create", self.createDatabase))

        self.spinBox_batch_size:SpinBox = self.tab_0.addWidget(SpinBox(self.mainWindow, "spinBox_batch_size"))
        self.spinBox_threads: SpinBox = self.tab_0.addWidget(SpinBox(self.mainWindow, "spinBox_threads"))

        self.textBrowser_threads:TextBrowser = self.tab_0.addWidget(TextBrowser(self.mainWindow, "textBrowser_threads"))

        self.lineEdit_db_ip:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_ip"))
        self.lineEdit_db_port:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_port"))
        self.lineEdit_db_name:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_name"))
        self.lineEdit_db_user:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_user"))
        self.lineEdit_db_pass:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_pass"))

        self.label_th_1: Label = self.tab_0.addWidget(Label(self.mainWindow, "label_th_1"))
        self.label_th_2: Label = self.tab_0.addWidget(Label(self.mainWindow, "label_th_2"))
        self.label_th_3: Label = self.tab_0.addWidget(Label(self.mainWindow, "label_th_3"))
        self.label_th_4: Label = self.tab_0.addWidget(Label(self.mainWindow, "label_th_4"))
        self.label_th_5: Label = self.tab_0.addWidget(Label(self.mainWindow, "label_th_5"))
        self.label_th_6: Label = self.tab_0.addWidget(Label(self.mainWindow, "label_th_6"))
        self.label_th_7: Label = self.tab_0.addWidget(Label(self.mainWindow, "label_th_7"))
        self.label_th_8: Label = self.tab_0.addWidget(Label(self.mainWindow, "label_th_8"))
        pass

    def tab_0_callbacks(self:SpotifyAnalyzer):

        pass
    
    def tab_0_process(self: SpotifyAnalyzer):
        self.thread_labels.append(self.label_th_1)
        self.thread_labels.append(self.label_th_2)
        self.thread_labels.append(self.label_th_3)
        self.thread_labels.append(self.label_th_4)
        self.thread_labels.append(self.label_th_5)
        self.thread_labels.append(self.label_th_6)
        self.thread_labels.append(self.label_th_7)
        self.thread_labels.append(self.label_th_8)

    def createDatabase(self:SpotifyAnalyzer):
        self.threads_num = self.spinBox_threads.value
        self.batch_size = self.spinBox_batch_size.value

        self.createEngine()
        loaded = self.loadData()
        if not loaded:
            self.textBrowser_threads.appendLineTimed("Did not load data file")
        else:
            self.data = self.data.loc[0:99999].copy()
            self.createFullTables()
            self.runAllBatches()
            
        pass

    def runAllBatches(self:SpotifyAnalyzer):
        size = len(self.data)
        batches = int(size/(self.threads_num * self.batch_size))
        end_index = batches*self.threads_num * self.batch_size

        self.textBrowser_threads.appendLineTimed(f"Starting batches End index = {end_index}")
        for i in range(batches):
            self.runSingleBatch(i)
            self.textBrowser_threads.appendLineTimed(f"Batch [{i}/{batches}] finished")
            pass
        pass
        if end_index < size:
            self.thread_updateTables(end_index,size)
            pass

        self.df_chart['streams'] = self.df_chart['streams'].astype(pd.Int64Dtype())

        path = os.path.dirname(self.datapath)
        self.df_artist.to_csv(path+'\\df_artist.csv',index=False)
        self.df_song.to_csv(path+'\\df_song.csv',index=False)
        self.df_songArtist.to_csv(path+'\\df_songArtist.csv',index=False)
        self.df_trend.to_csv(path+'\\df_trend.csv',index=False)
        self.df_day.to_csv(path+'\\df_day.csv',index=False)
        self.df_region.to_csv(path+'\\df_region.csv',index=False)
        self.df_category.to_csv(path+'\\df_category.csv',index=False)
        self.df_chart.to_csv(path+'\\df_chart.csv',index=False)

        
        self.df_artist.to_sql('artist', self.engine, if_exists='replace', index = False)
        self.df_song.to_sql('song', self.engine, if_exists='replace', index = False)
        self.df_songArtist.to_sql('song_artist', self.engine, if_exists='replace', index = False)
        self.df_trend.to_sql('trend', self.engine, if_exists='replace', index = False)
        self.df_day.to_sql('day', self.engine, if_exists='replace', index = False)
        self.df_region.to_sql('region', self.engine, if_exists='replace', index = False)
        self.df_category.to_sql('category', self.engine, if_exists='replace', index = False)
        self.df_chart.to_sql('chart', self.engine, if_exists='replace', index = False)

        self.textBrowser_threads.appendLineTimed(f"Finished all batches")


    def runSingleBatch(self:SpotifyAnalyzer,batch_cnt):
        thread: threading.Thread
        threads = []

        offset = batch_cnt * self.batch_size * self.threads_num
        size = self.batch_size
        
        for i in range(self.threads_num):
            threads.append(threading.Thread(target=self.thread_updateTables, args=(i*size + offset, (i+1)*size + offset - 1)))

        for thread in threads:
            thread.setDaemon(False)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        #print(self.df_chart.loc[990:1010])

    def thread_updateTables(self:SpotifyAnalyzer,v1,v2):
        print(f"Thread {v1} to {v2}")
        df_songArtist_cp = self.df_songArtist.loc[v1:v2].copy()

        df_songArtist_cp['song_id'] = df_songArtist_cp['song_id'].map(lambda x: self.df_song[self.df_song['title'] == x].song_id.values.astype(int)[0])
        df_songArtist_cp['artist_id'] = df_songArtist_cp['artist_id'].map(lambda x: self.df_artist[self.df_artist['name'] == x].artist_id.values.astype(int)[0])
        

        df_chart_cp = self.df_chart.loc[v1:v2].copy()
        df_chart_cp['song_id'] = df_chart_cp['song_id'].map(lambda x: self.df_song[self.df_song['title'] == x].song_id.values.astype(int)[0])
        df_chart_cp['day_id'] = df_chart_cp['day_id'].map(lambda x: self.df_day[self.df_day['date'] == x].day_id.values.astype(int)[0])
        df_chart_cp['region_id'] = df_chart_cp['region_id'].map(lambda x: self.df_region[self.df_region['name'] == x].region_id.values.astype(int)[0])
        df_chart_cp['category_id'] = df_chart_cp['category_id'].map(lambda x: self.df_category[self.df_category['name'] == x].category_id.values.astype(int)[0])
        df_chart_cp['trend_id'] = df_chart_cp['trend_id'].map(lambda x: self.df_trend[self.df_trend['trend'] == x].trend_id.values.astype(int)[0])
        self.lock.acquire()
        self.df_songArtist.update(df_songArtist_cp)
        self.df_chart.update(df_chart_cp)
        self.lock.release()
        pass

    def createFullTables(self:SpotifyAnalyzer):
        self.textBrowser_threads.appendLineTimed("Creating initial dataframes")
        # Artist
        self.df_artist = pd.DataFrame(self.data['artist'].unique(), columns=['name'])
        self.df_artist = self.df_artist.assign(name=self.df_artist['name'].str.split(', ')).explode('name')
        self.df_artist.reset_index(drop = True, inplace=True)
        self.df_artist.insert(0, 'artist_id', range(1, 1 + len(self.df_artist)))
        # Song
        self.df_song = pd.DataFrame(self.data['title'].unique(), columns=['title'])
        self.df_song.insert(0, 'song_id', range(1, 1 + len(self.df_song)))
        # Trend
        self.df_trend = pd.DataFrame(self.data['trend'].unique(), columns=['trend'])
        self.df_trend.insert(0, 'trend_id', range(1, 1 + len(self.df_trend)))
        # Day
        self.df_day = pd.DataFrame(self.data['date'].unique(), columns=['date'])
        self.df_day.insert(0, 'day_id', range(1, 1 + len(self.df_day)))
        # Category
        self.df_category = pd.DataFrame(self.data['chart'].unique(), columns=['name'])
        self.df_category.insert(0, 'category_id', range(1, 1 + len(self.df_category)))
        # Region
        self.df_region = pd.DataFrame(self.data['region'].unique(), columns=['name'])
        self.df_region.insert(0, 'region_id', range(1, 1 + len(self.df_region)))
        # Song Artist
        self.df_songArtist = self.data[['title', 'artist']].drop_duplicates().reset_index().drop(columns = ['index'])
        self.df_songArtist.rename(columns = {'title': 'song_id', 'artist': 'artist_id'}, inplace = True)
        self.df_songArtist = self.df_songArtist.assign(artist_id=self.df_songArtist['artist_id'].str.split(', ')).explode('artist_id')
        self.df_songArtist.reset_index(drop = True, inplace=True)
        # Chart
        self.df_chart = self.data[['rank', 'title', 'date', 'region', 'chart', 'trend', 'streams']].drop_duplicates().reset_index().drop(columns = ['index'])
        self.df_chart = self.df_chart.rename(columns = {'title':'song_id', 'rank':'position', 'date':'day_id', 'region':'region_id', 'chart':'category_id', 'trend':'trend_id'})
        self.df_chart.insert(0, 'chart_id', range(1, 1 + len(self.df_chart)))
        #self.df_chart['streams'] = self.df_chart['streams'].astype('int')
        self.textBrowser_threads.appendLineTimed("Created initial dataframes")

        path = os.path.dirname(self.datapath)
        path = os.path.join(path,"processed")
        print(path)
        self.df_artist.to_csv(path+"\\artist.csv",index=False)
        self.df_song.to_csv(path+"\\song.csv",index=False)
        self.df_trend.to_csv(path+"\\trend.csv",index=False)
        self.df_day.to_csv(path+"\\day.csv",index=False)
        self.df_category.to_csv(path+"\\category.csv",index=False)
        self.df_region.to_csv(path+"\\region.csv",index=False)
        self.df_songArtist.to_csv(path+"\\songArtist.csv",index=False)
        self.df_chart.to_csv(path+"\\chart.csv",index=False)
        pass

    def createEngine(self:SpotifyAnalyzer):
        user = self.lineEdit_db_user.text
        password = self.lineEdit_db_pass.text
        ip = self.lineEdit_db_ip.text
        port = self.lineEdit_db_port.text
        db_name = self.lineEdit_db_name.text

        self.db_url = f"postgresql://{user}:{password}@{ip}:{port}/{db_name}"
        try:
            self.engine = create_engine(self.db_url)
        except:
            pass
        pass

    def loadData(self:SpotifyAnalyzer):
        filePath = QFileDialog.getOpenFileName(self.mainWindow, 'Open a file', '', 'CSV file (*.csv)')
        if filePath != ('', ''):
            self.datapath, extension = filePath
            self.data = pd.read_csv(self.datapath)
            self.textBrowser_threads.appendLineTimed("Read CSV file:")
            self.textBrowser_threads.appendLine(self.data.head().__repr__())
            return True

        return False
        pass

    