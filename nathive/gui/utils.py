#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk


def margin(parent, width, height=0):
    """Put an invisible separator between two widgets.
    @parent: The parent widget.
    @size: Separator width or height."""

    if not height: height = width

    box = gtk.HBox(False, 0)
    box.set_size_request(width, height)
    parent.pack_start(box, False, False, 0)


def separator(parent):
    """Put a horizontal separator between two widgets.
    @parent: The parent widget."""

    separator =  gtk.HSeparator()
    parent.pack_start(separator, False, False, 4)


def expander(parent):

    box = gtk.HBox(False, 0)
    parent.pack_start(box, True, True, 0)
