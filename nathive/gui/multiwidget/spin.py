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


class MultiWidgetSpin(object):

    def __init__(self, parent, label, scale, minval, maxval, value, callback):

        self.box = gtk.HBox(False, 0)

        self.label = gtk.Label('%s:' % label)
        self.label.set_alignment(0, 0.5)

        self.adjustment = gtk.Adjustment(value, minval, maxval, 1, 1, 0)

        if scale:
            self.scale = gtk.ScaleButton(1, minval, maxval, 1, ['gtk-index'])
            self.scale.set_adjustment(self.adjustment)

        self.spin = gtk.SpinButton(self.adjustment, 0, 0)
        self.handler = self.adjustment.connect(
            'value-changed',
            lambda x: callback(x.get_value()))

        # Pack into box.
        self.box.pack_start(self.label, True, True, 0)
        gutils.margin(self.box, 20, 1)
        if scale: self.box.pack_start(self.scale, False, False, 0)
        self.box.pack_start(self.spin, False, False, 0)

        # Pack into parent widget.
        parent.pack_start(self.box, False, False, 0)


    def get_value(self):

        value = self.adjustment.get_value()
        if not value % 1: return int(value)
        return value


    def set_value(self, value, propagate=False):

        if not propagate: self.adjustment.handler_block(self.handler)
        self.adjustment.set_value(value)
        if not propagate: self.adjustment.handler_unblock(self.handler)


    def connect_extra(self, callback):

        self.adjustment.connect('value-changed', lambda x: callback())
