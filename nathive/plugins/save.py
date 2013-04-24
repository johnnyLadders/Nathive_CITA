#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.plugin import *


class Save(PluginLauncher):

    def __init__(self):
        """To do when the plugin is loaded at program start."""

        # Subclass it.
        PluginLauncher.__init__(self)

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Common attributes.
        self.name = 'save'
        self.author = 'nathive-dev'
        self.menu = 'file'
        self.label = _('Save')
        self.icon = 'gtk-save'


    def callback(self):
        """To do when the plugin is called."""

        # Stop if none is open.
        if not main.documents.active: return

        # Alias.
        saveas = main.plugins.get_plugin('saveas')
        document = main.documents.active
        path = document.path

        # If the document is unsaved or the mime is not valid to rewrite
        # display the save-as dialog, else overwite the file.
        if not path:
            saveas.callback()
        else:
            if document.mime == 'image/openraster': format = 'ora'
            elif document.mime == 'image/png': format = 'png'
            elif document.mime == 'image/jpeg': format = 'jpg'
            else:
                saveas.callback()
                return
            saveas.save(path, format)
