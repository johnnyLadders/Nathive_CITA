#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


class ActionDocResize(object):

    def __init__(self, document):

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Store initial dimensions.
        self.document = document
        self.iwidth = self.document.width
        self.iheight = self.document.height


    def final(self, offset):

        # Store offset and final dimensions.
        self.offset_x, self.offset_y = offset
        self.fwidth = self.document.width
        self.fheight = self.document.height


    def restore(self):

        # Restore layer positions.
        for layer in self.document.layers.childs:
            layer.xpos += self.offset_x
            layer.ypos += self.offset_y

        # Restore dimensions and refresh.
        self.document.set_dimensions(self.iwidth, self.iheight)
        self.refresh()


    def unrestore(self):

        # Unrestore layer positions.
        for layer in self.document.layers.childs:
            layer.xpos -= self.offset_x
            layer.ypos -= self.offset_y

        # Unrestore dimensions and refresh.
        self.document.set_dimensions(self.fwidth, self.fheight)
        self.refresh()


    def refresh(self):

        # Refresh canvas.
        self.document.canvas.redraw_all(False)
        self.document.canvas.sandbox.clear()
        self.document.canvas.sandbox.redraw_all()

        # Refresh statusbar.
        main.gui.statusbar.update()
