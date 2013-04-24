#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import re

from nathive.lib import convert


class Color(object):
    """Store and handle foreground color and fill pattern.
    ⌥: Main > Color."""

    def __init__(self):
        """Create the color management object at program start."""

        main.log.info('loading color management')

        # Color values in several formats, rgb is the lead one.
        self.rgb = [0, 0, 0]
        self.rgb[0] = main.config.getint('color', 'r')
        self.rgb[1] = main.config.getint('color', 'g')
        self.rgb[2] = main.config.getint('color', 'b')
        self.hsv = convert.rgb_hsv(self.rgb)
        self.hex = convert.rgb_hex(self.rgb)

        # List of functions to call when color is updated.
        self.updated_todo = []


    def set_color_from_rgb(self, rgb):
        """Set the foreground color from rgb values.
        @rgb: Python 3-item list with values from 0 to 255."""

        self.rgb = rgb
        self.hsv = convert.rgb_hsv(rgb)
        self.hex = convert.rgb_hex(rgb)
        self.update_external()


    def set_color_from_hsv(self, hsv):
        """Set the foreground color from hsv values.
        @hsv: Python 3-item list with values from 0 to 255."""

        self.hsv = hsv
        self.rgb = convert.hsv_rgb(hsv)
        self.hex = convert.rgb_hex(self.rgb)
        self.update_external()


    def set_color_from_hex(self, hexa):
        """Set the foreground color from an hexadecimal string.
        @hexa: A string of six chars defining a color in hexadecimal format."""

        self.hex = hexa
        self.rgb = convert.hex_rgb(hexa)
        self.hsv = convert.rgb_hsv(self.rgb)
        self.update_external()


    def set_rgb_component(self, value, index):
        """Compose a new rgb color by changing one of its component, then set
        the foreground color with the new rgb values.
        @value: The new component value as int from 0 to 255.
        @index: The component to change as int from 0(red) to 2(blue)."""

        rgb = self.rgb
        rgb[index] = int(value)
        self.set_color_from_rgb(rgb)


    def set_hsv_component(self, value, index):
        """Compose a new hsv color by changing one of its component, then set
        the foreground color with the new hsv values.
        @value: The new component value as int.
        @index: The component to change as int from 0(hue) to 2(value)."""

        hsv = self.hsv
        hsv[index] = int(value)
        self.set_color_from_hsv(hsv)


    def set_hex(self, hexa):
        """Evaluate an hexadecimal string and set the foreground color.
        @hexa: A valid hexadecimal string of six chars."""

        if not re.search("^[0-9a-fA-F]{6}$", hexa): return
        self.hex = hexa
        rgb = convert.hex_rgb(hexa)
        self.set_color_from_hex(hexa)


    def update_external(self):
        """Call every function in the todo stack."""

        for func in self.updated_todo: func()


    def clear(self):
        """Restore the color to defaults, just black."""

        self.set_color_from_rgb([0, 0, 0])
