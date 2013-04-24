#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import re
import gtk


class Shortcuts(object):
    """The keyboard shortcuts manager."""

    def __init__(self):
        """Create the shortcuts manager instance."""

        main.log.info('loading shortcuts')

        self.childs = {}
        self.load_from_config()


    def load_from_config(self):
        """Load all shortcut entries from config and store it as Shortcut
        instances in items dict."""

        section = 'shortcuts'
        shortcuts = main.config.options(section)
        for shortcut in shortcuts:
            accel = main.config.get(section, shortcut)
            (key, mask) = gtk.accelerator_parse(accel)
            callback = self.callback_decode(shortcut)
            self.childs[shortcut] = Shortcut(hex(key), mask, callback)


    def save_to_config(self):

        for (name, shortcut) in self.childs.items():

            mask = int(shortcut.mask)
            mask_string = ''

            if mask // 8:
                mask_string += '<Alt>'
                mask -= 8
            if mask // 4:
                mask_string += '<Control>'
                mask -= 4
            if mask // 1:
                mask_string += '<Shift>'
                mask -= 1

            mask_string += shortcut.key

            #### TODO: Encode callback and send to config.
            #value = '%s %s' % (mask_string, plugin)
            #main.config.set('shortcuts', name, value)


    def callback_decode(self, callback):
        """Get a shortcut callback in config format and return it as real cb.
        @callback: Shortcut callback string in 'type:name' format.
        =return: Real callback function."""

        (cb_type, cb_name) = re.search('(.*?)\.(.*?)$', callback).groups()

        if cb_type == 'plugin':
            cb = main.plugins.childs[cb_name].callback

        if cb_type == 'layer':
            if cb_name == 'new':
                cb = lambda: main.documents.active.layers.append_blank()
            if cb_name == 'duplicate':
                cb = lambda: main.documents.active.layers.duplicate_active()
            if cb_name == 'up':
                cb = lambda: main.documents.active.layers.swap_up_active()
            if cb_name == 'down':
                cb = lambda: main.documents.active.layers.swap_down_active()
            if cb_name == 'remove':
                cb = lambda: main.documents.active.layers.remove_active()

        return cb


    def push(self):
        """Update (really create each time) the GTK window shortcuts list from
        stored shortcut instances."""

        self.group = gtk.AccelGroup()
        main.gui.window.add_accel_group(main.shortcuts.group)

        for shortcut in self.childs.values():
            self.group.connect_group(
                int(shortcut.key, 16),
                shortcut.mask,
                0,
                lambda w, x, y, z, s=shortcut: s.callback())


class Shortcut(object):
    """Smallest shortcut object to store into dict and able future tracking."""

    def __init__(self, key, mask, callback):
        """Create the shortcut instance."""

        self.key = key
        self.mask = mask
        self.callback = callback
