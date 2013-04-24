#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.plugin import *


class Undo(PluginLauncher):

    def __init__(self):

        # Subclass it.
        PluginLauncher.__init__(self)

        # Common attributes.
        self.name = 'undo'
        self.author = 'nathive-dev'
        self.menu = 'edit'
        self.label = _('Undo')
        self.icon = 'gtk-undo'
        self.set_sensitive(False)


    def callback(self):
        """To do when the plugin is called."""

        # Call undo action.
        actions = main.documents.active.actions
        actions.undo()

        # Update own and redo sentitive.
        self.update_sensitive()
        main.plugins.get_plugin('redo').update_sensitive()


    def update_sensitive(self):

        actions = main.documents.active.actions
        if actions.history: self.set_sensitive(True)
        else: self.set_sensitive(False)
