#!/usr/bin/python
# -*- coding: utf-8 -*-
from string import strip
import random

class Document:
    def __init__(self, filename):
        self.lines = map( strip, open(filename).readlines() )
        self.current_line = -1
        self.size = len(self.lines)

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

    def merge(self):
        """Merges text and author fields as two paragraphs."""
        # might need some quoting for " here.
        self.merged_text = '<p>%s</p>' % self.text
        if self.author:
            self.merged_text += '<p align="right"><strong><i>%s</i></strong></p>' % self.author

    def __repr__(self):
        return self.merged_text
    def __unicode__(self):
        return unicode(self.__repr__())
