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

        self.t0_lock = Lock()

        self.tab_0_widgets()
        self.tab_0_callbacks()
        pass

    def tab_0_widgets(self:SpotifyAnalyzer):
        self.t0_textBrowser:TextBrowser = self.tab_0.addWidget(TextBrowser(self.mainWindow, "textBrowser_tab_0"))

        self.t0_button_connect:Button = self.tab_0.addWidget(Button(self.mainWindow, "pushButton_test", self.tab_0_testDb))
        self.t0_button_clear:Button = self.tab_0.addWidget(Button(self.mainWindow, "pushButton_clear", self.tab_0_clearTxt))

        self.t0_list_tables:ListWidget = self.tab_0.addWidget(ListWidget(self.mainWindow, "listWidget_tables"))

        self.t0_lineEdit_db_ip:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_ip"))
        self.t0_lineEdit_db_port:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_port"))
        self.t0_lineEdit_db_name:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_name"))
        self.t0_lineEdit_db_user:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_user"))
        self.t0_lineEdit_db_pass:LineEdit = self.tab_0.addWidget(LineEdit(self.mainWindow, "lineEdit_db_pass"))
        pass

    def tab_0_callbacks(self:SpotifyAnalyzer):
        pass

    def createEngine(self:SpotifyAnalyzer):
        user = self.t0_lineEdit_db_user.text
        password = self.t0_lineEdit_db_pass.text
        ip = self.t0_lineEdit_db_ip.text
        port = self.t0_lineEdit_db_port.text
        db_name = self.t0_lineEdit_db_name.text

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

    def tab_0_clearTxt(self):
        self.t0_textBrowser.clear()
        pass

    def tab_0_testDb(self):
        if self.createEngine():
            self.session: sessionmaker
            dbClass = self.tab_0_getSelectedTableName()
            session_stmt = self.session.query(dbClass)
            session_results = session_stmt.limit(10).all()
            results_str = [res.__repr__() for res in session_results]
            self.t0_textBrowser.appendLineTimed(results_str)
            self.t0_textBrowser.appendLine("")
            #self.textBrowser.appendLineTimed(["Query results:"].append(results_str))
        pass

    def tab_0_getSelectedTableName(self):
        selected = self.t0_list_tables.getSelectedText()
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
