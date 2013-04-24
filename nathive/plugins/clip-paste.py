#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.plugin import *


class ClipPaste(PluginLauncher):

    def __init__(self):

        # Subclass it.
        PluginLauncher.__init__(self)

        # Common attributes.
        self.name = 'clip-paste'
        self.author = 'nathive-dev'
        self.menu = 'edit'
        self.label = _('Paste')
        self.icon = 'gtk-paste'


    def callback(self):
        """To do when the plugin is called."""

        document = main.documents.active
        if not document: return
        data, width, height = main.clipboard.paste()
        document.layers.append_from_data(data, width, height)
