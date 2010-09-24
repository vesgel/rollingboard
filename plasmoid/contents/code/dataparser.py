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

class DataParser:

    def __init__(self):
        self.textColor = None
        self.authorColor = None

    def readFile(self, filename):
        sourceFile = open(filename, 'r')
        styleData = []

        ### NOTE: Not finished yet!
        for line in sourceFile:
            if line.startswith(':'):
                sectionKey = line.lstrip(':').strip().upper()
            else:
                data = line.strip()
                if data:
                    if sectionKey == "STYLE":
                        styleData.append(data)
                    elif sectionKey == "DATA":
                        print "data section"

        print styleData
        
        sourceFile.close()
