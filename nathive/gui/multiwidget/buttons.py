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


class MultiWidgetButtons(object):
    """Display label and multiple toggle image buttons."""

    def __init__(self, parent, label, buttons):
        """Create and put on parent.
        @parent: Parent widget to put in.
        @label: Text to display.
        @buttons: """

        # Create main widget and add into parent.
        self.box = gtk.HBox(False, 0)
        parent.pack_start(self.box, False, False, 0)

        # Label.
        if label:
            label = gtk.Label('%s:' % label)
            label.set_alignment(0, 0.5)
            self.box.pack_start(label, True, True, 0)

        # Margin between label and buttons.
        gutils.margin(self.box, 20, 1)

        # Buttons.
        for properties in reversed(buttons):
            icon, tooltip, callback = properties
            button = gtk.Button()
            button.set_image(gtk.image_new_from_icon_name(icon, 1))
            button.set_relief(gtk.RELIEF_NONE)
            button.set_tooltip_text(tooltip)
            button.connect('clicked', lambda x,y=callback: y())
            self.box.pack_end(button, False)
