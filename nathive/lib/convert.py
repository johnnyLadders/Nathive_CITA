#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk
import re
import colorsys
import copy


def pixbuf_pointer(pixbuf):
    """Return the low-level memory address from a PyGTK pixbuf.
    @pixbuf: The Gtk.Gdk.Pixbuf."""

    pointer = pixbuf.get_properties('pixels')
    pointer = str(pointer[0])
    pointer = re.search("0x[0-9a-fA-F]+", pointer).group(0)
    pointer = int(pointer, 16)
    return pointer


def hex_rgb(hexcolor):

    r = hexcolor[0:2]
    g = hexcolor[2:4]
    b = hexcolor[4:6]
    rgb = [r, g, b]
    rgb = [int(x, 16) for x in rgb]
    return rgb


def rgb_hex(rgbcolor):

    rgb = '%2x%2x%2x' % (rgbcolor[0], rgbcolor[1], rgbcolor[2])
    rgb = rgb.replace(' ', '0')
    return rgb


def rgb_hsv(rgbcolor):

    rgb = copy.copy(rgbcolor)
    rgb = [float(x)/255 for x in rgbcolor]
    hsv = list(colorsys.rgb_to_hsv(*rgb))
    if hsv[0] == 1: hsv[0] = 0
    hsv[0] *= 360
    hsv[1] *= 100
    hsv[2] *= 100
    hsv = [int(x) for x in hsv]
    return hsv


def hsv_rgb(hsvcolor):

    hsv = copy.copy(hsvcolor)
    hsv[0] /= float(360)
    hsv[1] /= float(100)
    hsv[2] /= float(100)
    rgb = list(colorsys.hsv_to_rgb(*hsv))
    rgb = [int(x*255) for x in rgb]
    return rgb


def px_cm(px, dpi):

    return float(1) * px / dpi * 2.54


def cm_px(cm, dpi):

    return float(1) * cm * dpi / 2.54


def px_in(px, dpi):

    return float(1) * px / dpi


def in_px(inch, dpi):

    return float(1) * inch * dpi


def cm_in(cm, dpi):

    return float(1) * cm / 2.54


def in_cm(inch, dpi):

    return float(1) * inch * 2.54
