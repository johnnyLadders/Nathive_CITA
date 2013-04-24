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
import commands
import distutils.core
import StringIO

# if no arguments given.
if len(sys.argv) < 3:
    print 'python extbuild.py <source> <destination>'
    sys.exit(0)

# Get args and perform the whims of distutils.core.setup.
source = os.path.abspath(sys.argv[1])
destination = os.path.abspath(sys.argv[2])
sys.argv[1] = 'build'
sys.argv.pop()

# Paths validation and formating.
if not os.path.exists(source): sys.exit('%s does not exists' % source)
if not os.path.isdir(destination): sys.exit('%s is not dir' % destination)
path, tail = os.path.split(source)
name, fileext = os.path.splitext(tail)

# Set extesion modules.
modules = distutils.core.Extension(name, ['%s/%s' % (path, tail)])

# Redirect standard output temporally.
altout = StringIO.StringIO()
orgout = sys.stdout
sys.stdout = altout

# Build C extension with distutils.
distutils.core.setup(
    name = name,
    description = 'Nathive %s extension' % name,
    ext_modules = [modules])

# Reset standard output, filter and print messages.
sys.stdout = orgout
messages = altout.getvalue().split('\n')
for message in messages:
    if not message.startswith('creating'):
        print message

# Search and replace extension.
extpath = commands.getoutput('find ./build | grep %s.so' % name)
os.rename(extpath, '%s/%s.so' % (destination, name))
commands.getoutput('rm -r ./build')
print '**** %s.so created into %s/\n' % (name, destination)
