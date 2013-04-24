#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import copy


class ActionLayerCreate(object):

    def __init__(self, layer):

        # Allow debug tracking.
        main.log.allow_tracking(self)


    def final(self, layer):

        layers = main.documents.active.layers
        self.layer = layer
        self.index = layers.childs.index(layer)
        self.bytes = len(self.layer.pixbuf.get_pixels())


    def restore(self):

        # Remove layer.
        layers = main.documents.active.layers
        layers.childs.remove(self.layer)
        if layers.childs: layers.set_active(layers.childs[0])
        else: layers.set_active(None)

        # Redraw zone.
        layer = self.layer
        area = (layer.xpos, layer.ypos, layer.width, layer.height)
        main.documents.active.canvas.redraw(*area)

        # Notify to tool.
        tool =  main.plugins.activetool
        if tool and hasattr(tool, 'layer_changed'): tool.layer_changed()


    def unrestore(self):

        # Restore layer.
        layers = main.documents.active.layers
        layers.childs.insert(self.index, self.layer)
        layers.set_active(self.layer)

        # Redraw zone.
        layer = self.layer
        area = (layer.xpos, layer.ypos, layer.width, layer.height)
        main.documents.active.canvas.redraw(*area)

        # Notify to tool.
        tool =  main.plugins.activetool
        if tool and hasattr(tool, 'layer_changed'): tool.layer_changed()
