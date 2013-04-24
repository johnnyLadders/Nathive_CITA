#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import copy
import gtk

from nathive.lib.plugin import *
from nathive.libc import select
from nathive.lib import convert
from nathive.gui.multiwidget import *


class Select(PluginTool):

    def __init__(self):

        # Subclass it.
        PluginTool.__init__(self)

        # Common attributes.
        self.name = 'select'
        self.author = 'nathive-dev'
        self.icon = 'tool-select.png'

        # Hud items (scale and rotate indicators).
        self.huditems = []
        self.hudflush = None

        # More attributes.
        self.mode = False
        self.shi = None                                    # Selected hud item.
        self.oldlayer = None
        self.fakelayer = None
        self.resizelayer = None

        # Load attributes from cfg file.
        self.default()
        main.config.push_to_plugin(self)


    def enable(self):
        """To do when the tool is selected."""

        # Alias hud.
        hud = main.documents.active.canvas.hud

        # Add resize hud items.
        self.huditems = []
        for i in range(8):
            huditem = hud.add_from_name('hud-scale.png', 0, 0, -5, -5)
            self.huditems.append(huditem)

        # Add flush hud item.
        self.hudflush = hud.add_from_name('hud-ok.png', 0, 0, 10, -10)
        self.hudflush.set_display(False)

        # Reposition all hud items.
        self.reposition_huds()


    def disable(self):
        """To do when the tool is unselected."""

        self.flush_resized_layer()
        hud = main.documents.active.canvas.hud
        for huditem in self.huditems: hud.remove(huditem)
        hud.remove(self.hudflush)


    def default(self):

        self.interpolation = 1


    def update(self):

        self.gui_interpolation.set_value(self.interpolation)


    def layer_changed(self):

        self.flush_resized_layer()
        self.reposition_huds()


    def reposition_huds(self):

        if main.plugins.activetool is not self: return
        document = main.documents.active
        if not document: return
        layer = document.layers.active
        if not layer: return

        x = layer.xpos
        y = layer.ypos
        w = layer.width
        h = layer.height
        mw = w / 2
        mh = h / 2

        self.huditems[0].move(x, y)
        self.huditems[1].move(x+mw, y)
        self.huditems[2].move(x+w, y)
        self.huditems[3].move(x, y+mh)
        self.huditems[4].move(x+w, y+mh)
        self.huditems[5].move(x, y+h)
        self.huditems[6].move(x+mw, y+h)
        self.huditems[7].move(x+w, y+h)

        self.hudflush.move(x+w, y)

        hud = main.documents.active.canvas.hud
        hud.dump()


    def select_layer(self, x, y):
        """Activate the toplevel layer for the given coordinates.
        @x: coordinate in X axis.
        @y: coordinate in Y axis."""

        layers = main.documents.active.layers
        for layer in reversed(layers.childs):
            if x < layer.xpos or x > layer.xpos + layer.width: continue
            if y < layer.ypos or y > layer.ypos + layer.height: continue
            args = (layer.pointer, layer.width, x-layer.xpos, y-layer.ypos)
            if not select.get_pixel_alpha(*args): continue
            if layer == layers.active: break
            layers.set_active(layer)
            break


    def move_layer(self, x, y , ux, uy):

        # Reposition layer.
        document = main.documents.active
        layer = document.layers.active
        layer.xpos += (x - self.xroot)
        layer.ypos += (y - self.yroot)

        # Reposition huds (better performance than repostion method).
        for huditem in self.huditems:
            huditem.x += (x - self.xroot)
            huditem.y += (y - self.yroot)
        self.hudflush.x += (x - self.xroot)
        self.hudflush.y += (y - self.yroot)
        document.canvas.hud.dump()

        # Reset root coordinates.
        self.xroot = x
        self.yroot = y

        # Redraw zone.
        document.canvas.redraw_step(
            layer.xpos - 50,
            layer.ypos - 50,
            layer.width + 50,
            layer.height + 50)


    def get_selected_hud_item(self, ux, uy):
        """Check if the coordinates correspond to some hud item.
        @ux: Coordinate in X axis at user scope.
        @uy: Coordinate in Y axis at user scope.
        =return: 1:9 for resize hud (index+1), -1 for flush hud, 0 for none."""

        # Alias.
        layer = main.documents.active.layers.active
        sandbox = main.documents.active.canvas.sandbox

        # Check resize hud items.
        for item in self.huditems:
            item_x, item_y = sandbox.uncoordinate(item.x, item.y)
            if ux < item_x-5 or ux > item_x+5: continue
            if uy < item_y-5 or uy > item_y+5: continue
            return self.huditems.index(item) + 1

        # Check flush hud item.
        item_x, item_y = sandbox.uncoordinate(self.hudflush.x, self.hudflush.y)
        if ux < item_x+10 or ux > item_x+30: return 0
        if uy < item_y-10 or uy > item_y+10: return 0
        return -1


    def resize_layer(self, x, y ,ux, uy):

        # Alias active canvas and active layer.
        canvas = main.documents.active.canvas
        layer = main.documents.active.layers.active

        # Copy active layer.
        if not self.oldlayer:
            document = main.documents.active
            document.actions.begin('layer-modify')
            self.oldlayer = copy.copy(layer)
            self.fakelayer = copy.copy(layer)
            self.resizelayer = layer
            self.hudflush.set_display(True)

        # Get relative coordinates from root.
        rel_x = (x - self.xroot)
        rel_y = (y - self.yroot)

        # Alias selected hud item.
        shi = self.shi

        # Reverse relative for top and left hud items.
        if shi == 0 or shi == 3 or shi == 5: rel_x = -rel_x
        if shi == 0 or shi == 1 or shi == 2: rel_y = -rel_y

        # Disable an axis for central hud items.
        if shi == 1 or shi == 6: rel_x = 0
        if shi == 3 or shi == 4: rel_y = 0

        # Calc new dimensions.
        width = self.fakelayer.width + rel_x
        height = self.fakelayer.height + rel_y

        # Do proportional scaling for corner hud items.
        if shi == 0 or shi == 2 or shi == 5 or shi == 7:
            scale_x = float(width) / self.fakelayer.width
            scale_y = float(height) / self.fakelayer.height
            if scale_x > scale_y: width = self.fakelayer.width * scale_y
            else: height = self.fakelayer.height * scale_x

        # Calc new position.
        pos_x = self.fakelayer.xpos
        pos_y = self.fakelayer.ypos
        if shi == 0 or shi == 3 or shi == 5:
            pos_x += self.fakelayer.width - width
        if shi == 0 or shi == 1 or shi == 2:
            pos_y += self.fakelayer.height - height

        # Convert to avoid deprecations.
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        width = int(width)
        height = int(height)

        # Scale to new dimensions
        pixbuf = self.oldlayer.pixbuf.scale_simple(width, height, 0)

        # Set the temporal layer attributes.
        layer.pixbuf = pixbuf
        layer.pointer = convert.pixbuf_pointer(layer.pixbuf)
        layer.xpos = pos_x
        layer.ypos = pos_y
        layer.width = width
        layer.height = height

        # Reposition hud items and redraw affected area.
        self.reposition_huds()
        canvas.redraw_step(layer.xpos, layer.ypos, layer.width, layer.height)


    def flush_resized_layer(self):

        # Return if no resizing flush is pending.
        if not self.fakelayer: return

        # Alias active canvas and resizing layer.
        canvas = main.documents.active.canvas
        layer = self.resizelayer

        if self.interpolation == 0: interpolation = 0
        if self.interpolation == 1: interpolation = 2
        if self.interpolation == 2: interpolation = 3

        # Do the final scaling.
        pixbuf = self.oldlayer.pixbuf.scale_simple(
            self.fakelayer.width,
            self.fakelayer.height,
            interpolation)

        # Set layer attributes from fake layer.
        layer.pixbuf = pixbuf
        layer.pointer = convert.pixbuf_pointer(pixbuf)
        layer.xpos = self.fakelayer.xpos
        layer.ypos = self.fakelayer.ypos
        layer.width = self.fakelayer.width
        layer.height = self.fakelayer.height

        # Redraw layer.
        main.documents.active.layers.update_prelower()
        main.documents.active.layers.update_preupper()
        canvas.redraw_step(layer.xpos, layer.ypos, layer.width, layer.height)

        # Disable resizing mode.
        self.oldlayer = None
        self.fakelayer = None
        self.resizelayer = None
        self.mode = None

        # Hide flush hud item.
        self.hudflush.set_display(None)
        self.reposition_huds()

        # End resizing action.
        document = main.documents.active
        document.actions.end()


    def cancel_resized_layer(self):

        # Return if no resizing flush is pending.
        if not self.fakelayer: return

        # Alias active canvas and resizing layer.
        canvas = main.documents.active.canvas
        layer = self.resizelayer

        # Set layer attributes from fake layer.
        layer.pixbuf = self.oldlayer.pixbuf
        layer.pointer = convert.pixbuf_pointer(self.oldlayer.pixbuf)
        layer.xpos = self.oldlayer.xpos
        layer.ypos = self.oldlayer.ypos
        layer.width = self.oldlayer.width
        layer.height = self.oldlayer.height

        # Reposition hud items and redraw affected area.
        self.hudflush.set_display(None)
        self.reposition_huds()
        main.documents.active.layers.update_prelower()
        main.documents.active.layers.update_preupper()
        canvas.redraw_step(layer.xpos, layer.ypos, layer.width, layer.height)

        # Disable resizing mode.
        self.oldlayer = None
        self.fakelayer = None
        self.resizelayer = None
        self.mode = None


    def button_primary(self, x, y, ux, uy):

        self.xroot = x
        self.yroot = y
        shi = self.get_selected_hud_item(ux, uy)

        # If resize hud is clicked.
        if shi > 0:
            self.mode = 'resize'
            self.shi = shi - 1

        # If flush hud is clicked.
        elif shi == -1:
            self.flush_resized_layer()

        # Else select layer and/or move it.
        else:
            self.select_layer(x, y)
            if self.mode != 'resize':
                document = main.documents.active
                document.actions.begin('layer-move')
            self.mode = 'move'


    def motion_primary(self, x, y, ux, uy):

        if self.mode == 'move': self.move_layer(x, y, ux, uy)
        if self.mode == 'resize': self.resize_layer(x, y, ux, uy)


    def release_primary(self):

        # If a resize is unflushed update the fakelayer attributes.
        if self.fakelayer:
            self.shi = None
            layer = main.documents.active.layers.active
            self.fakelayer.xpos = layer.xpos
            self.fakelayer.ypos = layer.ypos
            self.fakelayer.width = layer.width
            self.fakelayer.height = layer.height

        # Else end unfinished layer moves.
        else:
            if self.mode == 'move':
                document = main.documents.active
                document.actions.end()
                self.mode = None

        # Avoid save root coordinates in configs.
        del self.xroot, self.yroot


    def key_press(self, keyint):

        if not self.fakelayer: return False
        if keyint == 65293: self.flush_resized_layer()            # Enter key.
        elif keyint == 65307: self.cancel_resized_layer()         # Escape key.
        else: return False
        return True


    def gui(self):

        self.box = gtk.VBox()

        self.gui_interpolation = MultiWidgetCombo(
            self.box,
            _('Scaling'),
            [_('Fast'), _('Normal'), _('Quality')],
            self.interpolation,
            lambda x: setattr(self, 'interpolation', x))

        return self.box
