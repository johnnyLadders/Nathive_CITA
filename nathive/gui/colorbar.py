#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk

from nathive.lib import convert


class Colorbar(object):
    """Define colorbar instance."""

    def __init__(self, parent):
        """Create the colorbar."""

        # Colorbar properties.
        self.vbox = gtk.VBox(False, 0)
        self.vbox.set_size_request(30, False)
        self.vbox.set_border_width(5)

        # Get palette.
        self.palette = self.getpalette()

        # Put colors in palette.
        for color in self.palette:
            self.item(color)

        # Pack colorbar into parent widget and show.
        parent.pack_start(self.vbox, False, False, 0)
        self.vbox.show_all()


    def getpalette(self):
        """Get palette from file, return Python list."""

        palette = open('%s/default.pal' % main.palpath).readlines()
        palette = [x.rstrip() for x in palette]
        return palette


    def item(self, hexcolor):
        """Put a color in the colorbar.
        @hexcolor: hexadecimal color like 57ABFF."""

        eventbox = gtk.EventBox()
        eventbox.set_size_request(20, False)
        color = gtk.gdk.color_parse('#' + hexcolor)
        eventbox.modify_bg(gtk.STATE_NORMAL, color)
        eventbox.connect('button-press-event', self.clicked, hexcolor)
        self.vbox.pack_start(eventbox, True, True, 0)


    def clicked(self, widget, event, hexcolor):
        """Callback for each color.
        @widget: Callback gtkwidget.
        @event: Callback gtkevent.
        @hexcolor: hexadecimal color like 57ABFF."""

        rgbcolor = convert.hex_rgb(hexcolor)
        main.color.set_color_from_rgb(rgbcolor)
