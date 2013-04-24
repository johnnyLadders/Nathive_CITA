#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import re
import optparse
from commands import getoutput as sh


# Get options from command line.
optparser = optparse.OptionParser()
optparser.add_option('-t', action='store_true', dest='totabs')
optparser.add_option('-s', action='store_true', dest='tospaces')
optparser.add_option('-w', action='store_true', dest='overwrite')
(options, args) = optparser.parse_args()

# Print allowed systax if there is no options.
if len(sys.argv) == 1:
    sys.exit('python indenter.py -t|-s [-w] <file-or-folder>')

# Get target from command line and set max allowed indentation.
target = args[0]
maxlevel = 10

# Set indentation properties from tabs to spaces.
if options.tospaces:
    inchar = '\t'
    outchar = ' '
    inmultiplier = 1
    outmultiplier = 4

# Set indentation properties from spaces to tabs.
if options.totabs:
    inchar = ' '
    outchar = '\t'
    inmultiplier = 4
    outmultiplier = 1

# If a folder target is given find files path,
# else the given file is the unique path.
if os.path.isdir(target):
    pypaths = sh('find %s -name "*.py"' % target)
    cypaths = sh('find %s -name "*.cy"' % target)
    pypaths = pypaths.split('\n')
    cypaths = cypaths.split('\n')
    paths = pypaths + cypaths
else:
    paths = [target]

# Iterate over paths.
for path in paths:

    # Retrieve file data.
    handler = open(path)
    data = handler.read()

    # Check indent type.
    has_spaces = True if re.search('\n ', data) else False
    has_tabs = True if re.search('\n\t', data) else False

    # Abort if reindent is not needed (stdout mode never aborts).
    if options.overwrite:
        if options.totabs and not has_spaces: continue
        if options.tospaces and not has_tabs: continue

    # Indent.
    for level in range(maxlevel, 0, -1):
        data = re.sub(
            '\n[%s]{%s}' % (inchar, level * inmultiplier),
            '\n%s' % (outchar * level * outmultiplier),
            data)

    # Trim spaces at line end.
    data = re.sub('[ |\t]+\n', '\n', data)

    # Trim blank lines at file end.
    data = re.sub('[ |\t|\n]+$', '', data)

    # Add newline at end of file.
    data += '\n'

    # Overwrite (or stdout) modified file.
    if options.overwrite:
        handler.close()
        handler = open(path, 'w')
        handler.write(data)
    else:
        print data
