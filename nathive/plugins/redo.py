#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.plugin import *


class Redo(PluginLauncher):

    def __init__(self):

        # Subclass it.
        PluginLauncher.__init__(self)

        # Common attributes.
        self.name = 'redo'
        self.author = 'nathive-dev'
        self.menu = 'edit'
        self.label = _('Redo')
        self.icon = 'gtk-redo'
        self.set_sensitive(False)


    def callback(self):
        """To do when the plugin is called."""

        # Call redo action.
        actions = main.documents.active.actions
        actions.redo()

        # Update own and undo sentitive.
        self.update_sensitive()
        main.plugins.get_plugin('undo').update_sensitive()


    def update_sensitive(self):

        actions = main.documents.active.actions
        if actions.rehistory: self.set_sensitive(True)
        else: self.set_sensitive(False)
