#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import commands

import docgen


class DocFile(object):

    def __init__(self, path):

        self.path = path
        code = commands.getoutput('python utils/indenter.py -t %s' % path)
        self.code = code.splitlines()
        self.name = ''
        self.title = ''
        self.classes = []
        self.parse()


    def parse(self):

        head, tail = os.path.split(self.path)
        name, ext = os.path.splitext(tail)
        self.name = name
        #self.title = '%s: %s' % (self.group, self.name)
        self.title = self.name

        self.code.append('')
        classlines = []
        for i, line in enumerate(self.code):
            if line.startswith('class '): classlines.append(i)
        for i, classline in enumerate(classlines):
            start = classline
            if i+1 < len(classlines): end = classlines[i+1] - 1
            else: end = -1
            classcode = self.code[start:end]
            aclass = docgen.DocClass(classcode)
            self.classes.append(aclass)


    def dump(self):

        rst = ''
        rst += self.title + '\n'
        rst += '=' * len(self.title)
        for aclass in self.classes:	rst += aclass.dump()
        return rst
