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

from string import strip
import random
import re
import os
import tarfile

class Document:
    def __init__(self, filename):
	self.ungz_if_needed(filename)
        self.lines = map( strip, open(filename).readlines() )
        self.current_line = -1
        self.size = len(self.lines)

    def ungz_if_needed(self, filename):
	"""Checks if input file exists. If it does not, tries to ungz the tar archive.
	If neither that exists, raises Exception."""
	if os.path.exists(filename):
	    return
	
	tarname = filename+".tar.gz"
	if os.path.exists(tarname):
	    tar = tarfile.open(filename, 'r:gz')
	    for item in tar:
		tar.extract(item)
	else:
	    raise Exception, "Neither %s nor %s does not exist." % (filename, tarname)
	
    def get_random_line(self):
        return Line( random.choice(self.lines) )

    def get_next_line(self):
        self.current_line += 1
        if self.current_line >= self.size:
            self.current_line = 0
        return Line( self.lines[self.current_line] )


    def get_previous_line(self):
        self.current_line -= 1
        if self.current_line < 0:
            # yes this is required as after -1*size, it blows up!
            self.current_line = self.size - 1
        return Line( self.lines[self.current_line] )


class Line:
    def __init__(self, line):
        self.text, self.author = line.split("|")
        self.merge()

    def get_twitter_link(self):
	return "http://twitter.com/home?status=%s" % self.plain_text
    
    def get_ff_link(self):
	return "http://friendfeed.com/share/bookmarklet/frame#title=%s" % self.plain_text
	
    def get_twitter_href(self):
	return '<a href="%s" title="Click to share this on Twitter">Twitter</a>' % self.get_twitter_link()

    def get_ff_href(self):
	return '<a href="%s" title="Click to share this on FriendFeed">FriendFeed</a>' % self.get_ff_link()

    
    def remove_html_tags(self, data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)
	
    def merge(self):
        """Merges text and author fields as two paragraphs."""
        # might need some quoting for " here.
        self.plain_text = "%s" % self.remove_html_tags(self.text)
        self.html_text = '<p>%s</p>' % self.text
        if self.author:
	    self.plain_text += " -- %s" % self.remove_html_tags(self.author)
            self.html_text+= '<p align="right"><strong><i>%s</i></strong></p>' % self.author

	self.html_text += "<p>Share on %s</p>" % ( " / ".join( (self.get_twitter_href(), self.get_ff_href()) ) )
	
    def __repr__(self):
        return self.html_text
        
    def __unicode__(self):
        return unicode(self.__repr__())
