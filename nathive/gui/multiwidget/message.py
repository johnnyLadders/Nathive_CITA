#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk


class MultiWidgetMessage(object):
    """A simplest way to show a gtk.MessageDialog."""

    def __init__(self, kind, message, submessage, buttons):
        """Create and show the message dialog.
        @kind: The type of message, "info|warning|question|error" string.
        @message: The message string to display.
        @buttons: A list of 2-tuple with button strings and callbacks."""

        if kind == 'info': kind = gtk.MESSAGE_INFO
        elif kind == 'warning': kind = gtk.MESSAGE_WARNING
        elif kind == 'question': kind = gtk.MESSAGE_QUESTION
        elif kind == 'error': kind = gtk.MESSAGE_ERROR
        else: raise ValueError(
            'First argument must be "info|warning|question|error" string')

        dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL,
            kind,
            gtk.BUTTONS_NONE,
            None)

        format = '<span size="large" weight="bold">%s</span>'
        dialog.set_markup(format % message)
        if submessage: dialog.format_secondary_text(submessage)

        dialog.connect('response', self.response, buttons)

        button_response = len(buttons)
        for button in buttons:
            (stock, callback) = button
            dialog.add_button(stock, button_response)
            button_response -= 1

        dialog.show_all()


    def response(self, widget, response, buttons):
        """Response (buttons) callbacks for the overwrite dialog.
        @widget: Call widget.
        @response: Response int.
        @buttons: A list of 2-tuple with button strings and callbacks."""

        button_response = len(buttons)
        for button in buttons:
            (stock, callback) = button
            if response == button_response: callback()
            button_response -= 1

        widget.destroy()
