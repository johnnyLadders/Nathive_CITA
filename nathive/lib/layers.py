#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import math

from nathive.lib.layer import Layer
from nathive.lib import convert


class Layers(object):
    """The layer management system, each document has its own instance.
    ⌥: Main > Documents > {n}Document > Layers."""

    def __init__(self, document):
        """Set up the layer management system.
        @document: The parent document instance."""

        # Allow debug tracking.
        main.log.allow_tracking(self)

        self.document = document
        self.childs = []
        self.active = None
        self.count = 0
        self.prelower = None
        self.preupper = None


    def __del__(self):

        pass


    def set_active(self, layer, redraw=True):

        # Change active and refresh preloaded layers.
        self.active = layer
        self.update_prelower()
        self.update_preupper()

        # Redraw canvas and refresh sidebar.
        if redraw:
            if hasattr(self.document, 'canvas'):
                self.document.canvas.redraw_all()
                main.gui.sidebar.layers.dump()

        # Allow tracking for tools.
        if hasattr(main.plugins.activetool, 'layer_changed'):
            main.plugins.activetool.layer_changed()


    def set_active_from_index(self, index):

        layer = self.childs[index]
        self.set_active(layer, False)


    def get_layer_from_index(self, index):

        return self.childs[index]


    def append_blank(self, width=0, height=0, fill=False):

        name = '%s %s' % (_('New'), self.count)
        if not width: width = self.document.width
        if not height: height = self.document.height
        layer = Layer(name, None, width, height, fill)
        self.childs.append(layer)
        self.set_active(layer)
        layer.id = self.count
        self.count += 1
        return layer


    def append_blank_tracked(self):

        self.document.actions.begin('layer-create')
        layer = self.append_blank()
        self.document.actions.end(layer)


    def append_from_path(self, path):

        name = name = '%s %s' % (_('Imported'), self.count)
        layer = Layer(name, None)
        layer.overwrite_from_path(path)
        self.childs.append(layer)
        self.set_active(layer)
        layer.id = self.count
        self.count += 1


    def append_from_data(self, data, width, height):

        name = name = '%s %s' % (_('Pasted'), self.count)
        layer = Layer(name, None, width, height)
        layer.overwrite_from_data(data)
        self.childs.append(layer)
        self.set_active(layer)
        layer.id = self.count
        self.count += 1
        return layer


    def append_from_pixbuf(self, pixbuf):

        name = name = '%s %s' % (_('Pasted'), self.count)
        layer = Layer(name, None, pixbuf.get_width(), pixbuf.get_height())
        layer.overwrite_from_pixbuf(pixbuf)
        self.childs.append(layer)
        self.set_active(layer)
        layer.id = self.count
        self.count += 1
        return layer


    def duplicate_active(self):

        name = '%s copy' % self.active.name
        copy = Layer(name, None, self.active.width, self.active.height)
        copy.pixbuf = self.active.pixbuf.copy()
        copy.update_pointer()
        copy.xpos = self.active.xpos
        copy.ypos = self.active.ypos
        self.childs.append(copy)
        self.set_active(copy)
        copy.id = self.count
        self.count += 1


    def swap_up_active(self):

        index = self.childs.index(self.active)
        self.childs.remove(self.active)
        self.childs.insert(index + 1, self.active)
        self.set_active(self.active)


    def swap_down_active(self):

        index = self.childs.index(self.active)
        self.childs.remove(self.active)
        newindex = index - 1
        if newindex < 0: newindex = 0
        self.childs.insert(newindex, self.active)
        self.set_active(self.active)


    def remove(self, layer):

        self.document.actions.begin('layer-remove')
        self.childs.remove(layer)
        if self.childs: self.set_active(self.childs[0])
        else: self.set_active(None)
        self.document.actions.end()


    def remove_active(self):

        self.remove(self.active)


    def update_pre(self):

        self.update_prelower()
        self.update_preupper()


    def update_prelower(self):
        """Creates a preload of all layers before the active layer."""

        # Init layer.
        prelower = Layer(
            'prelower',
            None,
            self.document.width,
            self.document.height)
        self.prelower = prelower

        # Draw bottom layers.
        for layer in self.childs:
            if layer is self.active: break
            layer.composite(
                1,
                prelower,
                layer.xpos,
                layer.ypos,
                layer.xpos,
                layer.ypos,
                layer.width,
                layer.height)


    def update_preupper(self):
        """Creates a preload of all layers after the active layer."""

        # Init layer.
        preupper = Layer(
            'preupper',
            None,
            self.document.width,
            self.document.height)
        self.preupper = preupper

        # Draw upper layers.
        for layer in self.childs:
            layer_index = self.childs.index(layer)
            active_index = self.childs.index(self.active)
            if layer_index <= active_index: continue
            layer.composite(
                1,
                preupper,
                layer.xpos,
                layer.ypos,
                layer.xpos,
                layer.ypos,
                layer.width,
                layer.height)


    def get_noalpha(self):

        # Init layer.
        noalpha = Layer(
            'noalpha',
            None,
            self.document.width,
            self.document.height,
            True)

        for layer in self.childs:
            layer.composite(
                1,
                noalpha,
                layer.xpos,
                layer.ypos,
                layer.xpos,
                layer.ypos,
                layer.width,
                layer.height)

        return noalpha
