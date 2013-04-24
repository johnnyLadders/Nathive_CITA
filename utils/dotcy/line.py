#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import re

from dotcy import types


class Line(object):

    def __init__(self, line, function):

        self.function = function
        self.line = line
        self.cline = None


    def get_indent(self):

        line = re.sub('    ', '\t', self.line)
        return len(re.findall('\t', line))


    def process_as_init(self):

        typechar = re.search('type (.*):', self.cline).group(1)
        typename = types.full_name(typechar)
        variables = re.search(':(.*)', self.cline).group(1)
        self.cline = '%s%s;' % (typename, variables)


    def process_as_conditional(self):

        self.cline = re.sub('if (.*?):' ,'if(\\1):', self.cline)
        if re.search(':(.+)', self.cline):
            self.cline = re.sub(':(.+)' ,'\\1;', self.cline)
            self.cline = self.cline.replace(':', '')
        else:
            self.cline = self.cline.replace(':', '')
            dent = '\t' * self.get_indent()
            self.cline += '\n%s{' % dent


    def process_as_conditional_out(self):

        if re.search(':(.+)', self.cline):
            self.cline = re.sub(':(.+)' ,'\\1;', self.cline)
            self.cline = self.cline.replace(':', '')
        else:
            self.cline = self.cline.replace(':', '')
            dent = '\t' * self.get_indent()
            self.cline += '\n%s{' % dent


    def process_as_loop(self):

        ipattern = 'for (.*) in range\((.*)\):'
        opattern = 'for(\\1=0; \\1<\\2; \\1++):'
        self.cline = re.sub(ipattern, opattern, self.cline)

        if re.search(':(.+)', self.cline):
            self.cline = re.sub(':(.+)' ,'\\1;', self.cline)
            self.cline = self.cline.replace(':', '')
        else:
            self.cline = self.cline.replace(':', '')
            dent = '\t' * self.get_indent()
            self.cline += '\n%s{' % dent


    def process_as_idle(self):

        self.cline = self.cline + ';'


    def perform_returns(self):

        if self.function.private: return
        returnvars = re.search('return (.+)', self.cline)
        if not returnvars: return
        returnvars = returnvars.group(1)

        if returnvars == '0':
            self.cline = re.sub(
                'return 0',
                'return Py_BuildValue("")',
                self.cline)
        else:
            otypes = self.function.otypes
            pytypes = [types.python_char(x) for x in otypes]
            pytypes = ''.join(pytypes)
            returnvars = '"%s", %s' % (pytypes, returnvars)
            self.cline = re.sub(
                'return (.+)',
                'return Py_BuildValue(%s)' % returnvars,
                self.cline)


    def dump(self):

        # Init C transcribed line.
        self.cline = self.line

        # Replace operators.
        self.cline = self.cline.replace(' and ', ' && ')
        self.cline = self.cline.replace(' or ', ' || ')
        self.cline = self.cline.replace(' not ', ' !')

        # Replace booleans.
        self.cline = self.cline.replace('True', '1')
        self.cline = self.cline.replace('False', '0')

        # Manage casts.
        chars = types.full_name()
        for char in chars.keys():
            searchto = '(%s)' % char
            replacewith = '(%s)' % types.full_name(char)
            self.cline = self.cline.replace(searchto, replacewith)

        # Remove indentation.
        self.cline = re.sub('    ', '\t', self.cline)
        self.cline = self.cline.replace('\t', '')
        if not self.cline: return ''

        # Fix non-value returns, compose public (to python) returns.
        self.cline = re.sub('return$', 'return 0', self.cline)
        self.perform_returns()

        # Detect line motif and process it.
        if self.cline.startswith('type '): self.process_as_init()
        elif self.cline.startswith('if '): self.process_as_conditional()
        elif self.cline.startswith('else:'): self.process_as_conditional_out()
        elif self.cline.startswith('for '): self.process_as_loop()
        else: self.process_as_idle()

        # Return dump string for this line.
        dent = '\t' * self.get_indent()
        return '%s%s\n' % (dent, self.cline)
