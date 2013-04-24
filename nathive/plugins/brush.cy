#!/usr/bin/env python
#nathive C extension (dotcy spec 1)

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.buftools import bufindex


def __softer(radio, dist, opacity, soft, 'ddii:c'):
    """Return a smoothing value for given position in the brush.
    @radio: Brush radio (half of size).
    @dist: Distance away from brush center in requested pixel to soft.
    @opacity: Brush opacity value (0-100).
    @soft: Brush smoothing value (0-100).
    =return: Smoothing value for requested pixel in scale 0-255."""

    # Some convertions.
    type d: soft_double, opacity_value, soft_start
    soft_double = (d)soft
    opacity_value = 255 * (d)opacity / 100
    soft_start = radio / 100 * (100-soft_double)

    # Go out if pixel doesn't need smoothing.
    if dist <= soft_start: return (c)opacity_value
    if dist > radio: return 0

    # Convert values to 0-1 scale.
    type d: soft_len, dist_prescale, dist_scale
    soft_len = radio - soft_start
    dist_prescale = dist - soft_start
    dist_scale = dist_prescale / soft_len

    # Apply y=x^3 in 0-1 scope.
    type d: value_scale
    if dist_scale < 0.5: value_scale = -(pow(dist_scale*2,3)/2)+1
    else: value_scale = fabs(pow((dist_scale-1)*2,3)/2)

    # Re-scale and return.
    type d: value
    value = value_scale * opacity_value
    return (c)value

def getSoftness(radio, dist, opacity, soft, 'ddii:c'):
    """Return a smoothing value for given position in the brush.
    @radio: Brush radio (half of size).
    @dist: Distance away from brush center in requested pixel to soft.
    @opacity: Brush opacity value (0-100).
    @soft: Brush smoothing value (0-100).
    =return: Smoothing value for requested pixel in scale 0-255."""

    # Some convertions.
    type d: soft_double, opacity_value, soft_start
    soft_double = (d)soft
    opacity_value = 255 * (d)opacity / 100
    soft_start = radio / 100 * (100-soft_double)

    # Go out if pixel doesn't need smoothing.
    if dist <= soft_start: return (c)opacity_value
    if dist > radio: return 0

    # Convert values to 0-1 scale.
    type d: soft_len, dist_prescale, dist_scale
    soft_len = radio - soft_start
    dist_prescale = dist - soft_start
    dist_scale = dist_prescale / soft_len

    # Apply y=x^3 in 0-1 scope.
    type d: value_scale
    if dist_scale < 0.5: value_scale = -(pow(dist_scale*2,3)/2)+1
    else: value_scale = fabs(pow((dist_scale-1)*2,3)/2)

    # Re-scale and return.
    type d: value
    value = value_scale * opacity_value
    return (d)value

def new(brush, recalc, shape, size, opacity, soft, r, g, b, 'Piiiiiiii:'):
    """Create a new brush in the given layer.
    @brush: Brush memory address as long int.
    @recalc: Boolean int to define if brush opacity is outdated.
    @shape: Brush shape mode as int.
    @size: Brush size pixels.
    @opacity: Brush opacity as int (0-100).
    @r: Red part of brush color as int (0-255).
    @g: Green part of brush color as int (0-255).
    @b: Blue part of brush color as int (0-255)."""

    # Set the radio distance.
    type d: radio
    radio = (d)size / 2

    # Loop over brush buffer to create new brush.
    type i: pos, x, y
    type d: dist, dist_x, dist_y
    for y in range(size):
        for x in range(size):

            pos = bufindex(x, y, size)
            brush[pos+0] = r
            brush[pos+1] = g
            brush[pos+2] = b

            if not recalc: continue

            dist_x = (d)x - radio + 0.5
            dist_y = (d)y - radio + 0.5

            # Square shape.
            if shape == 0:
                if abs(dist_x) > abs(dist_y): dist = abs(dist_x)
                else: dist = abs(dist_y)
                brush[pos+3] = softer(radio, dist, opacity, soft)

            # Circle shape.
            if shape == 1:
                dist = sqrt( (dist_x*dist_x) + (dist_y*dist_y) )
                brush[pos+3] = softer(radio, dist, opacity, soft)
