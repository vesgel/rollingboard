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
from PyQt4 import QtGui
from PyQt4 import uic

# PyKDE4 Section
from PyKDE4.kdeui import KIcon

# Application Section
from data_manager import DataManager

# System Section
import os

(AVAILABLE, INSTALLED) = range(2)

class ASItemWidget(QtGui.QWidget):
    def __init__(self, parent, data, item, mode, package):
        QtGui.QWidget.__init__(self, parent)
        self.item = item
        self.data = data
        self.mode = mode

        ui_class, widget_class = uic.loadUiType(package.filePath('ui', 'sourceitem.ui'))
        self.ui = ui_class()
        self.ui.setupUi(self)

        if self.mode == AVAILABLE:
            name = self.data[2]
            self.ui.buttonRemove.hide()
            self.ui.buttonApply.setIcon(KIcon("go-down"))
            self.ui.buttonApply.setToolTip("Download Source")
        else:
            name = self.data
            self.ui.buttonRemove.setIcon(KIcon("list-remove"))
            self.ui.buttonRemove.setToolTip("Remove Source")
            self.ui.buttonApply.setToolTip("Select Source")

        self.ui.labelName.setText(name)

class ASPopup(QtGui.QMenu):
    # Auto Sources Popup Class
    def __init__(self, parent, package):
        QtGui.QMenu.__init__(self, parent)
        self.parent = parent
        self.package = package
        package_path = self.package.path()
        self.data_path = "%scontents/data" % package_path
        self.dataManager = DataManager(self.data_path)

        self.mainLayout = QtGui.QGridLayout(self)

        # Label for Installed Sources
        lbl_is = QtGui.QLabel(self)
        lbl_is.setText("Installed Sources:")
        self.mainLayout.addWidget(lbl_is, 0, 0, 1, 1)

        # ListWidget for Installed Sources
        self.installedList = QtGui.QListWidget(self)
        self.installedList.setMinimumSize(QSize(260, 150))
        self.mainLayout.addWidget(self.installedList, 1, 0, 1, 1)
        installedSourceList = os.listdir(self.data_path)
        self.loadItems(self.installedList, installedSourceList, INSTALLED)

        # Label for Available Sources
        lbl_as = QtGui.QLabel(self)
        lbl_as.setText("Available Sources:")
        self.mainLayout.addWidget(lbl_as, 2, 0, 1, 1)

        # ListWidget for Available Sources
        self.availableList = QtGui.QListWidget(self)
        self.availableList.setMinimumSize(QSize(260, 150))
        self.mainLayout.addWidget(self.availableList, 3, 0, 1, 1)
        availableSourceList = self.dataManager.fetch_available_data()
        self.loadItems(self.availableList, availableSourceList, AVAILABLE)

    def loadItems(self, list_widget, data_list, mode):
        for data in data_list:
            item  = QtGui.QListWidgetItem(list_widget)
            item.setSizeHint(QSize(250, 32))
            asw = ASItemWidget(self, data, item, mode, self.package)
            list_widget.setItemWidget(item, asw)
