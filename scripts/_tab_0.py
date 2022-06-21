from __future__ import annotations
from concurrent.futures import thread
from time import sleep

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
        self.loadData()
        self.runAllBatches()
        pass

    def runAllBatches(self:SpotifyAnalyzer):
        batches = 2

        for i in range(batches):
            self.runSingleBatch(i)
            pass
        pass

    def runSingleBatch(self:SpotifyAnalyzer,batch_cnt):
        thread: threading.Thread
        threads = []

        offset = batch_cnt * self.batch_size * self.threads_num
        size = self.batch_size

        for i in range(self.threads_num):
            threads.append(threading.Thread(target=self.thread_toSQL, args=(i*size + offset, (i+1)*size + offset)))

        for thread in threads:
            thread.setDaemon(True)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            pass

        print(["#"*30])

    def thread_toSQL(self:SpotifyAnalyzer,v1,v2):
        data = self.data[v1:v2]


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
            path, extension = filePath
            self.data = pd.read_csv(path)
            self.textBrowser_threads.appendLineTimed("Read CSV file:")
            self.textBrowser_threads.appendLine(self.data.head().__repr__())
        pass

    