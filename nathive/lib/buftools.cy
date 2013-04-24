#!/usr/bin/env python
#nathive C extension (dotcy spec 1)

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


def __bufindex(x, y, width, 'iii:l'):
    """Calculate index for the given coordinates and width of a pixel buffer.
    @x: Coordinate in x axis.
    @y Coordinate in y axis.
    @width: Image width as pixels.
    =return: Index for the first pixel channel."""

    return ((y * width) + x) << 2
