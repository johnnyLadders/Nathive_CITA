#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import re


# Get app directory from makefile.
make = open('makefile').read()
base = re.search('BASE = (.*)', make).group(1)
tail = re.search('APP = (.*)', make).group(1)
appdir = os.path.join(base, tail)

# Replace appdir in sh template.
sh = open('utils/shdata').read()
sh = sh.replace('$appdir', appdir)

# Write sh file.
shfile = open('nathive.sh', 'w')
shfile.write(sh)
shfile.close()

# Set meta appdir.
meta = open('META').read()
replacement = 'appdir = %s' % appdir
meta = re.sub('appdir =(.*)', replacement, meta)
metafile = open('META', 'w')
metafile.write(meta)
metafile.close()
