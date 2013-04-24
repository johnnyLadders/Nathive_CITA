#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import shutil
import re
import ConfigParser
from commands import getoutput as sh

import docgen


# Relative paths for code and documentation bases.
code = '.'
docs = 'doc/source'

# Find and remove old documentation files.
rstfiles = sh('find %s -name *.rst -type f' % docs)
rstfiles = rstfiles.split('\n')
rstfiles = [x for x in rstfiles if '__init__.rst' not in x]
rstfiles = [x for x in rstfiles if 'index.rst' not in x]
for rstfile in rstfiles: os.remove(rstfile)

# List target folders
folders = [
    'nathive/lib',
    'nathive/gui',
    'utils/dotcy',
    'utils/docgen']

# Generate documentation.
for folder in folders:
    infolder = os.path.join(code, folder)
    outfolder = os.path.join(docs, folder)
    docfolder = docgen.DocFolder(infolder, outfolder)
    docfolder.generate()

# Get version data.
meta = ConfigParser.RawConfigParser()
meta.read('META')
version = meta.get('meta', 'version')
phase = meta.get('meta', 'phase')
release = '%s %s' % (version, phase)

# Change documentation version.
confpath = os.path.join(docs, 'conf.py')
confdata = open(confpath).read()
confdata = re.sub("version = '.*'", "version = '%s'" % version, confdata)
confdata = re.sub("release = '.*'", "release = '%s'" % release, confdata)
open(confpath, 'w').write(confdata)
