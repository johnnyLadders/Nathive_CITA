#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import pygtk
import gtk
import traceback

from nathive.gui.menubar import Menubar
from nathive.gui.headbar import Headbar
from nathive.gui.toolbar import Toolbar
from nathive.gui.tabs import Tabs
from nathive.gui.sidebar import Sidebar
from nathive.gui.colorbar import Colorbar
from nathive.gui.colorDictionary import ColorDictionary
from nathive.gui.statusbar import Statusbar
from nathive.gui.cursor import Cursor


class Main(object):
    """Manage graphical user interface, the event loop, and containing window
    and modular interface parts as other objects.
    ⌥: Main > Gui."""

    def interface(self):
        """Create and display the main window, init interface objects."""

        # Create the main window.
        gtkversion = '.'.join([str(x) for x in gtk.gtk_version])
        main.log.info('loading gtk interface (v%s)' % gtkversion)
        pygtk.require('2.0')
        self.window = gtk.Window()
        self.window.set_icon_from_file('%s/icon.png' % main.imgpath)
        self.window.set_title("Nathive %s %s" % (main.version, main.phase))
        self.window.set_position('center')
        self.window.connect('window-state-event', self.state_cb)
        self.window.connect('configure-event', self.state_cb)
        self.window.connect('destroy', lambda x: self.quit())

        # Window size.
        width = main.config.getint('window','width')
        height = main.config.getint('window','height')
        self.window.set_default_size(width, height)
        if main.config.getint('window', 'maximize'): self.window.maximize()

        # Add shortcuts to window.
        main.shortcuts.push()

        # Main window box.
        vbox = gtk.VBox(False, 0)
        vbox.show()

        # Top section.
        self.menubar = Menubar(vbox)
        self.headbar = Headbar(vbox)

        # Central section.
        hbox = gtk.HBox(False, 0)
        hbox.show()
        self.toolbar = Toolbar(hbox)
        self.tabs = Tabs(hbox)
        self.sidebar = Sidebar(hbox)
        self.colorbar = Colorbar(hbox)
        self.colorDictionary = ColorDictionary(hbox)
        vbox.pack_start(hbox, True, True, 0)

        # Bottom section.
        self.statusbar = Statusbar(vbox)

        # Cursor icons handler.
        self.cursor = Cursor()

        # Show main window
        self.window.add(vbox)
        self.window.show()
        self.window.set_focus(None)


    def state_cb(self, widget, event):
        """To do when the window size or state change.
        @widget: Root widget.
        @event: Emited event object."""

        # Get maximize state and set in config.
        maximized = int(main.gui.window.window.get_state())
        maximized = (maximized >> 2) % 2
        main.config.set('window', 'maximize', maximized)
        if maximized: return

        # Get window dimensions and set in config.
        width, height = main.gui.window.window.get_geometry()[2:4]
        main.config.set('window', 'width', width)
        main.config.set('window', 'height', height)


    def loop(self):
        """Loop over GTK GUI to hook events."""

        main.log.info('waiting for events')
        gtk.main()


    def quit(self):
        """Exit GUI iteration."""

        main.config.set('color', 'r', main.color.rgb[0])
        main.config.set('color', 'g', main.color.rgb[1])
        main.config.set('color', 'b', main.color.rgb[2])

        main.config.save()
        main.log.end()
        gtk.main_quit()
