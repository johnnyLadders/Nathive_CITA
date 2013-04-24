#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import re

import docgen


class DocClass(object):

    def __init__(self, code):

        self.code = code
        self.name = ''
        self.parent = ''
        self.title = ''
        self.logic = ''
        self.docstring = ''
        self.methods = []
        self.parse()


    def parse(self):

        definition = self.code[0]
        res = re.search('class (.*)\((.*)\):', definition)
        self.name = res.group(1)
        self.parent = res.group(2)
        self.title = 'class %s' % self.name
        if self.parent != 'object': self.title += '(%s)' % self.parent

        self.code.append('')
        methodlines = []
        for i, line in enumerate(self.code):
            if line.startswith('\tdef '): methodlines.append(i)
        for i, methodline in enumerate(methodlines):
            start = methodline
            if i+1 < len(methodlines): end = methodlines[i+1] - 1
            else: end = -1
            if start != end: methodcode = self.code[start:end]
            else: methodcode = [self.code[start]]
            amethod = docgen.DocMethod(methodcode, self.name)
            if amethod.name == '__del__': continue
            self.methods.append(amethod)


    def dump(self):

        rst = ''
        rst += '\n\n\n%s\n' % self.title
        rst += '-' * len(self.title)
        for method in self.methods: rst += method.dump()
        return rst
