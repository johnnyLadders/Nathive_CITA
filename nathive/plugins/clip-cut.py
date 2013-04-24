#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.plugin import *


class ClipCut(PluginLauncher):

    def __init__(self):

        # Subclass it.
        PluginLauncher.__init__(self)

        # Common attributes.
        self.name = 'clip-cut'
        self.author = 'nathive-dev'
        self.menu = 'edit'
        self.label = _('Cut')
        self.icon = 'gtk-cut'


    def callback(self):
        """To do when the plugin is called."""

        document = main.documents.active
        if not document: return
        layer = document.layers.active
        if not layer: return
        main.clipboard.copy(
            layer.pixbuf.get_pixels(),
            layer.width,
            layer.height)

        document.layers.remove(layer)
