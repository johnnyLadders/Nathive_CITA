#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import gtk

from nathive.lib.plugin import *


class Open(PluginDialog):

    def __init__(self):
        """To do when the plugin is loaded at program start."""

        # Subclass it.
        PluginDialog.__init__(self)

        # Common attributes.
        self.name = 'open'
        self.author = 'nathive-dev'
        self.menu = 'file'
        self.label = _('Open')
        self.icon = 'gtk-open'

        # Setting up the plugin.
        self.whitelist = ['.ora', '.png', '.jpg', '.jpeg', '.gif']
        self.default()
        main.config.push_to_plugin(self)


    def default(self):
        """Reset plugin attributes to their default values."""

        self.folder = main.home


    def callback(self):
        """To do when the plugin is called."""

        # Create dialog.
        self.dialog = gtk.FileChooserDialog(self.label, None, 0, None, None)
        self.dialog.set_modal(True)
        self.dialog.set_current_folder(self.folder)

        # Preview widget.
        preview = gtk.Frame(_('Preview'))
        self.preview_box = gtk.VBox(False, 5)
        self.preview_box.set_size_request(150, -1)
        self.preview_box.set_border_width(10)
        preview.add(self.preview_box)
        self.preview_image = gtk.Image()
        self.preview_label = gtk.Label()
        self.preview_box.pack_start(self.preview_image, False)
        self.preview_box.pack_start(self.preview_label, False)
        preview.show_all()
        self.dialog.set_preview_widget(preview)
        self.dialog.set_use_preview_label(False)

        # Connect.
        self.dialog.connect('file-activated', self.select)
        self.dialog.connect('current-folder-changed', lambda x: self.infolder())
        self.dialog.connect('selection-changed', lambda x: self.previewer())
        self.dialog.connect('response', self.response)
        self.dialog.connect('destroy', lambda x: self.quit())

        # Buttons (auto-connected by response).
        self.dialog.add_button('gtk-cancel', 2)
        self.dialog.add_button('gtk-open', 1)

        # Show.
        self.dialog.show_all()


    def response(self, widget, response):
        """Response (buttons) callbacks.
        @widget: Call widget.
        @response: Response int."""

        if response == 1: self.select(widget)
        if response == 2: self.quit()


    def select(self, widget):
        """To do when the user select a file.
        @widget: Call widget."""

        # Get path from chooser.
        path = widget.get_filename()
        name, ext = os.path.splitext(path)
        ext = ext.lower()

        # If path is image, open path and hide chooser.
        if ext in self.whitelist:
            main.documents.new_from_path(path)
            self.quit()


    def infolder(self):
        """Callback for update the folder attribute."""

        self.folder = self.dialog.get_current_folder()
        previews = self.preview_box.get_children()
        [x.hide() for x in previews]


    def previewer(self):
        """Callback for update the preview image."""

        # Get path and abort if is empty.
        path = self.dialog.get_preview_filename()
        if not path: return

        # Get the list of preview subwidgets.
        previews = self.preview_box.get_children()

        # Get extension and abort if is not allowed.
        (root, ext) = os.path.splitext(path)
        whitelist = self.whitelist[:]                # Temporal patch while ora
        whitelist.remove('.ora')                     # preview does not work.
        if ext.lower() not in whitelist:
            [x.hide() for x in previews]
            return

        # Force preview subwidgets to show.
        [x.show() for x in previews]

        # Get and display preview image.
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(path, 128, 128)
        self.preview_image.set_from_pixbuf(pixbuf)

        # Get and display preview dimensions.
        (info, width, height) = gtk.gdk.pixbuf_get_file_info(path)
        self.preview_label.set_label('%s x %s' % (width, height))


    def quit(self):
        """To do when the plugin is closed."""

        main.config.push_from_plugin(self)
        self.dialog.hide()
        self.dialog.destroy()
