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
from nathive.gui.multiwidget import *
from nathive.gui import utils as gutils


class PresetManager(PluginDialog):
    """A dialog to manage plugin presets."""

    def __init__(self):

        # Subclass it.
        PluginDialog.__init__(self)

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Common attributes.
        self.name = 'preset-manager'
        self.author = 'nathive-dev'
        self.menu = 'edit'
        self.label = _('Preset manager')
        self.icon = 'gtk-properties'


    def callback(self, plugin_name=False, save=False):
        """To do when the plugin is called."""

        # Create dialog.
        self.dialog = gtk.Dialog(self.label)
        self.dialog.set_modal(True)
        self.dialog.set_resizable(False)
        self.dialog.set_size_request(250, 300)
        self.box = gtk.VBox(False, 5)
        self.box.set_border_width(5)
        self.dialog.vbox.pack_start(self.box)

        # Get plugin folders and names from cfg folders.
        self.plugin_paths = main.presets.get_plugin_paths()
        self.plugin_names = main.presets.get_plugin_names()

        # Set active plugin if given.
        if plugin_name in self.plugin_names:
            active = self.plugin_names.index(plugin_name)
        else:
            active = 0

        # Plugin selector.
        self.gui_plugin = MultiWidgetCombo(
            self.box,
            _('Plugin'),
            [x.capitalize() for x in self.plugin_names],
            active,
            lambda x: self.dump())

        # Presets list as treeview.
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.store = gtk.ListStore(str)
        self.treeview = gtk.TreeView(self.store)
        self.treeview.set_headers_visible(False)
        self.renderer = gtk.CellRendererText()
        self.renderer.set_property('editable', True)
        self.renderer.connect('edited', lambda x,y,z: self.edited(y, z))
        self.column = gtk.TreeViewColumn(None, self.renderer, text=0)
        self.treeview.append_column(self.column)
        scroll.add_with_viewport(self.treeview)
        self.box.pack_start(scroll, True, True)

        # Buttons to handle presets.
        button1 = (
            'gtk-remove',
            'Remove the selected preset',
            self.remove)
        button2 = (
            'gtk-add',
            'Create a new preset with the current plugin values',
            self.save)
        MultiWidgetButtons(
            self.box,
            False,
            (button1, button2))

        # Connect.
        self.dialog.connect('response', self.response)
        self.dialog.connect('destroy', lambda x: self.quit())

        # Buttons (auto-connected by response).
        self.dialog.add_button('gtk-close', 1)

        # Show.
        self.dump()
        self.dialog.show_all()

        if save: self.save()


    def dump(self, preset_name=False, edit=False):

        plugin_index = self.get_plugin_index()

        folder = self.plugin_paths[plugin_index]
        self.preset_tails = os.listdir(folder)
        self.preset_tails.sort()

        # Reset the tree store list.
        self.store = gtk.ListStore(str)
        self.treeview.set_model(self.store)

        # Dump tail names to treeview, store iters.
        self.iters = []
        for tail in self.preset_tails:
            name, ext = os.path.splitext(tail)
            rowiter = self.store.append([name])
            self.iters.append(rowiter)

        # Select first item.
        if self.iters:
            selection = self.treeview.get_selection()
            selection.select_iter(self.iters[0])

        # Select some preset if name is given, edit if edit flag is given.
        if preset_name:
            preset_names = [os.path.splitext(x)[0] for x in self.preset_tails]
            preset_index = preset_names.index(preset_name)
            selection.select_iter(self.iters[preset_index])
            if edit:
                self.treeview.set_cursor(preset_index, self.column, True)


    def get_plugin_index(self):

        return self.gui_plugin.get_value()


    def get_preset_index(self):

        selection = self.treeview.get_selection()
        treeview, path = selection.get_selected_rows()
        if not path: return None
        return path[0][0]


    def remove(self):

        if not self.iters: return
        folder = self.plugin_paths[self.get_plugin_index()]
        tail = self.preset_tails[self.get_preset_index()]
        path = os.path.join(folder, tail)
        os.remove(path)
        self.dump()


    def edited(self, preset_index, newtext):

        # Convert index to integer.
        preset_index = int(preset_index)

        # Get plugin name.
        plugin_index = self.get_plugin_index()
        plugin_name = self.plugin_names[plugin_index]

        # Get preset name.
        preset_tail = self.preset_tails[preset_index]
        preset_name, ext = os.path.splitext(preset_tail)

        # Rename preset and refresh gui.
        main.presets.rename_preset(plugin_name, preset_name, newtext)
        self.dump(newtext)


    def save(self):

        # Get plugin name.
        plugin_index = self.get_plugin_index()
        plugin_name = self.plugin_names[plugin_index]

        # Save plugin state and refresh gui.
        main.presets.save_preset(plugin_name)
        self.dump(' ', True)


    def response(self, widget, response):
        """Response (buttons) callbacks.
        @widget: Call widget.
        @response: Response int."""

        if response == 1: self.quit()


    def quit(self):
        """To do when the dialog is closed."""

        self.dialog.hide()
        self.dialog.destroy()
