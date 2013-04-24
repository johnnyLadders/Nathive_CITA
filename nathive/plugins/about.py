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
from nathive.gui import utils as gutils


class About(PluginDialog):

    def __init__(self):

        # Subclass it.
        PluginDialog.__init__(self)

        # Common attributes.
        self.name = 'about'
        self.author = 'nathive-dev'
        self.menu = 'help'
        self.label = _('About')
        self.icon = 'gtk-about'


    def callback(self):
        """To do when the plugin is called."""

        # Create dialog.
        self.dialog = gtk.Dialog(self.label)
        self.dialog.set_modal(True)
        notebook = gtk.Notebook()
        notebook.set_border_width(5)
        self.dialog.vbox.pack_start(notebook)

        # About tab.
        about = gtk.VBox(False, 5)
        splash = gtk.image_new_from_file('%s/about.png' % main.imgpath)
        copyright = gtk.Label('Copyright © 2008-2010 Marcos Diaz Mencia')
        version_string = '%s %s (%s)' % (main.version, main.phase, main.level)
        version = gtk.Label(version_string)
        about.pack_start(splash)
        about.pack_start(copyright)
        about.pack_start(version)
        gutils.margin(about, 2)
        notebook.append_page(about, gtk.Label(_('About')))

        # Credits tab.
        credits_text = open('%s/AUTHORS' % main.path).read()
        credits = self.textviewer(credits_text)
        notebook.append_page(credits, gtk.Label(_('Credits')))

        # License tab.
        license_text = open('%s/COPYING-BRIEF' % main.path).read()
        license = self.textviewer(license_text)
        notebook.append_page(license, gtk.Label(_('License')))

        # Connect.
        self.dialog.connect('response', self.response)
        self.dialog.connect('destroy', lambda x: self.quit())

        # Buttons (auto-connected by response).
        self.dialog.add_button('gtk-close', 1)

        # Show.
        self.dialog.show_all()


    def textviewer(self, text):
        """Generate a text view with special rules to show credits and license.
        @text: The textview content as string.
        =return: A gtk.ScrolledWindow."""

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        view = gtk.TextView()
        view.set_editable(False)
        view.set_cursor_visible(False)
        view.set_left_margin(8)
        view.set_wrap_mode(gtk.WRAP_WORD)
        tbuffer = view.get_buffer()
        tbuffer.set_text(text)
        scroll.add_with_viewport(view)

        return scroll


    def response(self, widget, response):
        """Response (buttons) callbacks.
        @widget: Call widget.
        @response: Response int."""

        if response == 1: self.quit()


    def quit(self):
        """To do when the dialog is closed."""

        self.dialog.hide()
        self.dialog.destroy()
