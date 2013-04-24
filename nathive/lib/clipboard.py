#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


class Clipboard(object):

    def __init__(self):

        self.data = None
        self.width = None
        self.height = None

    def copy(self, data, width=None, height=None):

        self.data = data
        self.width = width
        self.height = height


    def paste(self):

        return (self.data, self.width, self.height)
