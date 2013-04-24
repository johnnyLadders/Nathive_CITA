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


class Tabs(object):
    """The document notebook handler, manage all GUI operations in the notebook
    as add, reorder or delete tabs, manage its titles too, but never the tabs
    content widgets.
    ⌥: Main > Gui > Tabs."""

    def __init__(self, parent):
        """Create notebook at program start.
        @parent: Parent widget."""

        # Create notebook.
        self.notebook = gtk.Notebook()
        self.notebook.set_scrollable(True)
        parent.pack_start(self.notebook, True, True, 0)

        # Connect notebook.
        self.notebook.connect('switch-page', self.switched)
        self.notebook.connect('page-reordered', self.reordered)

        # Show.
        self.notebook.show_all()


    def switched(self, widget, child, index):
        """Callback function when a tab is selected.
        @widget: Call widget.
        @child: Widget contained in selected tab.
        @index: Int index of selected tab."""

        main.documents.set_active_from_index(index)
        main.gui.sidebar.layers.dump()
        main.gui.statusbar.update()


    def reordered(self, widget, child, index):
        """Callback function when a tab is reordered,
        @widget: all widget.
        @child: unused widget contained in selected tab.
        @index: Int index of selected tab."""

        # Search for tab child in the document list.
        for document in main.documents.childs:
            if child is document.canvas.table:

                # Reorder document list like the notebook widget.
                main.documents.childs.remove(document)
                main.documents.childs.insert(index, document)


    def update_title(self, document):
        """Update the tab title.
        @document: The document instance related with the tab."""

        # Define the new title.
        title = document.path
        title = os.path.basename(title)
        title = self.short_title(title)

        # Get the actual label widget in the tab.
        label = self.notebook.get_tab_label(document.canvas.table)
        label = label.get_children()[0]

        # Replace the tab title and tooltip.
        label.set_text(title)
        label.set_tooltip_text(document.path)


    def update_all_titles(self):
        """Update all tab titles."""

        for document in main.documents.childs:
            self.update_title(document)


    def short_title(self, title):
        """Return a shortest version for tab title based on config rule.
        @title: The title string to short.
        =return: A shortest version of title or the same if not exceed."""

        maxlength = main.config.getint('misc', 'tabmaxlen')
        half = maxlength / 2
        if len(title) > maxlength:
            title = '%s...%s' % (title[:half], title[-half:])
        return title


    def append(self, document):
        """Append the given document as a new tab in the notebook.
        @document: A document instance to append."""

        # Set tab title, short if is too large.
        if document.path:
            title = os.path.basename(document.path)
            title = self.short_title(title)
        else:
            title = '%s %s' % (_('Unsaved'), main.documents.unsaved)

        # Set label widget.
        label = gtk.Label(title)
        label.set_tooltip_text(document.path)
        label.set_padding(4, 0)

        # Set image box, by this way expand parameter is tuned.
        button_box = gtk.HBox(False, 0)
        button_img = gtk.image_new_from_stock('gtk-close', 1)
        button_box.pack_start(button_img, True, False, 0)

        # Set button widget.
        button = gtk.Button()
        button.add(button_box)
        button.set_relief(gtk.RELIEF_NONE)
        button.set_focus_on_click(False)
        button.connect("clicked", lambda w: main.documents.close(document))
        button.set_name('thick')

        # Set button internal padding to zero.
        gtk.rc_parse_string('\
            style "thick"\
            {\
                xthickness = 0\
                ythickness = 0\
            }\
            widget "*.thick" style "thick"')

        # Adjust button size.
        settings = button.get_settings()
        (w,h) = gtk.icon_size_lookup_for_settings(settings, 1)
        button.set_size_request(w+4, h+4)

        # Add all to tab box.
        hbox = gtk.HBox(False, 3)
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(button, False, False, 0)
        hbox.show_all()

        # Append to notebook and select the new tab.
        self.notebook.append_page(document.canvas.table, hbox)
        self.notebook.set_tab_reorderable(document.canvas.table, True)
        self.notebook.set_current_page(-1)
