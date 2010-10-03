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
        values = { 'sourceType'    : None,
                   'source'        : None,
                   'textColor'     : None,
                   'authorColor'   : None,
                   'timerInterval' : None }

        generalGroup = self.config.group("General")

        if generalGroup.hasKey("sourceType"):
            values['sourceType'] = generalGroup.readEntry("sourceType")

        if generalGroup.hasKey("source"):
            values['source'] = generalGroup.readEntry("source")

        if generalGroup.hasKey("textColor"):
            values['textColor'] = generalGroup.readEntry("textColor", QColor(0xcc, 0xcc, 0xcc))
        else:
            values['textColor'] = Qt.white

        if generalGroup.hasKey("authorColor"):
            values['authorColor'] = generalGroup.readEntry("authorColor", QColor(0xcc, 0xcc, 0xcc))
        else:
            values['authorColor'] = Qt.green

        if generalGroup.hasKey("timerInterval"):
            values['timerInterval'] = generalGroup.readEntry("timerInterval")
        else:
            values['timerInterval'] = "00:03"

        return values

    def writeConfig(self, values):
        generalGroup = self.config.group("General")

        generalGroup.writeEntry("sourceType", values['sourceType'])
        generalGroup.writeEntry("source", values['source'])
        generalGroup.writeEntry("textColor", values['textColor'])
        generalGroup.writeEntry("authorColor", values['authorColor'])
        generalGroup.writeEntry("timerInterval", values['timerInterval'])
