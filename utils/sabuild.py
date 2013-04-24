#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import shutil
import tarfile
import platform
import ConfigParser


# Test if low-level libraries are compiled.
if not os.path.exists('./nathive/libc/core.so'):
    print '\n**** ERROR: Low-level libraries seems to be not compiled\n'
    sys.exit(0)

# Set folder names, remove if exists previously.
dest = './utils/standalone/'
if os.path.exists(dest): shutil.rmtree(dest)

# Copy all to work folder.
ignore = shutil.ignore_patterns('standalone')
shutil.copytree('./', dest, False, ignore)

# Set files and folder to remove.
useless_files = ['makefile', 'nathive.desktop', 'nathive.sh', 'TODO']
useless_dirs = ['nin', 'utils', '.bzr']

# Remove files.
for filename in useless_files:
    path = os.path.join(dest, filename)
    os.remove(path)

# Remove folders.
for dirname in useless_dirs:
    path = os.path.join(dest, dirname)
    shutil.rmtree(path, True)

# Get version and architecture.
parser = ConfigParser.RawConfigParser()
parser.read('META')
version = parser.get('meta', 'version')
arch = platform.machine()
arch = arch.replace('i686', 'x86')
arch = arch.replace('x86_64', 'x64')

# Configure tgz container.
tarname = 'nathive-%s-%s.tgz' % (version, arch)
tar = tarfile.open(tarname, "w:gz")

# Pack work folder into container and close it.
tar.add(dest, 'nathive')
tar.close()

# Remove work folder.
shutil.rmtree(dest)

# Final message.
if os.path.exists(tarname):
    print '\n**** %s successfully created\n' % tarname
