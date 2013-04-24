#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import re


class DocString(object):

    def __init__(self, lines):

        self.lines = lines
        self.docstring = ''
        self.parameters = []
        self.returninfo = ''
        self.parse()


    def parse(self):

        for line in self.lines:
            line = line.strip('\t')
            line = line.strip('"""')
            if line.startswith('@'):
                res = re.search('@(.*): (.*)', line)
                paramname = res.group(1)
                paraminfo = res.group(2)
                self.parameters.append((paramname, paraminfo))
            elif line.startswith('='):
                returninfo = line.replace('=return: ', '')
                self.returninfo = returninfo
            else: self.docstring += line + ' '


    def hasinfo(self):

        if self.docstring: return True
        if self.parameters: return True
        if self.returninfo: return True
        return False


    def dump_docstring(self):

        rst = ''
        if self.docstring: rst += '\n\n   %s' % self.docstring
        return rst


    def dump_parameters(self):

        rst = ''
        if self.parameters:
            for paramname, paraminfo in self.parameters:
                rst += '\n   | ``%s: %s``' % (paramname, paraminfo)
        if self.returninfo:
            rst += '\n   | ``RETURNS: %s``' % self.returninfo
        if rst: rst = '\n' + rst
        return rst


    def dump_noinfo(self):

        rst = ''
        message = 'no doctring or additional documentation, too bad.'
        rst += '\n\n   .. warning:: %s' % message
        return rst
