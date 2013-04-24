#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


class Plugin(object):
    """Parent class for all plugins.
    ⌥: Main > Plugins > {n}(some of Plugin child class)."""

    def __init__(self):

        self.icon = None
        self.menu = None
        self.sensitive = True


    def set_sensitive(self, boolean):

        self.sensitive = boolean
        if hasattr(main, 'gui'):
            main.gui.menubar.set_sensitive(self, boolean)
            main.gui.headbar.set_sensitive(self, boolean)


class PluginTool(Plugin):
    """Parent class for tool plugins.
    ⌥: Main > Plugins > {n}PluginTool."""

    def __init__(self):

        Plugin.__init__(self)
        self.type = 'tool'

    def enable(self): pass
    def disable(self): pass
    def button_primary(self, x, y, ux, uy): pass
    def button_secondary(self, x, y, ux, uy): pass
    def motion_primary(self, x, y, ux, uy): pass
    def motion_secondary(self, x, y, ux, uy): pass
    def motion_over(self, x, y, ux, uy): pass
    def release_primary(self): pass
    def release_secondary(self): pass
    def key_press(self, keyval): return False


class PluginLauncher(Plugin):
    """Parent class for launcher plugins.
    ⌥: Main > Plugins > {n}PluginLauncher."""

    def __init__(self):

        Plugin.__init__(self)
        self.type = 'launcher'


class PluginDialog(Plugin):
    """Parent class for dialog plugins.
    ⌥: Main > Plugins > {n}PluginDialog."""

    def __init__(self):

        Plugin.__init__(self)
        self.type = 'dialog'


class PluginToggle(Plugin):
    """Parent class for toggle plugins.
    ⌥: Main > Plugins > {n}PluginToogle."""

    def __init__(self):

        Plugin.__init__(self)
        self.type = 'toggle'
        self.state = False


    def set_state(self, boolean, switch=True):

        self.state = boolean
        if switch: self.callback()


    def callback(self):

        if self.state: self.switch_off()
        else: self.switch_on()
        self.state ^= 1                                         # Switch state.
