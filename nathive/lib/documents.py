#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os

from nathive.lib.document import Document


class Documents(object):
    """Management for documents, is the container for document object.
    ⌥: Main > Documents."""

    def __init__(self):
        """Create the documents management object at program start."""

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Attributes.
        self.childs = []                             # Opened document objects.
        self.active = None                          # Selected document object.
        self.unsaved = 1                          # Count of unsaved documents.


    def set_active(self, active):

        if active == self.active: return
        if self.active: main.plugins.activetool.disable()
        self.active = active
        if self.active: main.plugins.activetool.enable()


    def set_active_from_index(self, index):

        document = self.childs[index]
        self.set_active(document)


    def new_from_path(self, path):
        """Open a document instance and make related.
        @path: Image path."""

        # Create new document, append to list, tag as selected.
        main.log.info('opening doc: %s' % path)
        document = Document(path)
        self.childs.append(document)
        self.set_active(document)

        # Update sidebar layer list, show new tab.
        main.gui.sidebar.layers.dump()
        main.gui.tabs.append(document)


    def new_blank(self, width, height):

        main.log.info('creating doc: unsaved %s' % main.documents.unsaved)

        document = Document(None, width, height)
        self.childs.append(document)
        self.set_active(document)
        main.gui.tabs.append(document)
        main.gui.sidebar.layers.dump()

        self.unsaved += 1


    def close(self, document):
        """Close a document, remove related,
        instance should be automatically destroyed.
        @document: Document instance."""

        # Previous stuff.
        main.log.info('closing doc: %s' % document.path)
        notebook = main.gui.tabs.notebook

        # Remove page/tab from notebook.
        page = notebook.page_num(document.canvas.table)
        notebook.remove_page(page)

        # Remove document from document list.
        self.childs.remove(document)

        # Update current selected document.
        current = notebook.get_current_page()
        if current != -1: self.set_active_from_index(current)
        else: self.set_active(None)

        # Delete circular references and uncollectable garbage like Canvas,
        # which cannot be totally freezed since is ref by gobject connects.
        del document.layers
        del document.actions
        del document.canvas.document
        del document.canvas.sandbox
