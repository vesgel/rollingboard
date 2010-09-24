#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, Volkan Esgel
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
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

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
        self.__createMainLayout()

    def __createMainLayout(self):
        self.mainLayout = QGraphicsLinearLayout(Qt.Vertical, self.applet)

        text = "<b><i>Just a try</i></b>. This is an experimental plasmoid and may not work properly."

        textBrowser = Plasma.TextBrowser(self.applet)
        textBrowserNW = textBrowser.nativeWidget()
        textBrowserNW.setReadOnly(True)
        textBrowser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        textBrowser.setText(unicode(text, 'UTF-8'))
        textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)        
        self.mainLayout.addItem(textBrowser)

        self.applet.setLayout(self.mainLayout)

def CreateApplet(parent):
    return RollingBoard(parent)
