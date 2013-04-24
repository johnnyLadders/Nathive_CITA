#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk


class Cursor(object):

    def __init__(self):

        self.default = 'cursor'
        self.current = 'cursor'


    def set_default(self):

        self.set_from_name(self.default)


    def set_from_name(self, name):

        if self.current == name: return

        names = {
            'cursor' : gtk.gdk.ARROW,
            'cursor-restricted' : gtk.gdk.CIRCLE,
            'busy' : gtk.gdk.WATCH,
            'hand-open' : gtk.gdk.HAND1,
            'hand-closed' : gtk.gdk.FLEUR,
            'hand-pointing' : gtk.gdk.HAND2,
            'corner-top-left' : gtk.gdk.TOP_LEFT_CORNER,
            'corner-top-right' : gtk.gdk.TOP_RIGHT_CORNER,
            'corner-bottom-left' : gtk.gdk.BOTTOM_LEFT_CORNER,
            'corner-bottom-right' : gtk.gdk.BOTTOM_RIGHT_CORNER,
            'side-left' : gtk.gdk.LEFT_SIDE,
            'side-right' : gtk.gdk.RIGHT_SIDE,
            'side-top' : gtk.gdk.TOP_SIDE,
            'side-bottom' : gtk.gdk.BOTTOM_SIDE,
            'arrow-left' : gtk.gdk.SB_LEFT_ARROW,
            'arrow-right' : gtk.gdk.SB_RIGHT_ARROW,
            'arrow-up' : gtk.gdk.SB_UP_ARROW,
            'arrow-down' : gtk.gdk.SB_DOWN_ARROW,
            'arrow-double-vertical' : gtk.gdk.SB_V_DOUBLE_ARROW,
            'arrow-double-horizontal' : gtk.gdk.SB_H_DOUBLE_ARROW,
            'arrow-question' : gtk.gdk.QUESTION_ARROW,
            'font-cursor' : gtk.gdk.XTERM,
            'x-cursor' : gtk.gdk.X_CURSOR,
            'cross' : gtk.gdk.CROSS,
            'plus' : gtk.gdk.PLUS,
            'pencil' : gtk.gdk.PENCIL}

        gdkname = names[name]
        cursor = gtk.gdk.Cursor(gdkname)
        main.gui.window.window.set_cursor(cursor)
        self.current = name
