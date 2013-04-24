#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


class ActionLayerMove(object):

    def __init__(self, layer):

        # Allow debug tracking.
        main.log.allow_tracking(self)

        self.layer = layer
        self.xdiff = -self.layer.xpos
        self.ydiff = -self.layer.ypos


    def final(self):

        self.xdiff += self.layer.xpos
        self.ydiff += self.layer.ypos
        self.bytes = 0


    def restore(self):

        # Set the target layer as active.
        main.documents.active.layers.set_active(self.layer, False)
        main.gui.sidebar.layers.dump()

        # Get redraw zone.
        zone = [0] * 4
        if self.xdiff > 0: zone[0] = self.layer.xpos - self.xdiff
        else: zone[0] = self.layer.xpos
        if self.ydiff > 0: zone[1] = self.layer.ypos - self.ydiff
        else: zone[1] = self.layer.ypos
        zone[2] = abs(self.xdiff) + self.layer.width
        zone[3] = abs(self.ydiff) + self.layer.height

        # Restore layer position.
        self.layer.xpos -= self.xdiff
        self.layer.ypos -= self.ydiff

        # Redraw zone.
        main.documents.active.canvas.redraw(*zone)

        # Notify to tool.
        tool =  main.plugins.activetool
        if tool and hasattr(tool, 'layer_changed'): tool.layer_changed()


    def unrestore(self):

        # Set the target layer as active.
        main.documents.active.layers.set_active(self.layer, False)
        main.gui.sidebar.layers.dump()

        # Get redraw zone.
        zone = [0] * 4
        if self.xdiff < 0: zone[0] = self.layer.xpos + self.xdiff
        else: zone[0] = self.layer.xpos
        if self.ydiff < 0: zone[1] = self.layer.ypos + self.ydiff
        else: zone[1] = self.layer.ypos
        zone[2] = abs(self.xdiff) + self.layer.width
        zone[3] = abs(self.ydiff) + self.layer.height

        # Unrestore layer position.
        self.layer.xpos += self.xdiff
        self.layer.ypos += self.ydiff

        # Redraw zone.
        main.documents.active.canvas.redraw(*zone)

        # Notify to tool.
        tool =  main.plugins.activetool
        if tool and hasattr(tool, 'layer_changed'): tool.layer_changed()
