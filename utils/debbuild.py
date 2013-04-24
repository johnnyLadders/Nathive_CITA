#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import platform
import commands
import ConfigParser


# Fix folders permissions.
os.system('chmod 755 ./utils/deb/usr')
os.system('chmod 755 ./utils/deb/usr/bin')
os.system('chmod 755 ./utils/deb/usr/share/doc')
os.system('chmod 755 ./utils/deb/usr/share/applications')

# Set config files parser.
parser = ConfigParser.RawConfigParser()
parser.read('META')

# Parse meta data.
version = parser.get('meta', 'version')
release = parser.get('meta', 'release')
phase = parser.get('meta', 'phase')
maintainer = parser.get('meta', 'maintainer')
arch = platform.machine().replace('i686', 'i386').replace('x86_64', 'amd64')
size = 0
for (dirpath, dirnames, filenames) in os.walk('./utils/deb'):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        size += os.path.getsize(filepath) / 1024
size = str(size)

# Set Debian control file.
data = open('./utils/debdata').read()
data = data.replace('$arch', arch)
data = data.replace('$version', version)
data = data.replace('$release', release)
data = data.replace('$phase', phase)
data = data.replace('$size', size)
data = data.replace('$maintainer', maintainer)
open('./utils/deb/DEBIAN/control', 'w').write(data)

# Build DEB package.
package = 'nathive_%s-%s_%s.deb' % (version, release, arch)
os.system('rm -f %s' % package)
print commands.getoutput('dpkg -b ./utils/deb %s' % package)
os.system('rm -rf ./utils/deb')

# Final message.
if os.path.exists(package):
    print ''
    print '**** DEB package was successfully created'
    print ''
    print '     to install:'
    print '     - dpkg -i %s' % package
    print '     - or double-click the package'
    print ''
else:
    print ''
    print '**** An error occurred while building DEB package'
    print ''
