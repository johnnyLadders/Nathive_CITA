#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import re
import gtk


class Headbar(object):
    """Define headbar instance."""

    def __init__(self, parent):
        """Create headbar and buttons.
        @box: Parent widget"""

        # Create headbar (really is a GTK toolbar).
        self.toolbar = gtk.Toolbar()
        self.toolbar.set_style(gtk.TOOLBAR_ICONS)
        parent.pack_start(self.toolbar, False, False, 0)

        # Dictionary to access dumped buttons.
        self.buttons = {}

        # Add items.
        self.dump()


    def dump(self):
        """Filter sort list, dump to headbar, and push to config."""

        # Clean previous dumps.
        self.toolbar.foreach(self.toolbar.remove)
        self.buttons = {}

        # Alias.
        plugins = main.plugins.childs
        toolbar = self.toolbar

        # Get sort list from config.
        self.sort = main.config.get('sort', 'headbar').split(',')

        # Remove non-plugin from sort list.
        condition = lambda x: self.istag(x) or plugins.has_key(x)
        self.sort = [x for x in self.sort if condition(x)]

        # Remove tool plugins from sort list.
        condition = lambda x: self.istag(x) or plugins[x].type != 'tool'
        self.sort = [x for x in self.sort if condition(x)]

        # Dump each item to headbar.
        for name in self.sort:
            if self.istag(name):
                if name == '[S]': toolbar.insert(gtk.SeparatorToolItem(), -1)
                continue
            self.item(plugins[name])
        self.toolbar.show_all()

        # Push sort to config.
        main.config.set('sort', 'headbar', ','.join(self.sort))


    def istag(self, string):

        return re.search('^\[.*\]$', string)


    def item(self, plugin):
        """Append headbar buttons.
        @plugin: A callback-able plugin instance."""

        button = gtk.ToolButton(plugin.icon)
        button.set_icon_name(plugin.icon)
        button.set_sensitive(plugin.sensitive)
        button.connect('clicked', lambda w: plugin.callback())
        self.toolbar.insert(button, -1)
        self.buttons[plugin] = button


    def set_sensitive(self, plugin, boolean):

        self.buttons[plugin].set_sensitive(boolean)
