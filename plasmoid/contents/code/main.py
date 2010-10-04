#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, Volkan Esgel, Ahmet Emre Aladağ
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt4 Section
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

# PyKDE4 Section
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

# Application Section
from html_parser import Document
from configs import GeneralConfig
from widgets import ASPopup
from data_manager import DataManager

# System Section
import webbrowser


class LineDisplayer(Plasma.TextBrowser):
    def __init__(self, parent=None):
	Plasma.TextBrowser.__init__(self, parent)
	self.parent = parent

    def contextMenuEvent(self, event):
	self.menu = menu = QMenu(None)
	copyToClipboard = menu.addAction("Copy to clipboard")
	twitter = menu.addAction("Share on Twitter")
	friendfeed = menu.addAction("Share on FriendFeed")

	action = menu.exec_(event.screenPos())

        if action == copyToClipboard:
	    clipboard = QApplication.clipboard()
	    clipboard.setText(self.board.line.plain_text)
	elif action == twitter:
	    webbrowser.open(self.board.line.get_twitter_link())
	elif action == friendfeed:
	    webbrowser.open(self.board.line.get_ff_link())

    def mousePressEvent(self, event):
	#Plasma.TextBrowser.mousePressEvent(self, event)
	if event.button() == Qt.LeftButton:
	    self.board._onClick()

    def refreshText(self):
	self.setText(self.board.line.__unicode__())

class RollingBoard(plasmascript.Applet):

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        self.setHasConfigurationInterface(True)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        self.resize(400, 100)

        self.conf = self.config()
        self.loadConfigurations()

        self.__createMainLayout()

    #=============== OPERATIONAL METHODS ============================

    def fetchRandomLine(self):
	self.line = self.document.get_random_line()
	self.textBrowser.refreshText()

    def timerEvent(self, event):
        self.fetchRandomLine()
        #self.update()

    def _onClick(self):
        self._resetTimer()
        self.fetchRandomLine()

    def _resetTimer(self):
	try:
          self.killTimer(self.mytimer)
        except:
          pass
        timerval = (int(self.automin)*60+int(self.autosec))*1000
        if timerval > 0:
           self.mytimer = self.startTimer(timerval)

    def getTimerIntervals(self, timer_interval):
        time = timer_interval.split(":")
        min, sec = map(int, time)
        return min, sec

    def loadConfigurations(self):
        self.generalConfig = GeneralConfig(self.conf)
        self.confValues = self.generalConfig.readConfig()

        self.automin, self.autosec = self.getTimerIntervals(self.confValues['timerInterval'])
        self._resetTimer()

    #=============== LAYOUT METHODS ============================
    def __createMainLayout(self):
        self.mainLayout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
        self.document = Document(self.package().path(), self.conf)

        self.line = self.document.get_random_line()

        self.textBrowser = textBrowser = LineDisplayer(self.applet)
        textBrowser.board = self

        textBrowserNW = textBrowser.nativeWidget()
        textBrowserNW.setReadOnly(True)

        textBrowser.refreshText()
        textBrowser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mainLayout.addItem(textBrowser)
        self.applet.setLayout(self.mainLayout)

    #=============== CONFIG METHODS ============================
    def createConfigurationInterface(self, parent):
        self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
        self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)

        self.generalCP = QWidget(parent)  # General Config Page
        uic.loadUi(self.package().filePath('ui', 'generalconfig.ui'), self.generalCP)
        parent.addPage(self.generalCP, "General", 'configure', "General Configuration Options")

        # Popup Menu for Auto Sources
        ASMenu = ASPopup(self.generalCP, self.package())
        self.generalCP.autoSource.setMenu(ASMenu)

        values = self.generalConfig.readConfig()
        if not values['source']:
            values['source'] = ""
            ## FIXME: This assignment might be cause empty addresses in sourceAddress

        if values['sourceType']:
            if values['sourceType'] == 'Auto':
                print "Auto Source"
            else:
                print "Manual Source"

        if self.generalCP.rdb_autoSource.isChecked():
            self.generalCP.manualSource.setEnabled(False)
        else:
            self.generalCP.autoSource.setEnabled(False)

        self.generalCP.manualSource.setText(values['source'])  ## !!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.generalCP.textColor.setColor(QColor(values['textColor']))
        self.generalCP.authorColor.setColor(QColor(values['authorColor']))

        min, sec = self.getTimerIntervals(values['timerInterval'])
        self.generalCP.timeEdit.setTime(QTime(min, sec))

        # We have only two radio buttons and connecting one of them with signal is OK.
        self.connect(self.generalCP.rdb_manualSource, SIGNAL("toggled(bool)"), self.sourceChanged)

    def configAccepted(self):
        values = { 'sourceType'    : None,
                   'source'        : None,
                   'textColor'     : None,
                   'authorColor'   : None,
                   'timerInterval' : None }

        if self.generalCP.rdb_autoSource.isChecked():
            values['sourceType'] = "Auto"
            #values['source'] = self.generalCP.sourceAddress.currentText()
        else:
            values['sourceType'] = "Manual"
            values['source'] = self.generalGP.manualSource.text()
        values['textColor'] = self.generalCP.textColor.color()
        values['authorColor'] = self.generalCP.authorColor.color()
        values['timerInterval'] = self.generalCP.timeEdit.text()

        self.generalConfig.writeConfig(values)
        self.loadConfigurations()

    def configDenied(self):
        print "..config denied!.."

    def sourceChanged(self, value):
        self.generalCP.manualSource.setEnabled(value)
        self.generalCP.autoSource.setEnabled(not value)

def CreateApplet(parent):
    return RollingBoard(parent)
