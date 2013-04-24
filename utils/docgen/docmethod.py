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


class DocMethod(object):

    def __init__(self, code, parent):

        self.code = code
        self.parent = parent
        self.name = ''
        self.parameters = []
        self.docstring = ''
        self.parse()


    def parse(self):

        definition = self.code[0]
        res = re.search('def (.*)\((.*)\):', definition)
        self.name = res.group(1)
        rawparams = res.group(2)
        rawparams = rawparams.replace(' ', '')
        self.parameters = rawparams.split(',')
        self.parameters.remove('self')

        isdocline = False
        doclines = []
        for line in self.code:
            if line.startswith('\t\t"""'): isdocline = True
            if isdocline: doclines.append(line)
            if line.endswith('"""'): isdocline = False
        self.docstring = docgen.DocString(doclines)


    def dump(self):

        rst = ''
        params = ', '.join(self.parameters)
        rst += '\n\n\n.. method:: %s.%s(%s)' % (self.parent, self.name, params)
        if self.docstring.hasinfo():
            rst += self.docstring.dump_docstring()
            rst += self.docstring.dump_parameters()
        else:
            rst += self.docstring.dump_noinfo()
        return rst
