#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import gc
import sys
import gtk
import pango

from nathive.lib.plugin import *
from nathive.gui import utils as gutils


class Console(PluginDialog):

    def __init__(self):
        """To do when the plugin is loaded at program start."""

        # Subclass it.
        PluginDialog.__init__(self)

        # Common attributes.
        self.name = 'console'
        self.author = 'nathive-dev'
        self.menu = 'help'
        self.label = _('Console')
        self.icon = 'terminal'

        # Own attributes.
        self.locals = None
        self.history = ['']
        self.history_pos = 0

        # Set history file path.
        folder = os.path.join(main.cfgpath, 'console')
        path = os.path.join(folder, 'history')
        self.history_path = path

        # Load history from file.
        self.load_history()


    def callback(self):
        """To do when the plugin is called."""

        # Redirect the output buffer.
        self.stdout = sys.stdout
        sys.stdout = self

        # Create dialog.
        self.dialog = gtk.Dialog(_('Console'))
        self.dialog.set_size_request(425, 325)

        # Create box for dialog except response buttons.
        self.box = gtk.VBox()
        self.box.set_border_width(5)
        self.dialog.vbox.pack_start(self.box)

        # Create the textview and related.
        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        self.adjustment = self.scroll.get_vadjustment()
        self.view = gtk.TextView()
        self.view.set_editable(False)
        self.view.set_cursor_visible(False)
        self.view.set_left_margin(8)
        self.view.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        self.buffer = self.view.get_buffer()
        self.scroll.add(self.view)
        self.box.pack_start(self.scroll)

        # Set the textview style.
        font = pango.FontDescription("DejaVu Sans Mono 9")
        self.view.modify_font(font)
        self.view.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color('#000'))
        self.view.modify_text(gtk.STATE_NORMAL, gtk.gdk.Color('#fff'))

        # Throw the welcome message.
        self.buffer.set_text(
            'This is a Python pseudo-interpreter that allow you runtime '
            'introspection into Nathive, enjoy it!\n')
        self.evaluate('dir(main)')

        # Add margin between textview and input entry.
        gutils.margin(self.box, 4)

        # Create the input entry.
        self.input = gtk.Entry()
        focus = self.input.grab_focus
        self.input.connect('key-press-event', self.keypress)
        self.input.connect('focus-out-event', lambda x,y: focus())
        self.box.pack_start(self.input, False, False)
        focus()

        # Connect.
        self.dialog.connect('response', self.response)
        self.dialog.connect('destroy', lambda x: self.quit())

        # Buttons (auto-connected by response).
        self.dialog.add_button('gtk-close', 1)

        # Show.
        self.dialog.show_all()


    def keypress(self, widget, event):
        """Callback funtion when a key is pressed in the input entry.
        @widget: A gtk.Textview.
        @event: A gtk.Event."""

        # If keyboard enter (normal or numpad) is pressed.
        if event.keyval == 65293 or event.keyval == 65421:
            command = widget.get_text()
            self.evaluate(command)
            widget.set_text('')
            if command:
                if command == 'clear' or command == 'reset':
                    self.buffer.set_text('')
                else:
                    if command in self.history: self.history.remove(command)
                self.history.insert(1, command)
            self.history_pos = 0

        # If keyboard up is pressed
        if event.keyval == 65362:
            self.history_pos += 1
            length = len(self.history) - 1
            if self.history_pos > length: self.history_pos = length
            widget.set_text(self.history[self.history_pos])

        # If keyboard down is pressed
        if event.keyval == 65364:
            self.history_pos -= 1
            if self.history_pos <= 0: self.history_pos = 0
            widget.set_text(self.history[self.history_pos])


    def evaluate(self, command):
        """Try to evaluate or execute the command, preserves the locals to allow
        user assigned variables.
        @command: A command to evaluate."""

        # Load old locals to keep user defined variables.
        if self.locals:
            for (name, value) in self.locals.items():
                locals()[name] = value

        # Output command like python interpreter.
        self.write_in_buffer('>>> %s' % command)

        # First try to eval, if not, try to exec, if not, throw error.
        try:
            retrieve = eval(command)
            self.write_in_buffer(retrieve)
        except:
            try: exec command
            except Exception, error: self.write_in_buffer(error)

        # Save old locals to keep user defined variables.
        self.locals = locals()
        self.locals.pop('self')
        self.locals['revid'] = self.revid


    def write_in_buffer(self, message):
        """Append a message to the textview.
        @message: A message string."""

        message = '\n%s' % str(message)
        enditer = self.buffer.get_end_iter
        self.buffer.insert(enditer(), message)
        mark = self.buffer.create_mark('mark', enditer())
        self.view.scroll_mark_onscreen(mark)


    def write(self, message):
        """Hook to print in both outputs, standart and buffer.
        @message: A message string."""

        self.stdout.write(message)
        if message != '\n': self.write_in_buffer(message)


    def save_history(self):
        """Save history in filesystem."""

        # Format history string,
        history = self.history[:]
        history.reverse()
        if len(history) > 100: history = history[:-100]
        history = '\n'.join(history)

        # Save to disk.
        head, tail = os.path.split(self.history_path)
        if not os.path.exists(head): os.makedirs(head)
        fileobj = open(self.history_path, 'w')
        fileobj.write(history)
        fileobj.close()


    def load_history(self):
        """Load history from filesystem."""

        if not os.path.exists(self.history_path): return
        history = open(self.history_path).read().split('\n')
        history.reverse()
        self.history = history


    def revid(self, addr):
        """Reverse id search, return the object for the given address, it's
        callable directly in console for debugging purposes.
        @addr: Memory address as int or hex."""

        for objectx in gc.get_objects():
            if id(objectx) == addr:
                return objectx


    def response(self, widget, response):
        """Response (buttons) callbacks.
        @widget: Call widget.
        @response: Response int."""

        if response == 1: self.quit()


    def quit(self):
        """To do when the dialog is closed."""

        sys.stdout = self.stdout
        self.save_history()
        self.history_pos = 0
        self.dialog.hide()
        self.dialog.destroy()
