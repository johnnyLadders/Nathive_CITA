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

from nathive.gui.sidebar_color import SidebarColor
from nathive.gui.sidebar_layers import SidebarLayers
from nathive.gui import utils as gutils
from nathive.gui.multiwidget import *


class Sidebar(object):
    """The main window sidebar."""

    def __init__(self, box):
        """Create the sidebar.
        @box: Parent widget."""

        # Create the notebook and add to parent.
        self.notebook = gtk.Notebook()
        box.pack_start(self.notebook, False, False, 0)

        # Get and set sidebar width.
        width = main.config.getint('sidebar','width')
        self.notebook.set_size_request(width, -1)

        # Append color properies to the sidebar notebook.
        self.color = SidebarColor()
        self.notebook.append_page(self.color.box, gtk.Label(_('Color')))

        # Append layers tree to the sidebar notebook.
        self.layers = SidebarLayers()
        self.notebook.append_page(self.layers.box, gtk.Label(_('Objects')))

        # Append tools properties to sidebar notebook.
        self.tool = gtk.VBox(False, 0)
        self.tool.set_border_width(10)
        self.toolgroup = MultiWidgetGroup(self.tool)
        activetool = main.plugins.activetool
        toolimg_path = os.path.join(main.imgpath, activetool.icon)
        toolimg = gtk.image_new_from_file(toolimg_path)
        self.notebook.append_page(self.tool, toolimg)

        # Display the above widgets (from now will be dynamically displayed).
        self.notebook.show_all()

        # Append tool GUIs to the tool notebook page.
        for name, plug in main.plugins.childs.items():
            if plug.type == 'tool':
                widget = plug.gui()
                gutils.expander(widget)
                MultiWidgetPresets(plug, widget, False)
                self.toolgroup.append(name, widget)

        # Display the properties of active tool (the first one).
        self.toolgroup.show(main.plugins.activetool.name)


    def toolchanged(self):
        """To do when the user select another tool."""

        # Get active tool.
        activetool = main.plugins.activetool

        # Set icon in sidebar tab.
        toolimg_path = os.path.join(main.imgpath, activetool.icon)
        toolimg = gtk.image_new_from_file(toolimg_path)
        self.notebook.set_tab_label(self.tool, toolimg)

        # Show tool group into sidebar tab.
        self.toolgroup.show(activetool.name)
