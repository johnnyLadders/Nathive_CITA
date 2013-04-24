#!/usr/bin/env python
#nathive C extension (dotcy spec 1)

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.buftools import bufindex


def pick(pixbuf, width, x, y, 'Piii:iii'):
    """Return the color at the given coordinates pixel in the given image.
    @pixbuf: Pixbuf memory address as int.
    @width: Pixbuf width in pixels.
    @x: X coordinate of wanted pixel.
    @y: Y coordinate of wanted pixel.
    =return: 3-item list with RGB values."""

    type l: index
    index = bufindex(x, y, width)

    type c: r, g, b
    r = pixbuf[index+0]
    g = pixbuf[index+1]
    b = pixbuf[index+2]

    return r, g, b
