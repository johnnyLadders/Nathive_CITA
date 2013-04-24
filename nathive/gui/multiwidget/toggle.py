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


class MultiWidgetToggle(object):
    """Display label and multiple toggle image buttons."""

    def __init__(self, parent, label, options, selected, callback):
        """Create and put on parent.
        @parent: Parent widget to put in.
        @label: Text to display.
        @option: Variable-length list with image names as strings.
        @selected: Index int to choose selected toggled button.
        @callback: Callback function to pass index int when toogled."""

        # Create main widget and add into parent.
        self.box = gtk.HBox(False, 0)
        parent.pack_start(self.box, False, False, 0)

        # Label.
        label = gtk.Label('%s:' % label)
        label.set_alignment(0, 0.5)
        self.box.pack_start(label, True, True, 0)

        # Margin between label and buttons.
        gutils.margin(self.box, 20, 1)

        # Toggle buttons.
        self.buttons = []
        self.group = None
        for option in options:
            button = gtk.RadioButton(self.group, None, False)
            if not self.group: self.group = button
            imagepath = '%s/%s.png' % (main.imgpath, option)
            button.set_image(gtk.image_new_from_file(imagepath))
            button.set_relief(gtk.RELIEF_NONE)
            button.set_mode(False)
            self.buttons.append(button)
            button.connect('pressed', lambda x: callback(self.buttons.index(x)))
            self.box.pack_start(button, False, False, 0)

        # Set default toggled button.
        self.buttons[selected].set_active(True)


    def set_value(self, value):

        self.buttons[value].set_active(True)
