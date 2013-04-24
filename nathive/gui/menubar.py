#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk
import re


class Menubar(object):
    """The main window menu manager.
    ⌥: Main > Gui > Menubar."""

    def __init__(self, parent):
        """Create the menubar widget and submenus.
        @parent: Parent widget."""

        # Widget related.
        self.menubar = gtk.MenuBar()
        parent.pack_start(self.menubar, False, False, 0)

        # Dictionary to access dumped menu items.
        self.items = {}

        # Append menus.
        self.file = Menu(self, self.menubar, 'file', _('File'))
        self.edit = Menu(self, self.menubar, 'edit', _('Edit'))
        self.view = Menu(self, self.menubar, 'view', _('View'))
        self.help = Menu(self, self.menubar, 'help', _('Help'))

        # Show.
        self.menubar.show_all()


    def set_sensitive(self, plugin, boolean):

        self.items[plugin].set_sensitive(boolean)


class Menu(object):
    """Define menu instances contained in menubar."""

    def __init__(self, menubar, parent, name, label):
        """Create a menu.
        @menubar: The parent menubar to append in.
        @name: The menu name as string.
        @label: The menu title as string."""

        # Setting up attributes.
        self.menubar = menubar
        self.menu = gtk.MenuItem(label, True)
        self.submenu = gtk.Menu()
        parent.append(self.menu)
        self.menu.set_submenu(self.submenu)
        self.accelgroup = gtk.AccelGroup()
        self.name = name

        # Show.
        self.dump(True)


    def dump(self, addlost=False):
        """Filter sort list, dump to menu, and push to config."""

        # Alias.
        plugins = main.plugins.childs

        # Remove previous stuff.
        self.submenu.foreach(gtk.Widget.destroy)

        # Get sort list from config.
        option = 'menu%s' % self.name
        self.sort = main.config.get('sort', option).split(',')

        # Add lost plugins.
        if addlost:
            position = self.sort.index('[N]')
            for name, plugin in plugins.items():
                if name not in self.sort:
                    if plugins[name].type != 'tool':
                        if plugins[name].menu == self.name:
                            self.sort.insert(position + 1, name)

        # Remove non-plugin from sort list.
        condition = lambda x: self.istag(x) or plugins.has_key(x)
        self.sort = [x for x in self.sort if condition(x)]

        # Remove tool plugins from sort list.
        condition = lambda x: self.istag(x) or plugins[x].type != 'tool'
        self.sort = [x for x in self.sort if condition(x)]

        # Remove other menu childs form sort list.
        condition = lambda x: self.istag(x) or plugins[x].menu == self.name
        self.sort = [x for x in self.sort if condition(x)]

        # For each entry in sort list create a submenu.
        for name in self.sort:
            if self.istag(name):
                if name == '[S]': self.submenu.append(gtk.SeparatorMenuItem())
                continue
            self.item(plugins[name])
        self.menu.show_all()

        # Push sort to config.
        option = 'menu%s' % self.name
        main.config.set('sort', option, ','.join(self.sort))


    def istag(self, string):

        return re.search('^\[.*\]$', string)


    def item(self, plugin):
        """Create a new item into menu.
        @plugin: The plugin instance associated."""

        # Create the menuitem.
        if plugin.type == 'launcher' or plugin.type == 'dialog':
            item = gtk.ImageMenuItem(plugin.label, True)
        if plugin.type == 'toggle':
            item = gtk.CheckMenuItem(plugin.label, True)
            item.set_active(plugin.state)
        item.connect('activate', lambda x: plugin.callback())
        item.set_sensitive(plugin.sensitive)
        self.submenu.append(item)
        self.menubar.items[plugin] = item

        # Add image.
        if plugin.icon:
            isstock = plugin.icon.startswith('gtk-')
            if isstock: image = gtk.image_new_from_stock(plugin.icon, 1)
            else: image = gtk.image_new_from_icon_name(plugin.icon, 1)
            item.set_image(image)

        # Add shortcut.
        cfgname = 'plugin.%s' % plugin.name
        shortcuts = main.shortcuts.childs
        if shortcuts.has_key(cfgname):
            shortcut = shortcuts[cfgname]
            item.add_accelerator(
                'activate',
                self.accelgroup,
                int(shortcut.key, 16),
                shortcut.mask,
                gtk.ACCEL_VISIBLE)
