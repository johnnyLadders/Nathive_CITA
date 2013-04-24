#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gobject
import gtk

from nathive.gui import utils as gutils


class SidebarLayers(object):

    def __init__(self):

        # Allow debug tracking.
        main.log.allow_tracking(self)

        # Parent box for the following widgets.
        self.box = gtk.VBox(False, 0)
        self.box.set_border_width(10)

        # Layers tree.
        self.treeview = gtk.TreeView()
        self.treeview.set_headers_visible(False)
        self.treeview.set_reorderable(True)
        self.box.pack_start(self.treeview, True, True)
        render_txt = gtk.CellRendererText()
        render_txt.set_property('editable', True)
        render_txt.connect('edited', lambda x,y,z: self.edited(y, z))
        render_pix = gtk.CellRendererPixbuf()
        column_txt = gtk.TreeViewColumn(
            None,
            render_txt,
            text=0)
        column_pix = gtk.TreeViewColumn(
            None,
            render_pix,
            stock_id=1,
            stock_size=2)
        self.treeview.append_column(column_pix)
        self.treeview.append_column(column_txt)

        # Break.
        gutils.separator(self.box)

        # Bottom buttons.
        grid = gtk.HBox(True, 0)
        self.box.pack_start(grid, False, False)

        # Set buttons properties.
        buttons = []
        layers = lambda: main.documents.active.layers
        buttons.append(['gtk-new', lambda x=layers: x().append_blank_tracked()])
        buttons.append(['gtk-copy', lambda x=layers: x().duplicate_active()])
        buttons.append(['gtk-go-up', lambda x=layers: x().swap_up_active()])
        buttons.append(['gtk-go-down', lambda x=layers: x().swap_down_active()])
        buttons.append(['gtk-delete', lambda x=layers: x().remove_active()])

        # Create buttons.
        for icon, callback in buttons:
            image = gtk.image_new_from_stock(icon, 1)
            button = gtk.Button()
            button.set_image(image)
            button.set_relief(gtk.RELIEF_NONE)
            button.connect('clicked', lambda x,y=callback: y())
            grid.pack_start(button, True, True)


    def dump(self):

        # Alias.
        layers = main.documents.active.layers

        # Flag to avoid update feedback.
        self.locked = True

        # Reset the tree store list.
        self.store = gtk.ListStore(str, str, int)
        self.store.connect('row-inserted', self.inserted_cb)
        self.store.connect('row-deleted', self.deleted_cb)
        self.treeview.set_model(self.store)

        # List of tree nodes.
        self.iters = []

        # Stop here if the document has no layers.
        if not main.documents.active.layers.active: return

        # Dump each layer as tree node.
        for layer in reversed(layers.childs):
            rowiter = self.store.append([layer.name, 'gtk-missing-image', 5])
            self.iters.append(rowiter)

        # Set tree selection from active layer.
        self.selection = self.treeview.get_selection()
        active_layer_index = layers.childs.index(layers.active)
        active_layer_revindex = len(layers.childs) - active_layer_index - 1
        self.selection.select_iter(self.iters[active_layer_revindex])

        # Connect the selection callback.
        self.treeview.connect('cursor-changed', lambda x: self.changed())

        # Disable feedback lock.
        self.locked = False


    def changed(self):

        if self.locked: return
        layers = main.documents.active.layers

        (treeview, path) = self.selection.get_selected_rows()
        if path:
            index = path[0][0]
            revindex = len(layers.childs) - index - 1
            if revindex != layers.childs.index(layers.active):
                layers.set_active_from_index(revindex)


    def edited(self, index, newtext):

        layers = main.documents.active.layers
        revindex = len(layers.childs) - int(index) - 1
        layer = layers.get_layer_from_index(revindex)
        layer.name = newtext
        self.dump()


    def inserted_cb(self, treeview, path, itr):

        self.last_inserted = path[0]


    def deleted_cb(self, treeview, path):

        a = path[0]
        b = self.last_inserted
        if a < b: b -= 1
        if a > b: a -= 1
        self.move(a, b)


    def move(self, a, b):

        layers = main.documents.active.layers
        count = len(layers.childs)
        a = count - a - 1
        b = count - b - 1
        item = layers.childs[a]
        layers.childs.pop(a)
        layers.childs.insert(b, item)
        layers.set_active(item)
        self.dump()
