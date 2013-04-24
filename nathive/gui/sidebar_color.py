#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk

from nathive.gui.multiwidget import *
from nathive.gui import utils as gutils


class SidebarColor(object):
    """Class to display and manage the sidebar color tab.
    ⌥: Main > Gui > Sidebar > SidebarColor."""

    def __init__(self):
        """Create the sidebar color object at program start, including the
        interface controllers."""

        # Configure box.
        self.box = gtk.VBox(False, 0)
        self.box.set_border_width(10)

        # Append callback to color update stack.
        main.color.updated_todo.append(self.update)

        # Red controller.
        self.color_r = MultiWidgetSpin(
            self.box,
            _('Red') + ' (R)',
            True,
            0,
            255,
            main.color.rgb[0],
            lambda x: main.color.set_rgb_component(x, 0))

        # Green controller.
        self.color_g = MultiWidgetSpin(
            self.box,
            _('Green') + ' (G)',
            True,
            0,
            255,
            main.color.rgb[1],
            lambda x: main.color.set_rgb_component(x, 1))

        # Blue controller.
        self.color_b = MultiWidgetSpin(
            self.box,
            _('Blue') + ' (B)',
            True,
            0,
            255,
            main.color.rgb[2],
            lambda x: main.color.set_rgb_component(x, 2))

        # Separator between rgb and hsv.
        gutils.separator(self.box)

        # Hue controller.
        self.color_h = MultiWidgetSpin(
            self.box,
            _('Hue') + ' (H)',
            True,
            0,
            359,
            main.color.hsv[0],
            lambda x: main.color.set_hsv_component(x, 0))

        # Saturation controller.
        self.color_s = MultiWidgetSpin(
            self.box,
            _('Saturation') + ' (S)',
            True,
            0,
            100,
            main.color.hsv[1],
            lambda x: main.color.set_hsv_component(x, 1))

        # Value controller.
        self.color_v = MultiWidgetSpin(
            self.box,
            _('Value') + ' (V)',
            True,
            0,
            100,
            main.color.hsv[2],
            lambda x: main.color.set_hsv_component(x, 2))

        # Separator between hsv and hexadecimal.
        gutils.separator(self.box)

        self.color_hex = MultiWidgetEntry(
            self.box,
            _('Hexadecimal'),
            6,
            main.color.hex,
            main.color.set_hex)

        # Gap to the box bottom.
        gutils.expander(self.box)
        gutils.separator(self.box)

        # Clear button.
        self.clear = MultiWidgetClear(
            self.box,
            1,
            main.color.clear)


    def update(self):
        """Update the user interface controllers of the sidebar color tab."""

        # Update rgb controllers.
        self.color_r.set_value(main.color.rgb[0])
        self.color_g.set_value(main.color.rgb[1])
        self.color_b.set_value(main.color.rgb[2])

        # Update hsv controllers.
        self.color_h.set_value(main.color.hsv[0])
        self.color_s.set_value(main.color.hsv[1])
        self.color_v.set_value(main.color.hsv[2])

        # Update hex controllers.
        self.color_hex.set_value(main.color.hex)
