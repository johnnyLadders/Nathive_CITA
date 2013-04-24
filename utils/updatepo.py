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


pofiles = os.listdir('po')
for pofile in pofiles:
    cmd = 'msgmerge -N po/%s nathive.pot -o po/%s' % (pofile, pofile)
    commands.getoutput(cmd)
