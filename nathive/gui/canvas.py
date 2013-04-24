#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import time
import gtk

from nathive.libc import core
from nathive.gui.sandbox import Sandbox
from nathive.gui.hud import Hud


class Canvas(object):
    """Canvas macro-widget displayed into tabs, each resulting object manage
    the visual representation of the parent document, including scrollbars,
    sandbox zoom system and hud floating stuff.
    ⌥: Main > Documents > {n}Document > Canvas."""

    def __init__(self, document):
        """Create canvas and show it.
        @document: Parent document object."""

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Store parent document to use in methods.
        self.document = document

        # Last redraw timestamp.
        self.lastredraw = None

        # Event hook.
        self.pressed_button = 0
        self.layout = gtk.Layout()
        self.eventbox = gtk.EventBox()

        self.eventbox.add(self.layout)
        self.eventbox.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.eventbox.connect('button-press-event', self.button_cb)
        self.eventbox.connect('button-release-event', self.release_cb)
        self.eventbox.connect('motion-notify-event', self.motion_cb)
        self.eventbox.connect('scroll-event', self.zoom_cb)
        self.eventbox.connect('enter-notify-event', self.enter_cb)
        self.eventbox.connect('leave-notify-event', self.leave_cb)
        self.eventbox.connect('size_allocate', self.allocate_cb)
        self.last_allocation_area = None
        self.last_motion_coordinates = None

        main.gui.window.add_events(gtk.gdk.POINTER_MOTION_MASK)
        main.gui.window.connect('key-press-event', self.key_cb)

        # Scrollbars.
        self.hscrollbar = gtk.HScrollbar()
        self.vscrollbar = gtk.VScrollbar()
        self.hadjustment = self.hscrollbar.get_adjustment()
        self.vadjustment = self.vscrollbar.get_adjustment()
        self.hadjustment.connect(
            'value-changed',
            lambda x: self.sandbox.redraw_all(False, False, True))
        self.vadjustment.connect(
            'value-changed',
            lambda x: self.sandbox.redraw_all(False, False, True))

        # Table.
        self.table = gtk.Table(2, 2)
        self.table.attach(self.eventbox, 0, 1, 0, 1)
        self.table.attach(self.hscrollbar, 0, 1, 1, 2, 4, 4)
        self.table.attach(self.vscrollbar, 1, 2, 0, 1, 4, 4)
        self.table.show_all()

        # Sandbox.
        self.sandbox = Sandbox(self)
        self.zoom_blocked = False

        # Head up display.
        self.hud = Hud(self)

        # Init redraw timing limits.
        self.obscured = [0] * 4
        self.obscured_time = None

        # Perform to display.
        self.redraw_all()


    def allocate_cb(self, widget, event):

        area = (event.x, event.y, event.width, event.height)
        if area == self.last_allocation_area: return
        self.last_allocation_area = area

        self.sandbox.redraw_all()


    def layout_reverse(self):
        """Reverse the layout children order, it is a way to keep the hud items
        over the sandbox despite the lack of a z-index system in the layout and
        fixed gtk widgets."""

        childrens = self.layout.get_children()
        for children in reversed(childrens):
            x = self.layout.child_get_property(children, 'x')
            y = self.layout.child_get_property(children, 'y')
            self.layout.remove(children)
            self.layout.put(children, x, y)


    def enter_cb(self, widget, event):
        """To do when the user moves the mouse into the eventbox.
        @widget: Root widget.
        @event: Emited event object."""

        self.hud.create_cursor()


    def leave_cb(self, widget, event):
        """To do when the user moves the mouse out of the eventbox.
        @widget: Root widget.
        @event: Emited event object."""

        #self.hud.remove_cursor()           # The eventbox emit the leave event
        pass                                # when the user click it, WTH!


    def key_cb(self, widget, event):
        """To do when the user press a key.
        @widget: Root widget.
        @event: Emited event object."""

        tool = main.plugins.activetool
        if not tool: return
        catched = tool.key_press(event.keyval)
        return catched


    def button_cb(self, widget, event):
        """To do when the user click a mouse button over the eventbox.
        @widget: Root widget.
        @event: Emited event object."""

        self.pressed_button = event.button
        x, y = self.sandbox.recoordinate(event.x, event.y)

        tool = main.plugins.activetool
        if not tool: return

        if self.pressed_button == 1:
            tool.button_primary(x, y, int(event.x), int(event.y))

        elif self.pressed_button == 3:
            tool.button_secondary(x, y, int(event.x), int(event.y))

        elif self.pressed_button == 2:
            self.scroll_xroot = event.x
            self.scroll_yroot = event.y
            self.hud.hide_cursor()
            main.gui.cursor.set_from_name('hand-closed')


    def motion_cb(self, widget, event):
        """To do when the user move the mouse over the eventbox.
        @widget: Root widget.
        @event: Emited event object."""

        x, y = self.sandbox.recoordinate(event.x, event.y)

        if (x, y) == self.last_motion_coordinates: return
        else: self.last_motion_coordinates = (x, y)

        tool = main.plugins.activetool
        if not tool: return

        if self.pressed_button == 1:
            tool.motion_primary(x, y, int(event.x), int(event.y))

        elif self.pressed_button == 3:
            tool.motion_secondary(x, y, int(event.x), int(event.y))

        elif self.pressed_button == 2:
            self.handscroll(event.x, event.y)

        else:
            tool.motion_over(x, y, int(event.x), int(event.y))
            main.gui.statusbar.update(x, y)

        self.hud.move_cursor(x, y)
        self.hud.dump_cursor()


    def release_cb(self, widget, event):
        """To do when the user release a mouse button.
        @widget: Root widget.
        @event: Emited event object."""

        tool = main.plugins.activetool
        if not tool: return

        if self.pressed_button == 1: tool.release_primary()
        elif self.pressed_button == 2: main.gui.cursor.set_default()
        elif self.pressed_button == 3: tool.release_secondary()

        self.pressed_button = 0
        self.hud.show_cursor()


    def handscroll(self, x, y):
        """Perform a freehand scroll in relation to the click root position.
        @x: The motion coordinate in x axis.
        @y: The motion coordinate in y axis."""

        xrel = x - self.scroll_xroot
        yrel = y - self.scroll_yroot
        self.scroll_xroot = x
        self.scroll_yroot = y
        self.hadjustment.set_value(self.hadjustment.value - xrel)
        self.vadjustment.set_value(self.vadjustment.value - yrel)


    def zoom_cb(self, widget, event):
        """To do when the user uses the mouse scroll over the eventbox.
        @widget: Root widget.
        @event: Emited event object."""

        if self.zoom_blocked: return
        else: self.zoom_blocked = True

        # Get coordinates.
        x = int(event.x)
        y = int(event.y)

        # Set pointer center.
        re_x, re_y = self.sandbox.recoordinate(x, y)
        sandbox_width, sandbox_height = self.sandbox.get_alloc()
        center = [re_x, re_y]

        # Set pointer gap from center.
        gap_x = (x - (sandbox_width / 2))
        gap_y = (y - (sandbox_height / 2))
        gap = [gap_x, gap_y]

        # Allowed zoom levels.
        multipliers = [1, 1.5, 2, 3, 4, 5, 6, 7, 8]
        multipliers += [10, 12, 14, 16, 20, 24, 28, 32]
        levels = [1.0 / x for x in reversed(multipliers)]
        levels += [float(x) for x in multipliers[1:]]
        level = levels.index(self.sandbox.factor)

        # Change zoom factor.
        if event.direction == gtk.gdk.SCROLL_UP:
            if level == len(levels)-1:
                self.zoom_blocked = False
                return
            self.sandbox.factor = levels[level+1]
        if event.direction == gtk.gdk.SCROLL_DOWN:
            if level == 0:
                self.zoom_blocked = False
                return
            self.sandbox.factor = levels[level-1]

        # Set interpolation algoritm.
        if self.sandbox.factor > 1: self.interpolation = gtk.gdk.INTERP_NEAREST
        else: self.interpolation = gtk.gdk.INTERP_NEAREST

        # Fill background.
        self.sandbox.pixbuf.fill(0x00000000)

        # Apply new zoom.
        main.gui.statusbar.update(*center)
        self.sandbox.redraw_all(center, gap)

        # Refresh hud.
        self.hud.create_cursor()
        self.hud.move_cursor(*center)
        self.hud.dump_cursor()
        self.hud.set_area(None)
        self.hud.dump()

        # Unblock zoom change.
        self.zoom_blocked = False


    def redraw(self, x, y, width, height, propagate=True, timing=False):
        """Redraw an outdated area in the displayed image.
        @x: The x coordinate of upper-left corner of rectangle.
        @y: The y coordinate of upper-left corner of rectangle.
        @width: The width of rectangle.
        @height: The height of rectangle.
        @propagate: Boolean to redraw or not the related sandbox area.
        @timing: Boolean to use or not the redraw timing system."""

        # Use the timing system.
        if timing:

            # Update obscure limits.
            obs = self.obscured
            if not obs[0] or x < obs[0]: obs[0] = x
            if not obs[1] or y < obs[1]: obs[1] = y
            if not obs[2] or x+width > obs[2]: obs[2] = x+width
            if not obs[3] or y+height > obs[3]: obs[3] = y+height
            if not self.obscured_time: self.obscured_time = time.time()

            # Abort redraw if there are more redraws in the stack and
            # the last redraw is too close.
            if gtk.events_pending():
                if time.time() - self.obscured_time < 0.04:
                    return

            # Overwrite redraw area with obscure limits.
            x = self.obscured[0]
            y = self.obscured[1]
            width = self.obscured[2] - self.obscured[0]
            height = self.obscured[3] - self.obscured[1]

        # Clear area with black and transparent pixels.
        core.clear(
            self.document.pointer,
            self.document.width,
            self.document.height,
            x,
            y,
            width,
            height)

        # Draw prelower layer.
        prelower = self.document.layers.prelower
        prelower.composite(1, self.document, 0, 0, x, y, width, height)

        # Avoid if there is no active layer.
        if self.document.layers.active:

            # Draw active (middle) layer.
            self.document.layers.active.composite(
                1,
                self.document,
                self.document.layers.active.xpos,
                self.document.layers.active.ypos,
                x,
                y,
                width,
                height)

            # Draw preupper layer.
            preupper = self.document.layers.preupper
            preupper.composite(1, self.document, 0, 0, x, y, width, height)

        # Progagate redraw to sandbox.
        if propagate:
            if hasattr(self.sandbox, 'pixbuf'):
                self.sandbox.redraw(x, y, width, height)

        # Reset redraw timing limits.
        if timing:
            self.obscured = [0] * 4
            self.obscured_time = None


    def redraw_all(self, propagate=True):
        """Redraw the displayed image completely.
        @propagate: Boolean to redraw or not the related sandbox area."""

        self.redraw(0, 0, self.document.width, self.document.height, propagate)


    def redraw_step(self, x, y, width, height, recursion=True):
        """Redraw an outdated area in the displayed image step by step.
        @x: The x coordinate of upper-left corner of rectangle.
        @y: The y coordinate of upper-left corner of rectangle.
        @width: The width of rectangle.
        @height: The height of rectangle."""

        # Step width and height.
        step_w = 250
        step_h = 160

        # Calc needed steps to redraw the requested zone.
        steps_in_x = width / step_w
        steps_in_y = height / step_h
        if width % step_w: steps_in_x += 1
        if height % step_h: steps_in_y += 1

        # Set redraw timestamp.
        thisredraw = time.time()
        self.lastredraw = thisredraw

        # Redraw step by step, stop if there are new redraws pending.
        for step_y in range(steps_in_y):
            for step_x in range(steps_in_x):
                if gtk.events_pending(): gtk.main_iteration()
                if thisredraw != self.lastredraw: return
                self.redraw(
                    x + (step_x * step_w),
                    y + (step_y * step_h),
                    step_w,
                    step_h)

        # Redraw all to clean artifacts, this only will be executed if the
        # previous loop ends completely (there is no more event pendings).
        if recursion: self.redraw_all_step(False)


    def redraw_all_step(self, recursion=True):
        """Redraw the displayed image completely step by step."""

        self.redraw_step(
            0,
            0,
            self.document.width,
            self.document.height,
            recursion)
