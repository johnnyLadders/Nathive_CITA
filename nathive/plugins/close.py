#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.plugin import *


class Close(PluginLauncher):

    def __init__(self):

        # Subclass it.
        PluginLauncher.__init__(self)

        # Common attributes.
        self.name = 'close'
        self.author = 'nathive-dev'
        self.menu = 'file'
        self.label = _('Close')
        self.icon = 'gtk-close'


    def callback(self):
        """To do when the plugin is called."""

        document = main.documents.active
        if document: main.documents.close(document)
