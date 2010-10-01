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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from html_parser import Document
from configs import GeneralConfig
from data_manager import DataManager
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
	    self.board.__onClick()

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
	
	# TODO: Get these from config
	self.automin = 0
        self.autosec = 3
        
        self.conf = self.config()
        self.generalConfig = GeneralConfig(self.conf)
        
        self.__createMainLayout()

    #=============== OPERATIONAL METHODS ============================
    
    def fetchRandomLine(self):
	self.line = self.document.get_random_line()
	self.textBrowser.refreshText()

    def timerEvent(self, event):
        self.fetchRandomLine()
        #self.update()

    def __onClick(self):
        self.__resetTimer()
        self.fetchRandomLine()        

    def __resetTimer(self):
	try:
          self.killTimer(self.mytimer)
        except:
          pass
        timerval = (int(self.automin)*60+int(self.autosec))*1000
        if timerval > 0:
           self.mytimer = self.startTimer(timerval)
        
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
	self.__resetTimer()
	
    #=============== CONFIG METHODS ============================
    def createConfigurationInterface(self, parent):
        self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
        self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)
        
        self.generalConfigPage = QWidget(parent)
        uic.loadUi(self.package().filePath('ui', 'generalconfig.ui'), self.generalConfigPage)
        parent.addPage(self.generalConfigPage, "General", 'configure', "General Configuration Options")
        
        sourceFile, textColor, authorColor = self.generalConfig.readConfig()
        if not sourceFile:
            sourceFile = ""
        
        self.generalConfigPage.sourceFile.setText(sourceFile)
        self.generalConfigPage.textColor.setColor(QColor(textColor))
        self.generalConfigPage.authorColor.setColor(QColor(authorColor))
        
    def configAccepted(self):
        sourceFile = self.generalConfigPage.sourceFile.text()
        textColor = self.generalConfigPage.textColor.color()
        authorColor = self.generalConfigPage.authorColor.color()

        self.generalConfig.writeConfig(sourceFile, QVariant(textColor), QVariant(authorColor))
        #self.__resetTimer()


    def configDenied(self):
        print "..config denied!.."

def CreateApplet(parent):
    return RollingBoard(parent)
