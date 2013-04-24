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
from nathive.lib import convert
from nathive.gui.multiwidget import *
from nathive.gui import utils as gutils


class New(PluginDialog):
    """The new document dialog."""

    def __init__(self):

        # Subclass it.
        PluginDialog.__init__(self)

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Common attributes.
        self.name = 'new'
        self.author = 'nathive-dev'
        self.menu = 'file'
        self.label = _('New')
        self.icon = 'gtk-new'

        self.default()
        main.config.push_to_plugin(self)


    def default(self):
        """Reset plugin attributes to their default values."""

        self.unit = 0
        self.width = 400
        self.height = 300
        self.dpi = 150


    def update(self):

        self.mw_unit.set_value(self.unit)
        self.mw_width.set_value(self.width)
        self.mw_height.set_value(self.height)
        self.mw_dpi.set_value(self.dpi)


    def callback(self):
        """To do when the plugin is called."""

        # Create dialog.
        self.dialog = gtk.Dialog(self.label)
        self.dialog.set_modal(True)
        self.dialog.set_resizable(False)
        self.box = gtk.VBox(False, 5)
        self.box.set_border_width(5)
        self.dialog.vbox.pack_start(self.box)

        # Units selector.
        self.mw_unit = MultiWidgetCombo(
            self.box,
            _('Units'),
            [_('Pixels'), _('Centimeters'), _('Inches')],
            self.unit,
            lambda x: self.change_unit(x))

        # Width spin.
        self.mw_width = MultiWidgetSpin(
            self.box,
            '',
            False,
            0,
            0,
            0,
            lambda x: setattr(self, 'width', x))

        # Height spin.
        self.mw_height = MultiWidgetSpin(
            self.box,
            '',
            False,
            0,
            0,
            0,
            lambda x: setattr(self, 'height', x))

        # Resolution spin.
        self.mw_dpi = MultiWidgetSpin(
            self.box,
            '%s (dpi)' % _('Resolution'),
            False,
            0,
            10000,
            self.dpi,
            lambda x: setattr(self, 'dpi', x))

        # Loader.
        self.loader = MultiWidgetPresets(self, self.box)

        # Update values.
        self.change_unit(self.unit)

        # Connect.
        self.dialog.connect('response', self.response)
        self.dialog.connect('destroy', lambda x: self.quit())

        # Buttons (auto-connected by response).
        self.dialog.add_button('gtk-cancel', 1)
        self.dialog.add_button('gtk-ok', 2)

        # Show.
        self.dialog.show_all()


    def change_unit(self, unit_index):
        """Update values when the unit is changed.
        @unit_index: Index of selected unit."""

        # Set previous and actual unit, alias dpi.
        unit_prev = self.unit
        self.unit = unit_index
        dpi = self.dpi

        # Set the converter function.
        converter = None
        if unit_prev == 0:
            if self.unit == 1: converter = lambda x,y=dpi: convert.px_cm(x, y)
            if self.unit == 2: converter = lambda x,y=dpi: convert.px_in(x, y)
        if unit_prev == 1:
            if self.unit == 0: converter = lambda x,y=dpi: convert.cm_px(x, y)
            if self.unit == 2: converter = lambda x,y=dpi: convert.cm_in(x, y)
        if unit_prev == 2:
            if self.unit == 0: converter = lambda x,y=dpi: convert.in_px(x, y)
            if self.unit == 1: converter = lambda x,y=dpi: convert.in_cm(x, y)

        # Apply the converter.
        if converter:
            self.width = converter(self.width)
            self.height = converter(self.height)

        # Define specials for multiwidget.
        if self.unit == 0:
            info = 'px'
            digits = 0
            upper = 100000
            step = 1
        if self.unit == 1:
            info = 'cm'
            digits = 2
            upper = 999.99
            step = 0.01
        if self.unit == 2:
            info = 'in'
            digits = 2
            upper = 999.99
            step = 0.01

        # Set values and specials to multiwidget.
        self.mw_width.adjustment.upper = upper
        self.mw_height.adjustment.upper = upper
        self.mw_width.adjustment.step_increment = step
        self.mw_height.adjustment.step_increment = step
        self.mw_width.set_value(self.width)
        self.mw_height.set_value(self.height)
        self.mw_width.label.set_text('%s (%s):' % (_('Width'), info))
        self.mw_height.label.set_text('%s (%s):' % (_('Height'), info))
        self.mw_width.spin.set_digits(digits)
        self.mw_height.spin.set_digits(digits)


    def response(self, widget, response):
        """Response (buttons) callbacks.
        @widget: Call widget.
        @response: Response int."""

        if response == 1: self.quit()
        if response == 2: self.new()


    def new(self):
        """Create the new document with selected dimensions."""

        # Alias to get cleanest code after.
        unit = self.unit
        width = self.width
        height = self.height
        dpi = self.dpi
        cm_px = convert.cm_px
        in_px = convert.in_px

        # Convert centimeters/inches to pixels.
        if unit != 0:
            width = cm_px(width, dpi) if unit == 1 else in_px(width, dpi)
            height = cm_px(height, dpi) if unit == 1 else in_px(height, dpi)

        # Create a new document and quit.
        main.documents.new_blank(int(width), int(height))
        self.quit()


    def quit(self):
        """To do when the dialog is closed."""

        self.dialog.hide()
        self.dialog.destroy()
