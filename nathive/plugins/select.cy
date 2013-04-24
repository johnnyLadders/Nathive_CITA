#!/usr/bin/env python
#nathive C extension (dotcy spec 1)

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.buftools import bufindex


def get_pixel_alpha(pixbuf, width, x, y, 'Piii:i'):

    type l: index
    index = bufindex(x, y, width)
    return pixbuf[index+3]
