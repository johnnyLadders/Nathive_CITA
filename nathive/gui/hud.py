#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import math
import gtk
import cairo
import StringIO


class Hud(object):
    """Class for floating visual data like layer borders or crop areas.
    ⌥: Main > Documents > {n}Document > Canvas > Hud."""

    def __init__(self, canvas):
        """Hud object initialization.
        @canvas: The parent canvas object."""

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Store canvas to use in methods.
        self.canvas = canvas

        # Attributes.
        self.childs = []
        self.cursor = None
        self.cursor_shape = None
        self.cursor_size = None
        self.cursor_outdated = False
        self.last_cursor = None
        self.area = None
        self.area_dimensions = [0] * 4
        self.area_sandboxed = False


    def get_item(self, image):
        """Returns the hud item object for given image.
        @image: A gtk image widget.
        =return: The hud item object that store the given image."""

        for item in self.childs:
            if item.image == image:
                return item


    def add(self, image, x=0, y=0, offset_x=0, offset_y=0):
        """Create and append a basic hud item object with the given properties.
        @image: A gtk image widget.
        @x: Coordinate in x axis.
        @y: Coordinate in y axis.
        @offset_x: Correction amount in x axis.
        @offset_y: Correction amount in y axis.
        =return: The created hud item object."""

        item = HudItem(image, x, y, offset_x, offset_y)
        self.childs.append(item)
        return item


    def add_from_name(self, name, x=0, y=0, offset_x=0, offset_y=0):
        """Create and append a basic hud item object using the given filename.
        @name: A file name with extension to load from the img folder.
        @x: Coordinate in x axis.
        @y: Coordinate in y axis.
        @offset_x: Correction amount in x axis.
        @offset_y: Correction amount in y axis.
        =return: The created hud item object."""

        path = os.path.join(main.imgpath, name)
        image = gtk.image_new_from_file(path)
        item = self.add(image, x, y, offset_x, offset_y)
        return item


    def remove(self, item):
        """Remove the given hud item object.
        @item: Am hud item object."""

        if item not in self.childs: return
        item.image.destroy()
        self.childs.remove(item)


    def set_cursor(self, shape, size):
        """Configure the hud cursor properties to create it.
        @shape: A string with the shape name, currently 'square' or 'circle'.
        @size: Cursor real size in pixels."""

        self.cursor_shape = shape
        self.cursor_size = size


    def move_cursor(self, x, y):
        """Move the hud cursor to the given coordinates.
        @x: Coordinate in x axis.
        @y: Coordinate in y axis."""

        if not self.cursor: return
        if self.cursor_outdated: self.create_cursor()
        self.cursor.x, self.cursor.y = self.canvas.sandbox.uncoordinate(x, y)


    def hide_cursor(self):
        """Hide hud cursor temporally, like in handscroll."""

        if not self.cursor: return
        self.cursor.image.hide()
        self.cursor.set_display(False)


    def show_cursor(self):
        """Show the hud cursor again after a temporally hide."""

        if not self.cursor: return
        self.cursor.set_display(True)


    def remove_cursor(self, totally=True):
        """Remove the current hud cursor, if the totally argument is given as
        False the hud cursor will be still configurated with the old
        properties and ready to be created again."""

        if not self.cursor and not self.cursor_size: return
        if hasattr(self.cursor, 'image'): self.cursor.image.destroy()
        self.cursor = None
        if totally:
            self.cursor_shape = None
            self.cursor_size = None
            self.last_cursor = None


    def create_cursor(self):
        """Create the hud cursor image (cairo based), after this the hud cursor
        is ready to be dumped."""

        # Stop if the hud cursor is not configured.
        if not self.cursor_shape or not self.cursor_size: return

        # Calc the size at sandbox scale.
        size = int(self.cursor_size * self.canvas.sandbox.factor)

        # Avoid to create a new cursor if the old is equal.
        if (self.cursor_shape, size) == self.last_cursor: return
        self.last_cursor = (self.cursor_shape, size)

        # Remove old cursor, abort if size is bigger than the sandbox width.
        self.remove_cursor(False)
        if size > self.canvas.sandbox.get_alloc()[0]: return

        # Configure cairo.
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, size+2, size+2)
        context = cairo.Context(surface)

        # Draw requested shape in the cairo context.
        if self.cursor_shape == 'circle':
            self.draw_circle(context, size)
        elif self.cursor_shape == 'square':
            self.draw_rectangle(context, size, size)

        # Get pixbuf from cairo surface.
        pixbuf = gtk.gdk.pixbuf_new_from_data(
            str(surface.get_data()),                 # Due to cairo uses
            0,                                       # premultiplied ARGB and
            True,                                    # pixbuf uses RGBA we cant
            8,                                       # do a direct conversion
            size+2,                                  # with antialing enabled.
            size+2,
            surface.get_stride())

        # Get image from pixbuf, set as new hud cursor.
        image = gtk.image_new_from_pixbuf(pixbuf)
        image.show()

        # Calc hud cursor position, apply corrector to fit grid.
        position = -(size / 2) - 1
        if self.cursor_size % 2:
            position += int(0.5 * self.canvas.sandbox.factor)

        # Create the cursor object.
        self.cursor = HudItem(image, 0, 0, position, position)
        self.cursor.set_display(True)
        self.cursor_outdated = False


    def set_area(self, area):
        """Create the hud area image with the given area dimensions, after this
        the hud is ready to be dumped.
        @area: Dimension rectangle as 4-item list."""

        # If not area given try to use the last known area or abort.
        if not area:
            if not self.area: return
            area = self.area_dimensions

        # Store the dimensions to allow refresh calls.
        self.area_dimensions = area

        # Unpack dimensions.
        x = area[0]
        y = area[1]
        width = area[2]
        height = area[3]

        # Turn width and height to sandbox scope.
        factor = self.canvas.sandbox.factor
        width = int(width * factor)
        height = int(height * factor)

        # Get sandbox dimensions.
        sandbox_width, sandbox_height = self.canvas.sandbox.get_alloc()
        sandbox_x, sandbox_y = self.canvas.sandbox.get_adjustment_values()

        # Improve performance sandboxing areas bigger than the sandbox itself,
        # ix like booleans defines if the initial or final coordinates are
        # visible into the current sandbox.
        self.area_sandboxed = False
        overset_x = 0
        overset_y = 0
        if width > sandbox_width:
            self.area_sandboxed = True
            diff_ix = sandbox_x - int(x * factor)
            diff_fx = (sandbox_x + sandbox_width) - (int(x * factor) + width)
            ix = True if diff_ix < 0 else False
            fx = True if diff_fx > 0 else False
            width = sandbox_width
            x = sandbox_x / factor
            if ix and not fx: overset_x = -diff_ix
            if not ix and fx: overset_x = -diff_fx
            if not ix and not fx:
                overset_x = -5
                width += 10
        if height > sandbox_height:
            self.area_sandboxed = True
            diff_iy = sandbox_y - int(y * factor)
            diff_fy = (sandbox_y + sandbox_height) - (int(y * factor) + height)
            iy = True if diff_iy < 0 else False
            fy = True if diff_fy > 0 else False
            height = sandbox_height
            y = sandbox_y / factor
            if iy and not fy: overset_y = -diff_iy
            if not iy and fy: overset_y = -diff_fy
            if not iy and not fy:
                overset_y = -5
                height += 10

        # Configure cairo.
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width+2, height+2)
        context = cairo.Context(surface)

        # Draw rectangle in cairo context.
        self.draw_rectangle(context, width, height, overset_x, overset_y)

        # Get pixbuf from cairo surface.
        pixbuf = gtk.gdk.pixbuf_new_from_data(
            str(surface.get_data()),
            0,
            True,
            8,
            width+2,
            height+2,
            surface.get_stride())

        # Get image from pixbuf.
        image = gtk.image_new_from_pixbuf(pixbuf)
        image.show()

        # Set image as new hud item.
        if self.area: self.remove(self.area)
        self.area = self.add(image, x, y)
        self.area.set_display(True)


    def move_area(self, x, y):
        """Move the area to the given coordinates.
        @x: Coordinate in x axis.
        @y: Coordinate in y axis."""

        self.area_dimensions[0] = x
        self.area_dimensions[1] = y
        if not self.area_sandboxed: self.area.move(x, y)
        else: self.set_area(None)


    def remove_area(self):
        """Remove area hud item."""

        self.remove(self.area)
        self.area = None


    def draw_circle(self, context, size):
        """Draw a b&w circle in the given cairo context.
        @context: A pycairo context object.
        @size: Requested size for the circle in pixels."""

        context.set_antialias(cairo.ANTIALIAS_NONE)

        center = (size / 2) + 1
        context.translate(center, center)

        context.set_line_width(3)
        context.set_source_rgba(0, 0, 0, 0.25)
        context.arc(0, 0, size/2, 0, 2*math.pi)
        context.stroke()

        context.set_line_width(1)
        context.set_source_rgb(1, 1, 1)
        context.arc(0, 0, size/2, 0, 2*math.pi)
        context.stroke()


    def draw_rectangle(self, context, width, height, offset_x=0, offset_y=0):
        """Draw a b&w square in the given cairo context.
        @context: A pycairo context object.
        @width: Requested width for the square in pixels.
        @height: Requested height for the square in pixels.
        @offset_x: Initial deviation at x axis in pixels.
        @offset_y: Initial deviation at y axis in pixels."""

        ix = 1 + offset_x
        iy = 1 + offset_y
        fx = width + offset_x
        fy = height + offset_y

        context.set_antialias(cairo.ANTIALIAS_NONE)

        context.move_to(ix, iy)
        context.set_line_width(3)
        context.set_source_rgba(0, 0, 0, 0.25)
        context.line_to(fx, iy)
        context.line_to(fx, fy)
        context.line_to(ix, fy)
        context.line_to(ix, iy)
        context.close_path()
        context.stroke()

        context.move_to(ix, iy)
        context.set_line_width(1)
        context.set_source_rgb(1, 1, 1)
        context.line_to(fx, iy)
        context.line_to(fx, fy)
        context.line_to(ix, fy)
        context.line_to(ix, iy)
        context.close_path()
        context.stroke()


    def dump(self):
        """Dump each basic (tracked child) hud item to sandbox."""

        # For each tracked hud item.
        for item in self.childs:

            # Transform coordinates from real to sandbox.
            x, y = self.canvas.sandbox.uncoordinate(item.x, item.y)

            # Put or move hud items over the sandbox.
            if item.image not in self.canvas.layout.get_children():
                self.canvas.layout.put(
                    item.image,
                    x + item.offset_x,
                    y + item.offset_y)
            else:
                self.canvas.layout.move(
                    item.image,
                    x + item.offset_x,
                    y + item.offset_y)

            # Show or hide from display attribute.
            if item.display: item.image.show()
            else: item.image.hide()


    def dump_cursor(self):
        """Dump the hud cursor to sandbox."""

        # Return if there is no cursor.
        if not self.cursor: return
        if not self.cursor.display: return

        #if gtk.events_pending():                         # Better perform, but
            #gtk.main_iteration()                         # worse refresh rate.

        # Put or move hud cursor image.
        if self.cursor.image not in self.canvas.layout.get_children():
            self.canvas.layout.put(
                self.cursor.image,
                self.cursor.x + self.cursor.offset_x,
                self.cursor.y + self.cursor.offset_y)
        else:
            self.canvas.layout.move(
                self.cursor.image,
                self.cursor.x + self.cursor.offset_x,
                self.cursor.y + self.cursor.offset_y)

        # Force to show cursor image (needed after hide and show).
        self.cursor.image.show()


class HudItem(object):
    """Class for Hud child items, resulting objects are floatings gtk images
    with defined position and other attributes, can be tracked as hud childs or
    used as base for other purposes.
    ⌥: Main > Documents > *Document > Canvas > Hud > HudItem."""

    def __init__(self, image, x=0, y=0, offset_x=0, offset_y=0):
        """Hud item object initialization.
        @image: A gtk image widget.
        @x: Coordinate in x axis.
        @y: Coordinate in y axis.
        @offset_x: Correction amount in x axis.
        @offset_y: Correction amount in y axis."""

        self.image = image
        self.x = x
        self.y = y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.display = True


    def move(self, x, y):
        """Set hud item new coordinates.
        @x: Coordinate in x axis.
        @y: Coordinate in y axis."""

        self.x = x
        self.y = y


    def set_display(self, display):
        """Set the hud item display state, True to show, False to hide.
        until the dump process is called.
        @display: New display state as boolean."""

        self.display = display
