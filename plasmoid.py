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

import optparse
import os

NAME_OF_PLASMOID = "rollingboard"

def main():
    p = optparse.OptionParser()
    
    p.add_option('--archive', '-a', action='store_true')
    p.add_option('--install', '-i', action='store_true')
    p.add_option('--remove', '-r', action='store_true')
    p.add_option('--view', '-v', action='store_true')
    p.add_option('--test', '-t', action='store_true')
    
    options, args = p.parse_args()

    if options.archive:
        os.system('zip -r ./%s.zip plasmoid/' % NAME_OF_PLASMOID)
    elif options.install:
        os.system('plasmapkg -i %s.zip' % NAME_OF_PLASMOID)
    elif options.remove:
        os.system('plasmapkg -r %s' % NAME_OF_PLASMOID)
    elif options.view:
        os.system('plasmoidviewer %s' % NAME_OF_PLASMOID)
    elif options.test:
        os.system('plasmapkg -r %s' % NAME_OF_PLASMOID)
        os.system('zip -r ./%s.zip plasmoid/' % NAME_OF_PLASMOID)
        os.system('plasmapkg -i %s.zip' % NAME_OF_PLASMOID)
        os.system('plasmoidviewer %s' % NAME_OF_PLASMOID)

if __name__ == '__main__':
    main()