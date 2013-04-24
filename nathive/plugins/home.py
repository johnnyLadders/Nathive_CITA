#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk
import webbrowser

from nathive.lib.plugin import *


class Home(PluginLauncher):

    def __init__(self):

        # Subclass it.
        PluginLauncher.__init__(self)

        # Common attributes.
        self.name = 'home'
        self.author = 'nathive-dev'
        self.type = 'launcher'
        self.menu = 'help'
        self.label = _('Nathive website')
        self.icon = 'gtk-home'


    def callback(self):
        """To do when the plugin is called."""

        webbrowser.open('http://www.nathive.org')
