#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk

from nathive.plugins.brush import Brush
from nathive.lib.layer import Layer
from nathive.gui import utils as gutils
from nathive.gui.multiwidget import *


class Eraser(Brush):

    def __init__(self):

        # Subclass it.
        Brush.__init__(self)

        # Plugin attributes.
        self.name = 'eraser'
        self.author = 'nathive-dev'
        self.icon = 'tool-eraser.png'

        # Load own plugin values.
        main.config.push_to_plugin(self)

        # Override composite mode, idle color update.
        self.composite_mode = 2
        self.color_updated_todo = []


    @property
    def color(self):
        """Override color usage to black permanently."""

        return [0] * 3
