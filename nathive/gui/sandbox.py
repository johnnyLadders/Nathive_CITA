#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import math
import gtk

from nathive.lib.layer import Layer


class Sandbox(object):

    def __init__(self, canvas):

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Store parent canvas to use in methods.
        self.canvas = canvas

        # Attributes.
        self.factor = 1.0
        self.interpolation = gtk.gdk.INTERP_NEAREST
        self.offset_x = 0
        self.offset_y = 0
        self.redraw_blocked = False

        # Raise recursion margin to avoid halt while masive events input.
        sys.setrecursionlimit(10000)


    def __del__(self):

        self.image.destroy()
        del(self.pixbuf)
        del(self.background)


    def recoordinate(self, x, y):

        adj_x, adj_y = self.get_adjustment_values()
        x += adj_x - self.offset_x
        y += adj_y - self.offset_y
        x /= self.factor
        y /= self.factor
        return (int(x), int(y))


    def uncoordinate(self, x, y):

        adj_x, adj_y = self.get_adjustment_values()
        x *= self.factor
        y *= self.factor
        x -= adj_x - self.offset_x
        y -= adj_y - self.offset_y
        return (int(x), int(y))


    def get_alloc(self):

        return [
            self.canvas.eventbox.allocation.width,
            self.canvas.eventbox.allocation.height]


    def get_adjustment_values(self):

        return [
            int(self.canvas.hadjustment.value),
            int(self.canvas.vadjustment.value)]


    def clear(self):

        self.pixbuf.fill(0x00000000)


    def test(self):

        sandbox_width, sandbox_height = self.get_alloc()

        # Test if there is no need to rebuild.
        if hasattr(self, 'pixbuf'):
            samewidth = sameheight = False
            if self.pixbuf.get_width() == sandbox_width: samewidth = True
            if self.pixbuf.get_height() == sandbox_height: sameheight = True
            if samewidth and sameheight: return

        # Remove old sandbox image and pixbuf.
        if hasattr(self, 'image'):
            self.canvas.layout.remove(self.image)
            del(self.image)
            del(self.pixbuf)

        # Set sandbox pixbuf and image widget.
        self.pixbuf = gtk.gdk.Pixbuf(
            gtk.gdk.COLORSPACE_RGB,
            True,
            8,
            sandbox_width,
            sandbox_height)
        self.image = gtk.image_new_from_pixbuf(self.pixbuf)
        self.clear()

        # Set background.
        pattern_path = os.path.join(main.imgpath, 'pattern.png')
        pattern = Layer('pattern', pattern_path)
        self.background = Layer(
            'background',
            None,
            sandbox_width + pattern.width,
            sandbox_height + pattern.height)

        # Determine how many times the pattern needs to be drawn.
        xtimes = float(1) * self.background.width / pattern.width
        ytimes = float(1) * self.background.height / pattern.height
        xtimes = int(math.ceil(xtimes))
        ytimes = int(math.ceil(ytimes))

        # Draw the pattern into the background.
        for x in range(xtimes):
            for y in range(ytimes):
                pattern.composite(
                    1,
                    self.background,
                    x * pattern.width,
                    y * pattern.height,
                    x * pattern.width,
                    y * pattern.height,
                    pattern.width,
                    pattern.height)

        # Set pattern dimensions, useful to set the correct background offset.
        self.background.pattern_width = pattern.width
        self.background.pattern_height = pattern.height

        # Add sandbox image to table and display it.
        self.canvas.layout.put(self.image, 0, 0)
        self.canvas.layout_reverse()
        self.image.show()


    def redraw_all(self, center=False, gap=False, scroll=False):

        if gtk.events_pending(): gtk.main_iteration()

        if self.redraw_blocked: return
        else: self.redraw_blocked = True

        if scroll:
            self.redraw_blocked = False
            if gtk.events_pending(): return           # This recursion improves
            self.redraw_all()                         # a lot the performance.
            hud =  self.canvas.hud
            if hud.area and hud.area_sandboxed:     # Refresh hud area while
                hud.set_area(None)                  # scroll if it's sandboxed.
                hud.dump()
            return

        self.test()
        sandbox_width, sandbox_height = self.get_alloc()
        adj_x, adj_y = self.get_adjustment_values()

        # Calc displayed image fake dimensions.
        fakewidth = self.canvas.document.width * self.factor
        fakeheight = self.canvas.document.height * self.factor

        # Calc adjustment values.
        if center:
            center = [x * float(self.factor) for x in center]
            adj_x = center[0] - (sandbox_width / 2) - gap[0]
            adj_y = center[1] - (sandbox_height / 2) - gap[1]
        else:
            adj_x, adj_y = self.get_adjustment_values()

        # Put horizontal adjustment value into limits, get offset.
        if fakewidth > sandbox_width:
            adj_x = max(0, adj_x)
            adj_x = min(adj_x, fakewidth - sandbox_width)
            self.offset_x = 0
            self.canvas.hscrollbar.show()
        else:
            adj_x = 0
            self.offset_x = int((sandbox_width - fakewidth) / 2)
            self.canvas.hscrollbar.hide()

        # Put vertical adjustment value into limits, get offset.
        if fakeheight > sandbox_height:
            adj_y = max(0, adj_y)
            adj_y = min(adj_y, fakeheight - sandbox_height)
            self.offset_y = 0
            self.canvas.vscrollbar.show()
        else:
            adj_y = 0
            self.offset_y = int((sandbox_height - fakeheight) / 2)
            self.canvas.vscrollbar.hide()

        # Corrector for gtk.Pixbuf.scale() bug. <http://ur1.ca/v9ps>
        if self.factor > 16 and self.factor % 16:
            corrector_x = int((adj_x + 2048) / 4096.0)
            corrector_y = int((adj_y + 2048) / 4096.0)
        else:
            corrector_x = 0
            corrector_y = 0

        # Dump background into sandbox.
        self.background.pixbuf.scale(
            self.pixbuf,
            self.offset_x,
            self.offset_y,
            int(min(sandbox_width, fakewidth)),
            int(min(sandbox_height, fakeheight)),
            self.offset_x - adj_x % self.background.pattern_width,
            self.offset_y - adj_y % self.background.pattern_height,
            1,
            1,
            self.interpolation)

        # Dump image into sandbox.
        self.canvas.document.pixbuf.composite(
            self.pixbuf,
            self.offset_x,
            self.offset_y,
            int(min(sandbox_width, fakewidth)),
            int(min(sandbox_height, fakeheight)),
            -adj_x + self.offset_x - corrector_x,
            -adj_y + self.offset_y - corrector_y,
            self.factor,
            self.factor,
            self.interpolation,
            255)

        # Refresh sandbox image.
        self.image.queue_draw()

        # Set new adjustment parameters.
        self.canvas.hadjustment.set_all(
            adj_x, 0, fakewidth, 10, 10, sandbox_width)
        self.canvas.vadjustment.set_all(
            adj_y, 0, fakeheight, 10, 10, sandbox_height)

        # Unblock sandbox redraw.
        self.redraw_blocked = False

        # Refresh hud.
        self.canvas.hud.dump()


    def redraw(self, x, y, width, height):

        if gtk.events_pending(): gtk.main_iteration()

        if self.redraw_blocked: return
        else: self.redraw_blocked = True

        sandbox_width, sandbox_height = self.get_alloc()
        adj_x, adj_y = self.get_adjustment_values()

        # Calc displayed image fake dimensions.
        fakewidth = self.canvas.document.width * self.factor
        fakeheight = self.canvas.document.height * self.factor

        # Calc fixed area.
        fixed_x = int((x * self.factor) + self.offset_x - adj_x)
        fixed_y = int((y * self.factor) + self.offset_y - adj_y)
        fixed_width = int(width * self.factor)
        fixed_height = int(height * self.factor)

        # Cut right margin excess.
        over_x = fixed_x + fixed_width - self.offset_x
        max_x = int(min(fakewidth, sandbox_width))
        if over_x > max_x:
            fixed_width -=  over_x - max_x
            fixed_width = max(0, fixed_width)

        # Cut bottom margin excess.
        over_y = fixed_y + fixed_height - self.offset_y
        max_y = int(min(fakeheight, sandbox_height))
        if over_y > max_y:
            fixed_height -=  over_y - max_y
            fixed_height = max(0, fixed_height)

        # Cut left margin excess.
        over_x = fixed_x - self.offset_x
        if over_x < 0:
            fixed_width += over_x
            fixed_width = max(0, fixed_width)
            fixed_x = 0 + self.offset_x

        # Cut top margin excess.
        over_y = fixed_y - self.offset_y
        if over_y < 0:
            fixed_height += over_y
            fixed_height = max(0, fixed_height)
            fixed_y = 0 + self.offset_y

        # Return if there is no area after cut.
        if not fixed_width or not fixed_height:
            self.redraw_blocked = False
            return

        # Corrector for gtk.Pixbuf.scale() bug. <http://ur1.ca/v9ps>
        if self.factor > 16 and self.factor % 16:
            corrector_x = int((adj_x + 2048) / 4096.0)
            corrector_y = int((adj_y + 2048) / 4096.0)
        else:
            corrector_x = 0
            corrector_y = 0

        # Dump background into sandbox.
        self.background.pixbuf.scale(
            self.pixbuf,
            fixed_x,
            fixed_y,
            fixed_width,
            fixed_height,
            self.offset_x - adj_x % self.background.pattern_width,
            self.offset_y - adj_y % self.background.pattern_height,
            1,
            1,
            self.interpolation)

        # Dump image into sandbox.
        self.canvas.document.pixbuf.composite(
            self.pixbuf,
            fixed_x,
            fixed_y,
            fixed_width,
            fixed_height,
            self.offset_x - adj_x - corrector_x,
            self.offset_y - adj_y - corrector_y,
            self.factor,
            self.factor,
            self.interpolation,
            255)

        # Refresh sandbox image.
        self.image.queue_draw_area(
            fixed_x,
            fixed_y,
            fixed_width ,
            fixed_height)

        # Unblock sandbox redraw.
        self.redraw_blocked = False
