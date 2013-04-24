#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import re
import platform

from dotcy.line import Line
from dotcy import types


class Function(object):

    def __init__(self, code):

        self.lines = code.splitlines()
        self.private = False

        self.rawdef = self.lines[0]
        self.rawdef = self.rawdef.replace(' ', '')
        self.rawdef = self.rawdef.replace('\t', '')
        self.name, self.args, self.itypes, self.otypes = self.parse_def()

        self.lines.pop(0)
        self.lines = [x for x in self.lines if x]
        self.lines = [Line(x, self) for x in self.lines]


    def parse_def(self):

        # Explode definition in elements.
        pattern = "(.*)\((.*),'(.*)'\)"
        name, args, io = re.search(pattern, self.rawdef).groups()

        # Process name.
        if name.startswith('__'):
            name = name[2:]
            self.private = True

        # Process arguments and types.
        args = args.split(',')
        itypes, otypes = io.split(':')

        # Return as tuple.
        return name, args, itypes, otypes


    def dump(self):

        # Init dump string.
        dumped = ''

        # Dump function definition.
        if self.private: dumped += self.dump_def_private()
        else: dumped += self.dump_def_public()

        # Dump lines.
        lastindent = 0
        for line in self.lines:
            indent = line.get_indent()
            if indent < lastindent:
                diff = lastindent - indent
                for i in range(diff):
                    dent = '\t' * (indent + diff - i - 1)
                    dumped += '%s}\n' % dent
            dumped += line.dump()
            lastindent = indent

        # Close last line indents.
        if lastindent > 0:
            for i in range(lastindent - 1):
                dent = '\t' * (lastindent - i - 1)
                dumped += '%s}\n' % dent

        # Mandatory return.
        if self.private: dumped += '\treturn 0;\n'
        else: dumped += '\treturn Py_BuildValue("");\n'

        # Close function.
        dumped += '}\n\n'

        # Return dump string for this function.
        return dumped


    def dump_def_private(self):

        dumped = ''
        args = []
        itypes = [types.full_name(x) for x in self.itypes]
        otype = types.full_name(self.otypes)

        for i, arg in enumerate(self.args):
            args.append('%s %s' % (itypes[i], arg))

        args = ', '.join(args)
        definition = '%s %s(%s)\n{\n' % (otype, self.name, args)
        dumped += definition
        return dumped


    def dump_def_public(self):

        # Init dump string.
        dumped = ''

        # Write function definition to receive Python objects.
        dumped += 'PyObject *%s' % self.name
        dumped += '(PyObject *self, PyObject *args)\n{\n'

        # Init variables.
        for i, itype in enumerate(self.itypes):
            typename = types.full_name(itype)
            arg = self.args[i]
            if itype == 'P': arg += '_'
            dumped += '\t%s %s;\n' % (typename, arg)

        # Convert input matrix to Python spec.
        pytypes = [types.python_char(x) for x in self.itypes]
        pytypes = ''.join(pytypes)

        # Create a comma-separated list of variable addresses.
        addresses = []
        for i, itype in enumerate(self.itypes):
            arg = self.args[i]
            if itype == 'P': arg += '_'
            addresses.append('&%s' % arg)
        addresses = ', '.join(addresses)

        # Write the ParseTuple function.
        formatter = pytypes, addresses
        dumped += '\tPyArg_ParseTuple(args, "%s", %s);\n' % formatter

        # Redirect pixel buffer address with given pointer.
        for i, itype in enumerate(self.itypes):
            if itype == 'P':
                arg = self.args[i]
                bits, linkage = platform.architecture()
                if bits == '32bit': cast = '(unsigned char*)(long int)'
                if bits == '64bit': cast = '(unsigned char*)'
                dumped += '\tunsigned char *%s = %s%s_;\n' % (arg, cast, arg)

        # Return dump string for this function.
        return dumped
