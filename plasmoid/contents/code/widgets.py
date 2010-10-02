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
from PyQt4 import uic

from PyKDE4.kdeui import KIcon

class ASItemWidget(QtGui.QWidget):
    def __init__(self, parent, data, item, package):
        QtGui.QWidget.__init__(self, parent)
        self.item = item
        self.data = data

        ui_class, widget_class = uic.loadUiType(package.filePath('ui', 'sourceitem.ui'))
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.ui.labelName.setText(data)
        self.ui.buttonInstall.setIcon(KIcon("go-down"))

class ASPopup(QtGui.QMenu):
    # Auto Sources Popup Class
    def __init__(self, parent, package):
        QtGui.QMenu.__init__(self, parent)
        self.parent = parent
        self.package = package

        self.mainLayout = QtGui.QGridLayout(self)

        # Label for Installed Sources
        lbl_is = QtGui.QLabel(self)
        lbl_is.setText("Installed Sources:")
        self.mainLayout.addWidget(lbl_is, 0, 0, 1, 1)

        # ListWidget for Installed Sources
        self.installedList = QtGui.QListWidget(self)
        self.installedList.setMinimumSize(QSize(260, 150))
        self.mainLayout.addWidget(self.installedList, 1, 0, 1, 1)
        self.loadItems(self.installedList)

        # Label for Available Sources
        lbl_as = QtGui.QLabel(self)
        lbl_as.setText("Available Sources:")
        self.mainLayout.addWidget(lbl_as, 2, 0, 1, 1)

        # ListWidget for Available Sources
        self.availableList = QtGui.QListWidget(self)
        self.availableList.setMinimumSize(QSize(260, 150))
        self.mainLayout.addWidget(self.availableList, 3, 0, 1, 1)

    def loadItems(self, listWidget):
        items = ["Resource 1", "Resource 2", "Resource 3", "Resource 4"]

        for i in items:
            item  = QtGui.QListWidgetItem(listWidget)
            item.setSizeHint(QSize(250, 32))
            asw = ASItemWidget(self, i, item, self.package)
            listWidget.setItemWidget(item, asw)
