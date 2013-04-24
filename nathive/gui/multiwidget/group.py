#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk


class MultiWidgetGroup(object):
    """A simplest way to group, show and hide widgets."""

    def __init__(self, parent):

        self.contents = {}
        self.box = gtk.VBox(False, 0)
        parent.pack_start(self.box, True, True, 0)


    def append(self, name, widget):

        self.contents[name] = widget
        self.box.pack_start(widget, True, True, 0)


    def hide_all(self):

        for widget in self.contents.values():
            widget.hide()


    def show(self, name):

        self.hide_all()
        self.contents[name].show_all()
