#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk

from nathive.lib.plugin import *
from nathive.libc import picker


class Picker(PluginTool):

    def __init__(self):

        # Subclass it.
        PluginTool.__init__(self)

        # Common attributes.
        self.name = 'picker'
        self.author = 'nathive-dev'
        self.icon = 'tool-picker.png'


    def button_primary(self, x, y, ux, uy):

        rgb = picker.pick(
            main.documents.active.pointer,
            main.documents.active.width,
            x,
            y)

        main.color.set_color_from_rgb(rgb)


    def motion_primary(self, x, y, ux, uy):

        self.button_primary(x, y, ux, uy)


    def gui(self):

        return gtk.VBox()
