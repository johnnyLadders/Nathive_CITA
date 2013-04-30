#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.

"""
This is a syntax abstraction layer that convert .cy code in .c code ready to
generate a Python extension .so file. It's like a little brother of Cython
<http://www.cython.org/> but here the aim is not to get a fully Python
interoperability, just the basic language features to manipulate pixels at low
level. Currently the implementation is done using the included Dotcy library.

The Dotcy features are:
- Manage automatically input and output argument types between Python and C.
- Provide multiplatform acquisition system for pixel buffers.
- Support for the basic Python syntax.
- Manage relative imports in pythonic way.
"""

import os
import sys

from dotcy.script import Script


# If no arguments given.
if len(sys.argv) < 3:
    print 'python cybuild.py <source-file> <destination-folder>'
    sys.exit(0)

# Get source and destination from CLI.
source = os.path.abspath(sys.argv[1])
destination = os.path.abspath(sys.argv[2])

# Paths validation and formating.
if not os.path.exists(source): sys.exit('%s does not exists' % source)
if not os.path.isdir(destination): sys.exit('%s is not dir' % destination)
head, tail = os.path.split(source)
name, fileext = os.path.splitext(tail)

# Transcribe to C using the dotcy lib, save to destination.
try:
    script = Script(source)
except:
    print "source: " + str(source)
path = os.path.join(destination, '%s.c' % name)
script.export(path)
