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
from nathive.lib.openraster import OpenRaster
from nathive.gui.multiwidget import *
from nathive.gui import utils as gutils


class Saveas(PluginDialog):

    def __init__(self):
        """To do when the plugin is loaded at program start."""

        # Subclass it.
        PluginDialog.__init__(self)

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Common attributes.
        self.name = 'saveas'
        self.author = 'nathive-dev'
        self.menu = 'file'
        self.label = _('Save as')
        self.icon = 'gtk-save-as'

        # Setting up the plugin.
        self.default()
        main.config.push_to_plugin(self)


    def default(self):
        """Reset plugin attributes to their default values."""

        self.folder = main.home
        self.format = 0
        self.quality = 90


    def callback(self):
        """To do when the plugin is called."""

        if not main.documents.active: return

        # Create dialog.
        self.dialog = gtk.FileChooserDialog(self.label, None, 1, None, None)
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

        # Search into the file chooser childrens and attach the format widget
        # to the name/location table.
        children = self.dialog.get_children()[0]
        children = children.get_children()[0]
        children = children.get_children()[0]
        children = children.get_children()[0]
        children = children.get_children()[0]
        table = children
        table.resize(2, 3)
        table.attach(self.format_widget(), 2, 3, 0, 2, 0)

        # Connect.
        self.dialog.connect('file-activated', lambda x: self.select())
        self.dialog.connect('current-folder-changed', lambda x: self.infolder())
        self.dialog.connect('selection-changed', lambda x: self.previewer())
        self.dialog.connect('response', self.response)
        self.dialog.connect('destroy', lambda x: self.quit())

        # Buttons (auto-connected by response).
        self.dialog.add_button('gtk-cancel', 2)
        self.dialog.add_button('gtk-save', 1)

        # Show.
        self.dialog.show_all()


    def response(self, widget, response):
        """Response (buttons) callbacks.
        @widget: Call widget.
        @response: Response int."""

        if response == 1: self.select()
        if response == 2: self.quit()


    def format_widget(self):

        # Format widget.
        frame = gtk.Frame()
        box = gtk.VBox(False, 2)
        box.set_border_width(8)
        frame.add(box)

        # Format label.
        self.format_label = gtk.Label()
        box.pack_start(self.format_label, False)

        # Format horizontal box.
        hbox = gtk.HBox(False, 2)
        box.pack_start(hbox, False)

        # Format combo.
        combo = gtk.combo_box_new_text()
        options = [_('Automatic'), 'OpenRaster', 'PNG', 'JPG']
        for option in options: combo.append_text(option)
        combo.set_active(self.format)
        combo.connect('changed', self.format_changed)
        hbox.pack_start(combo, False)

        # Quality spin.
        quality_adj = gtk.Adjustment(self.quality, 1, 100, 1, 1, 0)
        self.quality_spin = gtk.SpinButton(quality_adj)
        quality_adj.connect(
            'value-changed',
            lambda x: setattr(self, 'quality', x.get_value()))
        hbox.pack_start(self.quality_spin, False)

        frame.show_all()
        self.format_changed(combo)
        return frame


    def format_changed(self, combo):

        self.format = combo.get_active()
        if self.format == 3:
            markup = '<span size="small">%s / %s:</span>'
            self.format_label.set_markup(markup % (_('Format'), _('Quality')))
            self.quality_spin.show()
        else:
            markup = '<span size="small">%s:</span>'
            self.format_label.set_markup(markup % _('Format'))
            self.quality_spin.hide()


    def select(self):
        """To do when the user select a file."""

        # Get path, name, and extension.
        path = self.dialog.get_filename()
        (name, ext) = os.path.splitext(path)
        ext = ext.lower()

        # Init format tag and error flag.
        format = None
        error = False

        # If format is automatic.
        if self.format == 0:
            if not ext: format = 'ora'
            if ext == '.ora': format = 'ora'
            if ext == '.png': format = 'png'
            if ext == '.jpg' or ext == '.jpeg': format = 'jpg'

        # If format is openraster.
        if self.format == 1:
            if ext == '.ora' or not ext: format = 'ora'
            else:
                self.dismatch()
                error = True

        # If format is PNG.
        if self.format == 2:
            if ext == '.png' or not ext: format = 'png'
            else:
                self.dismatch()
                error = True

        # If format is JPG.
        if self.format == 3:
            if ext == '.jpg' or ext == '.jpeg' or not ext: format = 'jpg'
            else:
                self.dismatch()
                error = True

        # Stop here if error flag is on.
        if error: return

        # Append extension if path has not.
        if not ext: path = '%s.%s' % (path, format)

        # If file exists show overwrite dialog, else save directly.
        if os.path.exists(path): self.overwrite(path, format)
        else: self.save(path, format)


    def infolder(self):
        """Callback for update the folder attribute."""

        self.folder = self.dialog.get_current_folder()
        previews = self.preview_box.get_children()
        [x.hide() for x in previews]


    def previewer(self):
        """Callback for update the preview image."""

        # Formats allowed to be previewed.
        whitelist = ['.jpg', '.jpeg', '.png', '.gif', '.svg']

        # Get path and abort if is empty.
        path = self.dialog.get_preview_filename()
        if not path: return

        # Get the list of preview subwidgets.
        previews = self.preview_box.get_children()

        # Get extension and abort if is not allowed.
        (root, ext) = os.path.splitext(path)
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


    def overwrite(self, path, format):
        """The overwrite dialog.
        @path: Absolute path to save the file.
        @format: String containing the format."""

        message = _('«%s» already exists') % path.replace(main.home, '~')
        submessage = _('Overwrite will replace the old image with the new one.')

        buttons = [
            ('gtk-cancel', lambda:None),
            (_('Overwrite'), lambda: self.save(path, format))]

        MultiWidgetMessage('question', message, submessage, buttons)


    def dismatch(self):
        """Warning dialog when extension and format are not the same."""

        message = _('Extension is wrong')
        submessage = _('Change the format or file extension.')
        buttons = [('gtk-close', lambda:None)]

        MultiWidgetMessage('warning', message, submessage, buttons)


    def save(self, path, format):
        """Save the pixbuf to a file.
        @path: Absolute path to save the file.
        @format: String containing the format."""

        # Alias document.
        document = main.documents.active

        # Export document in requested format, pass quality in JPG format.
        quality = None
        if format == 'jpg': quality = self.quality
        document.export(path, format, quality)

        # Update and quit.
        document.set_path(path)
        document.set_mime_from_format(format)
        self.quit()


    def quit(self):
        """To do when the plugin is closed."""

        main.config.push_from_plugin(self)
        if hasattr(self, 'dialog'):
            self.dialog.hide()
            self.dialog.destroy()
