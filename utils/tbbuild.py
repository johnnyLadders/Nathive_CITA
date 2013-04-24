#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import tarfile
import platform
import ConfigParser


# Get version.
parser = ConfigParser.RawConfigParser()
parser.read('META')
version = parser.get('meta', 'version')

# Configure tgz container.
tarname = 'nathive-%s.tgz' % version
tar = tarfile.open(tarname, "w:gz")

# Pack all into container and close it.
filenames = os.listdir('.')
if '.bzr' in filenames: filenames.remove('.bzr')
for filename in filenames: tar.add(filename, 'nathive/%s' % filename)
tar.close()

# Final message.
if os.path.exists(tarname):
    print '\n**** %s successfully created\n' % tarname
