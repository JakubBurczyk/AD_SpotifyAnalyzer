from __future__ import annotations
from concurrent.futures import thread
from time import sleep
from multiprocessing import Process, Lock
from soupsieve import select

import sqlalchemy
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
from sqlalchemy.orm import sessionmaker

from typing import TYPE_CHECKING, Text
if TYPE_CHECKING:
    from spotifyAnalyzer import SpotifyAnalyzer
    from _tabMethods import Mixin_TabMethods


class Mixin_Tab_0():

    def __init__(self) -> None:
        self.engine: sqlalchemy.engine.Engine = None
        self.session:sessionmaker = None
        self.thread_labels = []
        self.threads_num = 4
        self.batch_size = 10000
        self.datapath = ""

        self.lock = Lock()

        self.tab_0_widgets()
        self.tab_0_callbacks()
        pass

    def tab_0_widgets(self:SpotifyAnalyzer):
        self.textBrowser:TextBrowser = self.tab_0.addWidget(TextBrowser(self.mainWindow, "textBrowser_tab_0"))

        self.button_connect:Button = self.tab_0.addWidget(Button(self.mainWindow, "pushButton_test", self.testDb))
        self.button_connect:Button = self.tab_0.addWidget(Button(self.mainWindow, "pushButton_clear", self.clearTxt))

        self.list_tables:ListWidget = self.tab_0.addWidget(ListWidget(self.mainWindow,"listWidget_tables"))

        self.lineEdit_db_ip:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_ip"))
        self.lineEdit_db_port:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_port"))
        self.lineEdit_db_name:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_name"))
        self.lineEdit_db_user:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_user"))
        self.lineEdit_db_pass:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_pass"))
        pass

    def tab_0_callbacks(self:SpotifyAnalyzer):
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
            self.session = (sessionmaker(bind=self.engine))()
            return True
        except:
            return False
            pass
        return False
        pass

    def clearTxt(self):
        self.textBrowser.clear()
        pass

    def testDb(self):
        if self.createEngine():
            self.session: sessionmaker
            dbClass = self.getSelectedTableName()
            session_stmt = self.session.query(dbClass)
            session_results = session_stmt.limit(10).all()
            results_str = [res.__repr__() for res in session_results]
            self.textBrowser.appendLineTimed(results_str)
            self.textBrowser.appendLine("")
            #self.textBrowser.appendLineTimed(["Query results:"].append(results_str))
        pass

    def getSelectedTableName(self):
        selected = self.list_tables.getSelectedText()
        dbClass = None
        if selected == "Artist":
            dbClass = Artist
            pass
        elif selected == "Song":
            dbClass = Song
            pass
        elif selected == "Song Artist":
            dbClass = SongArtist
            pass
        elif selected == "Trend":
            dbClass = Trend
            pass
        elif selected == "Day":
            dbClass = Day
            pass
        elif selected == "Region":
            dbClass = Region
            pass
        elif selected == "Category":
            dbClass = Category
            pass
        elif selected == "Chart":
            dbClass = Chart
            pass
        return dbClass
        pass
