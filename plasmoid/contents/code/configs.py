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

from PyQt4.QtGui import QColor
from PyQt4.QtCore import Qt

class GeneralConfig:
    def __init__(self, config):
        self.config = config
        self.readConfig()

    def readConfig(self):
        sourceFile = None
        textColor = None
        authorColor = None

        generalGroup = self.config.group("General")

        if generalGroup.hasKey("sourceFile"):
            sourceFile = generalGroup.readEntry("sourceFile")

        if generalGroup.hasKey("textColor"):
            textColor = generalGroup.readEntry("textColor", QColor(0xcc, 0xcc, 0xcc))
        else:
            textColor = Qt.white

        if generalGroup.hasKey("authorColor"):
            authorColor = generalGroup.readEntry("authorColor", QColor(0xcc, 0xcc, 0xcc))
        else:
            authorColor = Qt.green

        return sourceFile, textColor, authorColor

    def writeConfig(self, sourceFile, textColor, authorColor):
        generalGroup = self.config.group("General")

        generalGroup.writeEntry("sourceFile", sourceFile)
        generalGroup.writeEntry("textColor", textColor)
        generalGroup.writeEntry("authorColor", authorColor)
