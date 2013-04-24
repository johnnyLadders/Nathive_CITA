#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk

from nathive.lib.plugin import *
from nathive.gui.multiwidget import *


class Crop(PluginTool):

    def __init__(self):

        # Subclass it.
        PluginTool.__init__(self)

        # Common attributes.
        self.name = 'crop'
        self.author = 'nathive-dev'
        self.icon = 'tool-crop.png'

        # Own attributes.
        self.area = [0, 0, 0, 0]
        self.areas = {}
        self.moving = False
        self.resizing = False
        self.hudok = None


    def enable(self):

        document = main.documents.active
        if document in self.areas.keys():
            self.area = self.areas[document]

        hud = main.documents.active.canvas.hud
        self.hudok = hud.add_from_name('hud-ok.png', 0, 0, 10, -10)
        self.hudok.set_display(False)
        if self.area[2] and self.area[3]: self.update_hud()


    def disable(self):

        document = main.documents.active
        self.areas[document] = self.area[:]
        self.area = [0, 0, 0, 0]

        hud = main.documents.active.canvas.hud
        hud.remove(self.hudok)
        hud.remove_area()
        hud.dump()


    def button_primary(self, x, y, ux, uy):

        zone = self.get_zone_index(ux, uy)

        # Move area.
        if zone == 5:
            self.moving = True
            self.root = x, y
            main.gui.cursor.set_from_name('hand-closed')
            return

        # Crop area.
        if zone == 10:
            self.crop()
            return

        # Resize area.
        if zone:                                            # Not zone 5 or 10.
            self.resizing = zone
            self.root = x, y
            self.original = self.area[:]
            return

        # New area.
        self.area[0] = x
        self.area[1] = y


    def motion_primary(self, x, y, ux, uy):

        # Move area.
        if self.moving:
            root_x, root_y = self.root
            self.area[0] += x - root_x
            self.area[1] += y - root_y
            self.root = x, y
            self.update_gui()
            self.update_hud(self.area[0], self.area[1])

        # Resize area.
        elif self.resizing:
            self.resize_area(x, y, self.resizing)
            #self.root = x, y
            self.update_gui()
            self.update_hud()

        # New area.
        else:
            self.area[2] = x - self.area[0]
            self.area[3] = y - self.area[1]
            self.update_gui()
            self.update_hud()


    def motion_over(self, x, y, ux, uy):

        cursor = main.gui.cursor
        zone = self.get_zone_index(ux, uy)

        if zone:
            if zone == 1: cursor.set_from_name('corner-top-left')
            if zone == 2: cursor.set_from_name('side-top')
            if zone == 3: cursor.set_from_name('corner-top-right')
            if zone == 4: cursor.set_from_name('side-left')
            if zone == 5: cursor.set_from_name('hand-open')
            if zone == 6: cursor.set_from_name('side-right')
            if zone == 7: cursor.set_from_name('corner-bottom-left')
            if zone == 8: cursor.set_from_name('side-bottom')
            if zone == 9: cursor.set_from_name('corner-bottom-right')
            if zone == 10: cursor.set_from_name('hand-pointing')

        else: main.gui.cursor.set_default()


    def release_primary(self):

        if self.moving: main.gui.cursor.set_from_name('hand-open')
        self.moving = False
        self.resizing = False


    def key_press(self, keyint):

        if keyint == 65293: self.crop()                            # Enter key.
        elif keyint == 65307: self.cancel()                       # Escape key.
        else: return False
        return True


    def get_zone_index(self, ux, uy):

        area_x, area_y, area_w, area_h = self.get_validated()
        area_xw = area_x + area_w
        area_yh = area_y + area_h
        sandbox = main.documents.active.canvas.sandbox

        border_left, border_top = sandbox.uncoordinate(area_x, area_y)
        border_right, border_bottom = sandbox.uncoordinate(area_xw, area_yh)

        if uy > border_top-10 and uy < border_top+10:
            if ux > border_left-10 and ux < border_left+10: return 1
            if ux > border_left+10 and ux < border_right-10: return 2
            if ux > border_right-10 and ux < border_right+10: return 3
            if ux > border_right+10 and ux < border_right+30: return 10

        if uy > border_top+10 and uy < border_bottom-10:
            if ux > border_left-10 and ux < border_left+10: return 4
            if ux > border_left+10 and ux < border_right-10: return 5
            if ux > border_right-10 and ux < border_right+10: return 6

        if uy > border_bottom-10 and uy < border_bottom+10:
            if ux > border_left-10 and ux < border_left+10: return 7
            if ux > border_left+10 and ux < border_right-10: return 8
            if ux > border_right-10 and ux < border_right+10: return 9


    def resize_area(self, x, y, zone):

        # Calc relatives.
        root_x, root_y = self.root
        rel_x = x - root_x
        rel_y = y - root_y

        # Reverse relative for top and left zones.
        if zone == 1 or zone == 4 or zone == 7: rel_x = -rel_x
        if zone == 1 or zone == 2 or zone == 3: rel_y = -rel_y

        # Disable an axis for central zones.
        if zone == 2 or zone == 8: rel_x = 0
        if zone == 4 or zone == 6: rel_y = 0

        # Resize.
        orig_x, orig_y, orig_w, orig_h = self.original
        self.area[2] = orig_w + rel_x
        self.area[3] = orig_h + rel_y

        # Calc new position if was resized on top or left zones.
        if zone == 4: self.area[0] = orig_x - rel_x
        if zone == 2: self.area[1] = orig_y - rel_y

        # Do proportional scaling for corner zones.
        if zone == 1 or zone == 3 or zone == 7 or zone == 9:
            scale_x = self.area[2] / float(orig_w)
            scale_y = self.area[3] / float(orig_h)
            if scale_x > scale_y: self.area[2] = int(orig_w * scale_y)
            if scale_x < scale_y: self.area[3] = int(orig_h * scale_x)
            if zone == 1 or zone == 7:
                diff_w = self.area[2] - orig_w
                self.area[0] = orig_x - diff_w
            if zone == 1 or zone == 3:
                diff_h = self.area[3] - orig_h
                self.area[1] = orig_y - diff_h

        # Disallow unvalid rectangles.
        if self.area[0] >= orig_x + orig_w: self.area[0] = orig_x + orig_w - 1
        if self.area[1] >= orig_y + orig_h: self.area[1] = orig_y + orig_h - 1
        self.area[2] = max(1, self.area[2])
        self.area[3] = max(1, self.area[3])


    def get_validated(self):

        area = self.area[:]

        if self.area[2] < 0:
            area[2] = abs(area[2])
            area[0] -= area[2]
        if self.area[3] < 0:
            area[3] = abs(area[3])
            area[1] -= area[3]

        return area


    def set_area_from_gui(self):

        self.area[0] = self.gui_x.get_value()
        self.area[1] = self.gui_y.get_value()
        self.area[2] = self.gui_w.get_value()
        self.area[3] = self.gui_h.get_value()
        self.update_hud()


    def update_gui(self):

        area = self.get_validated()
        self.gui_x.set_value(area[0])
        self.gui_y.set_value(area[1])
        self.gui_w.set_value(area[2])
        self.gui_h.set_value(area[3])


    def update_hud(self, x=0, y=0):

        area = self.get_validated()
        hud = main.documents.active.canvas.hud
        if x and y: hud.move_area(x, y)
        else: hud.set_area(area)
        self.hudok.move(area[0] + area[2], area[1])
        self.hudok.set_display(True)
        hud.dump()


    def crop(self):

        offset_x, offset_y, width, height = self.get_validated()
        if width <= 0 or height <= 0: return

        main.documents.active.actions.begin('doc-resize')

        document = main.documents.active
        for layer in document.layers.childs:
            layer.xpos -= offset_x
            layer.ypos -= offset_y

        document.set_dimensions(width, height)
        document.canvas.redraw_all(False)
        document.canvas.sandbox.clear()
        document.canvas.sandbox.redraw_all()

        self.cancel()
        main.gui.statusbar.update()

        offset = offset_x, offset_y
        main.documents.active.actions.end(offset)

        main.gui.cursor.set_default()


    def cancel(self):

        self.hudok.set_display(False)
        self.area = [0] * 4
        self.update_gui()
        hud = main.documents.active.canvas.hud
        hud.remove_area()
        hud.dump()


    def gui(self):

        box = gtk.VBox()

        self.gui_x = MultiWidgetSpin(
            box,
            _('X offset'),
            False,
            -9999,
            9999,
            0,
            lambda x: self.set_area_from_gui())

        self.gui_y = MultiWidgetSpin(
            box,
            _('Y offset'),
            False,
            -9999,
            9999,
            0,
            lambda x: self.set_area_from_gui())

        self.gui_w = MultiWidgetSpin(
            box,
            _('Width'),
            False,
            0,
            10000,
            0,
            lambda x: self.set_area_from_gui())

        self.gui_h = MultiWidgetSpin(
            box,
            _('Height'),
            False,
            0,
            10000,
            0,
            lambda x: self.set_area_from_gui())

        return box
