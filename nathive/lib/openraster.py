#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import shutil
import zipfile
import tempfile
import xml.etree.ElementTree as xml
import gtk


class OpenRaster(object):
    """Library for openraster file hendle."""

    def __init__(self, path, mode='r'):
        """Create a new OpenRaster instance pointing to a disk location.
        @path: File absulute location.
        @mode: Read or write mode as unique char string."""

        self.path = path
        self.writeable = False

        if mode == 'r':
            if os.path.exists(path):
                if not self.check:
                    raise Exception('Path is not an OpenRaster file')
        elif mode == 'w': self.writeable = True
        else: raise Exception('Mode must be r|w')


    def check(self):
        """Check if the current path is a valid openraster file."""

        try:
            zipobj = zipfile.ZipFile(self.path, 'r')
            if zipobj.read('mimetype') == 'image/openraster': return True
            return False
        except:
            return False


    def get_size(self):
        """Retrieve the openraster file width and height.
        =return: A tuple with the width and height."""

        zipobj = zipfile.ZipFile(self.path)
        xmldata = zipobj.read('stack.xml')
        stack = xml.fromstring(xmldata)
        width = int(stack.get('w'))
        height = int(stack.get('h'))
        return (width, height)


    def load(self, document):
        """Load the openraster file contents into the given document.
        @document: A document object, usually empty."""

        zipobj = zipfile.ZipFile(self.path)
        xmldata = zipobj.read('stack.xml')
        image = xml.fromstring(xmldata)
        stack = image.find('stack')
        for layertag in stack.findall('layer'):
            name = layertag.get('name')
            x = int(layertag.get('x')) if layertag.get('x') else 0
            y = int(layertag.get('y')) if layertag.get('y') else 0
            alpha = layertag.get('opacity')
            alpha = float(alpha) if alpha else 1.0
            src = layertag.get('src')
            pngdata = zipobj.read(src)
            pixloader = gtk.gdk.PixbufLoader('png')
            pixloader.write(pngdata)
            pixbuf = pixloader.get_pixbuf()
            pixloader.close()
            layer = document.layers.append_from_pixbuf(pixbuf)
            layer.name = name
            layer.xpos = x
            layer.ypos = y
            layer.alpha = alpha


    def save(self, document):
        """Dump the given document contents to a new openraster file, this
        operation will overwrite files in the current path.
        @document: A document object to dump."""

        # Abort if mode does not allow to write.
        if not self.writeable: raise Exception('Mode is read, unable to write')

        # Create output file.
        fileobj = open(self.path, 'w')
        zipobj = zipfile.ZipFile(fileobj, 'w', zipfile.ZIP_STORED)

        # Create temporal directory.
        tempdir = tempfile.mkdtemp()
        datadir = os.path.join(tempdir, 'data')
        os.mkdir(datadir)
        zipobj.write(datadir, 'data')

        # Create and store mime file.
        mimepath = os.path.join(tempdir, 'mimetype')
        mimefile = open(mimepath, 'w')
        mimefile.write('image/openraster')
        mimefile.close()
        zipobj.write(mimepath, 'mimetype')

        # Create xml file.
        image = xml.Element('image')
        image.set('w', str(document.width))
        image.set('h', str(document.height))
        stack = xml.SubElement(image, 'stack')

        # Iterate over layers.
        for layer in document.layers.childs:

            # Export pixbufs to temporal png files.
            pixfilename = '%s.png' % layer.id
            pixpath = os.path.join(datadir, pixfilename)
            layer.pixbuf.save(pixpath, 'png')
            zipobj.write(pixpath, 'data/%s' % pixfilename)

            # Append layer tag and set attributes.
            layertag = xml.SubElement(stack, 'layer')
            layertag.set('name', layer.name)
            layertag.set('x', str(layer.xpos))
            layertag.set('y', str(layer.ypos))
            layertag.set('opacity', str(layer.alpha))
            layertag.set('src', 'data/%s' % pixfilename)

        # Dump and store xml file.
        stackpath = os.path.join(tempdir, 'stack.xml')
        stacktree = xml.ElementTree(image)
        stacktree.write(stackpath, 'UTF-8')
        stackdata = open(stackpath).read()
        stackdata = stackdata.replace('\n', '')
        stackdata = stackdata.replace('>', '>\n')
        open(stackpath, 'w').write(stackdata)
        zipobj.write(stackpath, 'stack.xml')

        # Calc thumbnail dimensions.
        if document.width > document.height:
            width = min(256, document.width)
            height = width * document.height / document.width
        else:
            height = min(256, document.height)
            width =  height * document.width / document.height

        # Create and store thumbnail.
        thumbpix = document.pixbuf.scale_simple(width, height, 2)
        thumbpath = os.path.join(tempdir, 'thumbnail.png')
        thumbpix.save(thumbpath, 'png')
        zipobj.write(thumbpath, 'thumbnail.png')

        # Delete temporal directory.
        shutil.rmtree(tempdir)
