#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk

from nathive.gui import utils as gutils


class MultiWidgetEntry(object):

    def __init__(self, parent, label, maxchar, text, callback):

        self.box = gtk.HBox(False, 0)

        label = gtk.Label('%s:' % label)
        label.set_alignment(0, 0.5)

        self.entry = gtk.Entry(maxchar)
        self.entry.set_width_chars(maxchar + 1)
        self.entry.set_text(text)
        self.handler = self.entry.connect(
            'changed',
            lambda x: callback(x.get_text()))

        # Pack into box.
        self.box.pack_start(label, True, True, 0)
        gutils.margin(self.box, 20, 1)
        self.box.pack_start(self.entry, False, False, 0)

        # Pack into parent widget.
        parent.pack_start(self.box, False, False, 0)


    def set_value(self, value, propagate=False):

        if not propagate: self.entry.handler_block(self.handler)
        self.entry.set_text(value)
        if not propagate: self.entry.handler_unblock(self.handler)
