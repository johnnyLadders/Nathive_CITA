#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk
import inspect

from nathive.lib import convert
from nathive.libc import core


class Layer(object):
    """An image layer with extra properties, usually contained in the layer
    management system, but can be used as standalone object."""

    def __init__(self, name, path, width=0, height=0, fill=False):
        """Create the layer."""
        

        #declare pixData Object
        self.pixData = None

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Set attributes.
        self.name = name
        self.id = None
        self.pixbuf = None
        self.xpos = 0
        self.ypos = 0
        self.width = None
        self.height = None
        self.pointer = None
        self.alpha = 1

        # If not dimensions given exit, so the pixbuf must be created later
        # manually with some overwrite method.
        if not width or not height:
            if path: self.overwrite_from_path(path)
            return

        # Create empty pixbuf scratch.
        self.pixbuf = gtk.gdk.Pixbuf(0, True, 8, width, height)

#        # Fill pixbuf.
#        if not fill: fillcolor = 0xffffff00
#        else: fillcolor = 0xffffffff
#        self.pixbuf.fill(fillcolor)

        # Set pixbuf dimensions and memory address.
        self.width = self.pixbuf.get_width()
        self.height = self.pixbuf.get_height()
        self.pointer = convert.pixbuf_pointer(self.pixbuf)


    def update_pointer(self):
        """Update the pixbuf pointer."""

        self.pointer = convert.pixbuf_pointer(self.pixbuf)


    def get_rowstride(self):

        return self.width * 4


    def overwrite_from_path(self, path):

        del(self.pixbuf)
        self.pixbuf = gtk.gdk.pixbuf_new_from_file(path)
        self.pixbuf = self.pixbuf.add_alpha(False, 'W', 'T', 'H')
        self.width = self.pixbuf.get_width()
        self.height = self.pixbuf.get_height()
        self.update_pointer()


    def overwrite_from_data(self, data):

        del(self.pixbuf)
        self.pixbuf = gtk.gdk.pixbuf_new_from_data(
            data,
            0,
            True,
            8,
            self.width,
            self.height,
            self.get_rowstride())
        self.update_pointer()


    def overwrite_from_pixbuf(self, pixbuf):

        del(self.pixbuf)
        self.pixbuf = pixbuf
        self.update_pointer()


    def composite(self, mode, dest, x, y, area_x, area_y, area_w, area_h):
        """Composite the given area of the layer into the destination.
        @mode: Composite mode as int, 0=copy, 1=over, 2=subtractive.
        @dest: Destination layer object, or layer-like object.
        @x: Offset in X axis of the layer into the destination.
        @y: Offset in X axis of the layer into the destination.
        @area_x: Action area X coordinate (in dest scope).
        @area_y: Action area Y coordinate (in dest scope).
        @area_w: Action area rectangle width.
        @area_h: Action area rectangle height."""

        core.composite(
            mode,
            dest.pointer,
            self.pointer,
            dest.width,
            dest.height,
            x,
            y,
            self.width,
            self.height,
            self.alpha,
            area_x,
            area_y,
            area_w,
            area_h)


    def clear(self, x, y, width, height):
        """Clear (fill) the given area with black and opaque pixels."""

        core.clear(self.pointer, self.width, self.height, x, y, width, height)
        
    def initPixData(self):
        
        #if not already initialized
        if(self.pixData is None):
            
            #get index of White in palette
            whiteIndex = main.gui.colorDictionary.palette.index("ffffff")
            
            #initialize with fill of white
            #self.pixData = [[[[whiteIndex,255,1.0]]for j in xrange(self.width)] for i in xrange(self.height)]
            self.pixData = [[[]for j in xrange(self.width)] for i in xrange(self.height)]
