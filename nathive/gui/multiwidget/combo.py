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


class MultiWidgetCombo(object):

    def __init__(self, parent, label, options, selected, callback):

        # Create main widget and add into parent.
        self.box = gtk.HBox(False, 0)
        parent.pack_start(self.box, False, False, 0)

        # Label.
        label = gtk.Label('%s:' % label)
        label.set_alignment(0, 0.5)
        self.box.pack_start(label, True, True, 0)

        # Margin between label and combo.
        gutils.margin(self.box, 20, 1)

        # Combo box.
        self.combo = gtk.combo_box_new_text()
        for option in options: self.combo.append_text(option)
        self.combo.set_active(selected)
        self.combo.connect('changed', lambda x: callback(x.get_active()))
        self.box.pack_start(self.combo, False)


    def set_value(self, value):

        self.combo.set_active(value)


    def get_value(self):

        return self.combo.get_active()


    def connect_extra(self, callback):

        self.combo.connect('changed', lambda x: callback())
