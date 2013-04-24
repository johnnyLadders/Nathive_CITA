#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.plugin import *


class ViewFullscreen(PluginToggle):

    def __init__(self):

        # Subclass it.
        PluginToggle.__init__(self)

        # Common attributes.
        self.name = 'view-fullscreen'
        self.author = 'nathive-dev'
        self.menu = 'view'
        self.label = _('Fullscreen')
        self.set_state(False, False)


    def switch_on(self):

        main.gui.window.fullscreen()


    def switch_off(self):

        main.gui.window.unfullscreen()
