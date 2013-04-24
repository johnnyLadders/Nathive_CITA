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
os.system('chmod 755 ./utils/rpm/SOURCES/nathive/usr')
os.system('chmod 755 ./utils/rpm/SOURCES/nathive/usr/bin')
os.system('chmod 755 ./utils/rpm/SOURCES/nathive/usr/share/doc')
os.system('chmod 755 ./utils/rpm/SOURCES/nathive/usr/share/applications')

# Set config files parser.
parser = ConfigParser.RawConfigParser()
parser.read('META')

# Parse meta data.
version = parser.get('meta', 'version')
release = parser.get('meta', 'release')
phase = parser.get('meta', 'phase')
maintainer = parser.get('meta', 'maintainer')
arch = platform.machine().replace('i686', 'i386')

# Set RPM spec file.
data = open('./utils/rpmdata').read()
data = data.replace('$arch', arch)
data = data.replace('$version', version)
data = data.replace('$release', release)
data = data.replace('$phase', phase)
data = data.replace('$maintainer', maintainer)
data = data.replace('$cwd', os.getcwd())
open('./utils/rpm/nathive.spec', 'w').write(data)

# Build RPM package.
package = 'nathive-%s-%s.%s.rpm' % (version, release, arch)
os.system('rm -f %s' % package)
cwd = os.getcwd()
print commands.getoutput(
    'rpmbuild '
    '-bb '
    '--buildroot %s/utils/rpm/SOURCES/nathive '        # Bug http://ur1.ca/z7uq
    'utils/rpm/nathive.spec' % cwd)

# Moving the package to the source folder.
print 'moving RPM to %s' % cwd
os.system('mv utils/rpm/%s/%s %s' % (arch, package, package))

# Remove build folders.
os.system('rm -rf ./utils/rpm')
hasfiles = bool(commands.getoutput('find ~/rpmbuild -type f'))
if not hasfiles: os.system('rm -rf ~/rpmbuild')

# Final message.
if os.path.exists(package):
    print ''
    print '**** RPM package was successfully created'
    print ''
    print '     to install:'
    print '     - rpm -i %s' % package
    print '     - or double-click the package'
    print ''
else:
    print ''
    print '**** An error occurred while building RPM package'
    print ''
