#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import gtk

from nathive.lib.layers import Layers
from nathive.lib.actions import Actions
from nathive.lib.openraster import OpenRaster
from nathive.lib import convert
from nathive.gui.canvas import Canvas


class Document(object):
    """Define document instances, each image opened."""

    def __init__(self, path, width=0, height=0):
        """Create a document instance from file or totally new.
        @path: Path of the requested image.
        @width: If no path given, width of new document.
        @height: If no path given, height of new document."""

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # If path given.
        self.path = path
        if path:

            # If given file is openraster, load it.
            name, ext = os.path.splitext(path)
            if ext == '.ora':
                ora = OpenRaster(path)
                width, height = ora.get_size()
                self.mime = 'image/openraster'
                self.configure(width, height)
                self.layers = Layers(self)
                ora.load(self)

            # If given file is an image loadable by gtk, load it.
            else:
                info, width, height = gtk.gdk.pixbuf_get_file_info(path)
                self.mime = info['mime_types'][0]
                self.configure(width, height)
                self.layers = Layers(self)
                self.layers.append_from_path(path)
                self.layers.active.name = _('Original')

        # If not path given, create a blank document.
        else:
            self.configure(width, height)
            self.layers = Layers(self)
            self.layers.append_blank(width, height, True)

        # Set canvas and action tracker.
        self.canvas = Canvas(self)
        self.actions = Actions(self)


    def configure(self, width, height):

        # Create pixbuf.
        self.pixbuf = gtk.gdk.Pixbuf(
            gtk.gdk.COLORSPACE_RGB,
            True,
            8,
            width,
            height)

        # Set attributes from pixbuf.
        self.pointer = convert.pixbuf_pointer(self.pixbuf)
        self.width = width
        self.height = height
        self.alpha = 1


    def __del__(self):

        pass


    def set_path(self, path):
        """Set a new path for the document, usually when is saved in other site.
        @path: The new path, must be absolute."""

        self.path = path
        main.gui.tabs.update_title(self)


    def set_mime_from_format(self, format):
        """Set a new mime type converting the passed format string.
        @format: File format string like 'png'."""

        if format == 'ora': mime = 'image/openraster'
        elif format == 'png': mime = 'image/png'
        elif format == 'jpg' or format == 'jpeg': mime = 'image/jpeg'
        else: raise ValueError("Given format must be ora|png|jpg")
        self.mime = mime


    def set_dimensions(self, width, height):

        self.configure(width, height)
        self.layers.update_pre()


    def export(self, path, format, quality=None):

        # OpenRaster format.
        if format == 'ora':
            ora = OpenRaster(path, 'w')
            ora.save(self)

        # PNG format.
        if format == 'png':
            pixbuf = self.pixbuf
            pixbuf.save(path, format)

        # JPG format.
        if format == 'jpg':
            format = 'jpeg'
            if quality: options = {'quality':str(quality)}
            else: options = {'quality':'90'}
            pixbuf = self.layers.get_noalpha().pixbuf
            pixbuf.save(path, format, options)

        # Print message to stdout.
        main.log.info('saving doc: %s' % path)
