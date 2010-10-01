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
from PyQt4 import QtGui

class ASPopup(QtGui.QMenu):
    # Auto Sources Popup Class
    def __init__(self, parent):
        QtGui.QMenu.__init__(self, parent)
        self.parent = parent

        self.mainLayout = QtGui.QGridLayout(self)

        # Label for Installed Sources
        lbl_is = QtGui.QLabel(self)
        lbl_is.setText("Installed Sources:")
        self.mainLayout.addWidget(lbl_is, 0, 0, 1, 1)

        self.installedSources = QtGui.QListWidget(self)
        self.installedSources.setMinimumSize(QSize(260, 150))
        self.mainLayout.addWidget(self.installedSources, 1, 0, 1, 1)

        # Label for Available Sources
        lbl_as = QtGui.QLabel(self)
        lbl_as.setText("Available Sources:")
        self.mainLayout.addWidget(lbl_as, 2, 0, 1, 1)

        self.availableSources = QtGui.QListWidget(self)
        self.availableSources.setMinimumSize(QSize(260, 150))
        self.mainLayout.addWidget(self.availableSources, 3, 0, 1, 1)
