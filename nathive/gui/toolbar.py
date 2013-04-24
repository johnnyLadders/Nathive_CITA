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

from nathive.lib import convert
from nathive.gui import utils as gutils


class Toolbar(object):
    """Define toolbar instance."""

    def __init__(self, parent):
        """Create toolbar and buttons.
        @parent: Parent widget."""

        # Create toolbar.
        self.box = gtk.VBox(False, 0)
        self.box.set_border_width(2)
        self.group = None

        # Add into parent widget and show.
        parent.pack_start(self.box, False, False, 0)
        self.dump(True)

        main.color.updated_todo.append(self.colorbox_update)


    def dump(self, addlost=False):
        """Filter sort list, dump to toolbar, and push to config."""

        # Alias.
        plugins = main.plugins.childs

        # Remove previous stuff.
        self.box.foreach(gtk.Widget.destroy)
        self.group = None

        # Get sort list from config.
        self.sort = main.config.get('sort', 'toolbar').split(',')

        # Add lost tools.
        if addlost:
            for (toolname, tool) in main.plugins.childs.items():
                if toolname not in self.sort:
                    if main.plugins.childs[toolname].type == 'tool':
                        self.sort.append(toolname)

        # Remove non-plugin from sort list.
        self.sort = [x for x in self.sort if plugins.has_key(x)]

        # Remove non-tool plugins from sort list.
        self.sort = [x for x in self.sort if plugins[x].type == 'tool']

        # Dump each item to toolbar.
        for toolname in self.sort:
            self.item(toolname)

        # Margin between buttons and colorboxes.
        gutils.margin(self.box, 5)

        # Colorboxes.
        self.colorwidget = gtk.HBox(True, 0)
        self.colorframe = gtk.Frame()
        self.colorbox = gtk.EventBox()
        self.colorbox.set_size_request(20, 20)
        self.colorframe.add(self.colorbox)
        self.colorwidget.pack_start(self.colorframe, False, False, 0)
        self.box.pack_start(self.colorwidget, False, False, 0)
        self.colorbox_update()

        # Show all.
        self.box.show_all()

        # Push sort to config.
        main.config.set('sort', 'toolbar', ','.join(self.sort))


    def item(self, toolname):
        """Append toolbar buttons.
        @toolname: Tool name to include in toolbar."""

        button = gtk.RadioButton(self.group, None, False)
        if not self.group: self.group = button
        plugin = main.plugins.get_plugin(toolname)
        imagepath = os.path.join(main.imgpath, plugin.icon)
        button.set_image(gtk.image_new_from_file(imagepath))
        button.set_relief(gtk.RELIEF_NONE)
        button.set_mode(False)
        self.box.pack_start(button, False, False, 0)

        button.connect('toggled', lambda x: self.toggled(toolname))
        button.connect('button-press-event', self.press)


    def toggled(self, toolname):
        """Callback function when some toolbar icon is selected.
        @toolname: Asociated tool name to activate."""

        main.plugins.set_active_tool(toolname)
        main.gui.sidebar.toolchanged()


    def press(self, widget, event):
        """Callback function that catch double-clicks in any button to show the
        tool propierties tab in the sidebar.
        @widget: Call widget.
        @event: Event data instance."""

        if event.type == gtk.gdk._2BUTTON_PRESS:
            main.gui.sidebar.notebook.set_current_page(2)


    def colorbox_update(self):
        """Updates colorbox color when is outdated."""

        rgbcolor = main.color.rgb
        hexcolor = convert.rgb_hex(rgbcolor)
        gtkcolor = gtk.gdk.Color('#' + hexcolor)
        self.colorbox.modify_bg(gtk.STATE_NORMAL, gtkcolor)
