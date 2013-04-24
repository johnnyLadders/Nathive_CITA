#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib import convert


class ActionLayerModify(object):

    def __init__(self, layer):

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Store target layer.
        self.layer = layer

        # Store initial state.
        self.ipixbuf = layer.pixbuf.copy()
        self.ixpos = layer.xpos
        self.iypos = layer.ypos
        self.iwidth = layer.width
        self.iheight = layer.height


    def final(self):

        # Store final state.
        self.fpixbuf = self.layer.pixbuf.copy()
        self.fxpos = self.layer.xpos
        self.fypos = self.layer.ypos
        self.fwidth = self.layer.width
        self.fheight = self.layer.height

        # Calc memory usage.
        self.bytes = 0
        self.bytes += len(self.ipixbuf.get_pixels())
        self.bytes += len(self.fpixbuf.get_pixels())


    def restore(self):

        # Set the target layer as active.
        main.documents.active.layers.set_active(self.layer, False)
        main.gui.sidebar.layers.dump()

        # Restore layer.
        self.layer.pixbuf = self.ipixbuf.copy()
        self.layer.pointer = convert.pixbuf_pointer(self.layer.pixbuf)
        self.layer.xpos = self.ixpos
        self.layer.ypos = self.iypos
        self.layer.width = self.iwidth
        self.layer.height = self.iheight

        # Redraw areas.
        iarea = (self.ixpos, self.iypos, self.iwidth, self.iheight)
        farea = (self.fxpos, self.fypos, self.fwidth, self.fheight)
        main.documents.active.canvas.redraw(*iarea)
        main.documents.active.canvas.redraw(*farea)

        # Notify to tool.
        tool =  main.plugins.activetool
        if tool and hasattr(tool, 'layer_changed'): tool.layer_changed()


    def unrestore(self):

        # Set the target layer as active.
        main.documents.active.layers.set_active(self.layer, False)
        main.gui.sidebar.layers.dump()

        # Unrestore layer.
        self.layer.pixbuf = self.fpixbuf.copy()
        self.layer.pointer = convert.pixbuf_pointer(self.layer.pixbuf)
        self.layer.xpos = self.fxpos
        self.layer.ypos = self.fypos
        self.layer.width = self.fwidth
        self.layer.height = self.fheight

        # Redraw areas.
        iarea = (self.ixpos, self.iypos, self.iwidth, self.iheight)
        farea = (self.fxpos, self.fypos, self.fwidth, self.fheight)
        main.documents.active.canvas.redraw(*iarea)
        main.documents.active.canvas.redraw(*farea)

        # Notify to tool.
        tool =  main.plugins.activetool
        if tool and hasattr(tool, 'layer_changed'): tool.layer_changed()
