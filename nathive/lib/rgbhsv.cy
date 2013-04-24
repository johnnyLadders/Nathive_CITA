#!/usr/bin/env python
#nathive C extension (dotcy spec 1)

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


def __rgb_to_hsv(r, g, b, 'fff:F'):
    """Convert an RGB color to HSV, note the returned array must be freed.
    @r: Red value as 0 to 1 float.
    @g: Green value as 0 to 1 float.
    @b: Blue value as 0 to 1 float.
    =return: HSV values as float array from 0 to 1."""

    # Get the max value of the given.
    type f: maxval
    maxval = r
    if g > maxval: maxval = g
    if b > maxval: maxval = b

    # Get the min value of the given.
    type f: minval
    minval = r
    if g < minval: minval = g
    if b < minval: minval = b

    # Allocate return array in memory to preserve it outside this function.
    type F: hsv
    hsv = (F)malloc(sizeof(float) * 3)

    # Init intermediate variable.
    type f: m
    m = 0

    # Calculate hue value.
    hsv[0] = 0
    if maxval != minval:
        if maxval == r:
            m = (g - b) / (maxval - minval)
            hsv[0] = (60 * m) + 0
            if g < b: hsv[0] += 360
        if maxval == g:
            m = (b - r) / (maxval - minval)
            hsv[0] = (60 * m) + 120
        if maxval == b:
            m = (r - g) / (maxval - minval)
            hsv[0] = (60 * m) + 240
        hsv[0] /= 360

    # Calculate saturation value.
    if maxval > 0:
        hsv[1] = 1 - (minval / maxval)
    #else: hsv[1] = 0.0                     # Statement with no effect warning.

    # Calculate brightness value.
    hsv[2] = maxval

    # Return array.
    return hsv



def __hsv_to_rgb(h, s, v, 'fff:F'):
    """Convert an HSV color to RGB, note the returned array must be freed.
    @h: Hue value as 0 to 1 float.
    @s: Saturation value as 0 to 1 float.
    @v: Brightness value as 0 to 1 float.
    =return: RGB values as float array from 0 to 1."""

    # Convert value to degrees.
    h *= 360

    # Get degree remainder.
    type i: hi
    hi = fmod(h / 60, 6)

    # Calculate assignable variables.
    type f: n, p, q, t
    n = (h / 60.0) - hi
    p = v * (1 - s)
    q = v * (1 - (n * s))
    t = v * (1 - ((1 - n) * s))

    # Allocate return array in memory to preserve it outside this function.
    type F: rgb
    rgb = (F)malloc(sizeof(float) * 3)

    # Assign variables in relation to the remainder.
    if hi == 0:
        rgb[0] = v
        rgb[1] = t
        rgb[2] = p
    if hi == 1:
        rgb[0] = q
        rgb[1] = v
        rgb[2] = p
    if hi == 2:
        rgb[0] = p
        rgb[1] = v
        rgb[2] = t
    if hi == 3:
        rgb[0] = p
        rgb[1] = q
        rgb[2] = v
    if hi == 4:
        rgb[0] = t
        rgb[1] = p
        rgb[2] = v
    if hi == 5:
        rgb[0] = v
        rgb[1] = p
        rgb[2] = q

    # Return array.
    return rgb
