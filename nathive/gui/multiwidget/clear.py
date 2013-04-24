#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk


class MultiWidgetClear(object):

    def __init__(self, parent, size, callback):

        self.box = gtk.HBox(False, 0)
        parent.pack_start(self.box, False, False, 0)

        button = gtk.Button(None, None, False)
        icon = gtk.image_new_from_stock('gtk-clear', size)
        button.set_image(icon)
        button.set_relief(gtk.RELIEF_NONE)
        button.connect('clicked', lambda x: callback())
        button.set_tooltip_text(_('Restore default values'))
        self.box.pack_end(button, False, False, 0)
