#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk
import zlib
import copy

from nathive.lib import convert
from nathive.libc import core


class ActionLayerContent(object):

    def __init__(self, layer):

        # Allow debug tracking.
        main.log.allow_tracking(self)

        self.layer = layer
        self.pixbuf = self.layer.pixbuf.copy()


    def final(self, zone=None):

        # If not zone given, zone is the entire layer.
        if not zone: zone = [0, 0, self.layer.width, self.layer.height]

        # Adjust zone to layer limits.
        if zone[0] < 0:
            zone[2] += zone[0]
            zone[0] = 0
        if zone[1] < 0:
            zone[3] += zone[1]
            zone[1] = 0
        zone[2] = min(zone[2], self.layer.width - zone[0])
        zone[3] = min(zone[3], self.layer.height - zone[1])
        self.zone = zone

        # Get original and modified subpixbufs.
        pixbuf = self.copy_area(self.pixbuf)
        pixbufmod = self.copy_area(self.layer.pixbuf)

        # Calc diff subpixbuf.
        core.diff(
            convert.pixbuf_pointer(pixbuf),
            convert.pixbuf_pointer(pixbufmod),
            zone[2],
            zone[3],
            False)

        # Compress diff subpixbuf.
        self.diff = zlib.compress(pixbuf.get_pixels())

        # Set propierties.
        self.rowstride = pixbuf.get_rowstride()
        self.bytes = len(self.diff)

        # Free memory.
        del(pixbuf)
        del(pixbufmod)
        del(self.pixbuf)


    def restore(self):

        # Set the target layer as active.
        main.documents.active.layers.set_active(self.layer, False)
        main.gui.sidebar.layers.dump()

        # Get diff and modified subpixbufs.
        diffbuf = self.decompress(self.diff)
        pixbuf = self.copy_area(self.layer.pixbuf)

        # Calc original subpixbuf.
        core.diff(
            convert.pixbuf_pointer(pixbuf),
            convert.pixbuf_pointer(diffbuf),
            self.zone[2],
            self.zone[3],
            True)

        # Copy original subpixbuf to layer.
        pixbuf.copy_area(
            0,
            0,
            self.zone[2],
            self.zone[3],
            self.layer.pixbuf,
            self.zone[0],
            self.zone[1])

        # Redraw zone (at document offset level).
        zone = copy.copy(self.zone)
        zone[0] += self.layer.xpos
        zone[1] += self.layer.ypos
        main.documents.active.canvas.redraw(*zone)


    def unrestore(self):

        # Set the target layer as active.
        main.documents.active.layers.set_active(self.layer, False)
        main.gui.sidebar.layers.dump()

        # Get diff and original subpixbufs.
        diffbuf = self.decompress(self.diff)
        pixbuf = self.copy_area(self.layer.pixbuf)

        # Calc modified subpixbuf.
        core.diff(
            convert.pixbuf_pointer(pixbuf),
            convert.pixbuf_pointer(diffbuf),
            self.zone[2],
            self.zone[3],
            False)

        # Copy modified subpixbuf to layer.
        pixbuf.copy_area(
            0,
            0,
            self.zone[2],
            self.zone[3],
            self.layer.pixbuf,
            self.zone[0],
            self.zone[1])

        # Redraw zone (at document offset level).
        zone = copy.copy(self.zone)
        zone[0] += self.layer.xpos
        zone[1] += self.layer.ypos
        main.documents.active.canvas.redraw(*zone)


    def decompress(self, data):

        return gtk.gdk.pixbuf_new_from_data(
            zlib.decompress(data),
            gtk.gdk.COLORSPACE_RGB,
            True,
            8,
            self.zone[2],
            self.zone[3],
            self.rowstride)


    def copy_area(self, pixbuf):

        newpixbuf = gtk.gdk.Pixbuf(
            gtk.gdk.COLORSPACE_RGB,
            True,
            8,
            self.zone[2],
            self.zone[3])

        pixbuf.copy_area(
            self.zone[0],
            self.zone[1],
            self.zone[2],
            self.zone[3],
            newpixbuf,
            0,
            0)

        return newpixbuf
