#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import gtk
import ConfigParser

from nathive.gui import utils as gutils


class MultiWidgetPresets(object):

    def __init__(self, plugin, parent, expander=True, onlyclear=False):

        # Alias.
        self.plugin = plugin

        # Force to make dir if not exists.
        main.presets.get_plugin_path(plugin.name)

        # Interface display.
        self.box = gtk.HBox()
        if expander:
            self.expander = gtk.Expander(_('Presets'))
            self.expander.add(self.box)
            gutils.separator(parent)
            parent.pack_start(self.expander, False)
        else:
            gutils.separator(parent)
            parent.pack_start(self.box, False)

        # Restore defaults button.
        default = gtk.Button()
        default.set_image(gtk.image_new_from_icon_name('gtk-clear', 1))
        default.set_relief(gtk.RELIEF_NONE)
        default.set_tooltip_text(_('Restore default values'))
        default.connect('clicked', lambda x: self.load_default())
        self.box.pack_end(default, False)

        if onlyclear: return

        # Manage presets button.
        manage = gtk.Button()
        manage.set_image(gtk.image_new_from_icon_name('gtk-edit', 1))
        manage.set_relief(gtk.RELIEF_NONE)
        manage.set_tooltip_text(_('Manage presets'))
        manager = main.plugins.childs['preset-manager']
        manage.connect('clicked',lambda x: manager.callback(plugin.name))
        self.box.pack_end(manage, False)

        # Save preset button.
        save = gtk.Button()
        save.set_image(gtk.image_new_from_icon_name('gtk-save', 1))
        save.set_relief(gtk.RELIEF_NONE)
        save.set_tooltip_text(_('Save the current values as a new preset'))
        save.connect('clicked', lambda x: self.save())
        self.box.pack_end(save, False)

        # Available presets menu-button.
        load = gtk.Button()
        load.set_image(gtk.image_new_from_icon_name('gtk-index', 1))
        load.set_relief(gtk.RELIEF_NONE)
        load.set_tooltip_text(_('Show available presets'))
        self.box.pack_end(load, False)
        load.connect(
            'clicked',
            lambda x: self.popup())


    def popup(self):

        self.update_presets()
        self.menu.popup(None, None, None, 1, 0)


    def update_presets(self):

        # Define presets folder and get preset names.
        folder = main.presets.get_plugin_path(self.plugin.name)
        preset_names = main.presets.get_preset_names(self.plugin.name)


        self.presets = main.presets.get_preset_parsers(self.plugin.name)
        self.menu = gtk.Menu()

        # Append presets to dropdown menu.
        for name in preset_names:
            menuitem = gtk.MenuItem(name, False)
            index = preset_names.index(name)
            menuitem.connect('activate', lambda x, y=index: self.load(y))
            menuitem.show()
            self.menu.append(menuitem)


    def load(self, index):

        # Get preset items.
        preset = self.presets[index]
        items = preset.items('preset')

        # Iter preset items.
        for key, value in items:

            # Convert from string to number.
            try: value = int(value)
            except:
                try: value = float(value)
                except: pass

            # Set plugin value.
            if hasattr(self.plugin, key): setattr(self.plugin, key, value)

        # Call plugin update function.
        self.plugin.update()


    def save(self):

        manager = main.plugins.childs['preset-manager']
        manager.callback(self.plugin.name, True)


    def load_default(self):

        self.plugin.default()
        if hasattr(self.plugin, 'update'): self.plugin.update()
