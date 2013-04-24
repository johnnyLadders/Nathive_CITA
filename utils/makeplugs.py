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


cyscript = 'python -B utils/cybuild.py'
extscript = 'python utils/extbuild.py'
sourcedir = 'nathive/plugins'
dest = 'nathive/libc'

for source in os.listdir(sourcedir):

    # Exit if file is not Cy, get full path.
    if not source.endswith('.cy'): continue
    sourcepath = os.path.join(sourcedir, source)

    # Build the C file from Cy, print builder output.
    command = ' '.join([cyscript, sourcepath, sourcedir])
    errors = commands.getoutput(command)
    if errors: print errors

    # Work with the created C file,
    sourcepath = sourcepath.replace('.cy', '.c')

    # Build so file from C, print builder output.
    command = ' '.join([extscript, sourcepath, dest])
    print commands.getoutput(command)

    # Remove useless C file.
    os.remove(sourcepath)
