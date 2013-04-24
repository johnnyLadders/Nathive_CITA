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
from nathive.gui.multiwidget import *
from nathive.gui import utils as gutils


class Preferences(PluginDialog):

    def __init__(self):

        # Subclass it.
        PluginDialog.__init__(self)

        # Common attributes.
        self.name = 'preferences'
        self.author = 'nathive-dev'
        self.menu = 'edit'
        self.label = _('Preferences')
        self.icon = 'gtk-preferences'


    def callback(self):
        """To do when the plugin is called."""

        # Create dialog.
        self.dialog = gtk.Dialog(self.label)
        self.dialog.set_modal(True)
        self.dialog.set_size_request(300, 400)
        notebook = gtk.Notebook()
        notebook.set_border_width(5)
        self.dialog.vbox.pack_start(notebook)

        # General tab.
        general = gtk.VBox(False, 5)
        general.set_border_width(10)
        notebook.append_page(general, gtk.Label(_('General')))
        self.language_combo(general)
        self.tabmaxlen_spin(general)

        # Menus tab.
        arrange = gtk.VBox(False, 5)
        arrange.set_border_width(10)
        notebook.append_page(arrange, gtk.Label(_('Arrange')))
        self.arrange_group = 'headbar'
        self.arrange_gui(arrange)
        self.arrange_dump()

        # Menus plugins.
        plugins = gtk.VBox(False, 5)
        notebook.append_page(plugins, gtk.Label(_('Plugins')))

        # Connect.
        self.dialog.connect('response', self.response)
        self.dialog.connect('destroy', lambda x: self.quit())

        # Buttons (auto-connected by response).
        self.dialog.add_button('gtk-close', 1)

        # Show.
        self.dialog.show_all()


    def language_combo(self, parent):

        current = main.config.get('misc', 'language')
        languages = os.listdir(main.potpath)
        languages.sort()
        languages = [x.replace('.po', '') for x in languages]
        options = [_('Automatic')]
        options += [x.upper() for x in languages]
        languages.insert(0, 'auto')

        if current == 'auto': index = 0
        else: index = languages.index(current)

        guiitem = MultiWidgetCombo(
            parent,
            _('Language'),
            options,
            index,
            lambda x: main.config.set('misc', 'language', languages[x]))


    def tabmaxlen_spin(self, parent):

        current = main.config.get('misc', 'tabmaxlen')
        guiitem = MultiWidgetSpin(
            parent,
            _('Tab max length'),
            False,
            10.0,
            100.0,
            float(current),
            lambda x: main.config.set('misc', 'tabmaxlen', int(x)))
        guiitem.connect_extra(main.gui.tabs.update_all_titles)


    def set_arrange_group_from_index(self, index):

        groups = ['headbar', 'toolbar']
        groups += ['menufile', 'menuedit', 'menuview', 'menuhelp']
        self.arrange_group = groups[index]
        self.arrange_dump()


    def arrange_gui(self, parent):

        # Selection of menu/bar to sort.
        sortables = []
        sortables.append(_('Headbar'))
        sortables.append(_('Toolbar'))
        sortables.append(_('File'))
        sortables.append(_('Edit'))
        sortables.append(_('View'))
        sortables.append(_('Help'))
        MultiWidgetCombo(
            parent,
            _('Sort group'),
            sortables,
            0,
            lambda x: self.set_arrange_group_from_index(x))

        # Treeview.
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.treeview = gtk.TreeView()
        self.treeview.set_headers_visible(False)
        self.treeview.set_reorderable(True)
        render_pix = gtk.CellRendererPixbuf()
        render_txt = gtk.CellRendererText()
        pix_column = gtk.TreeViewColumn(
            None,
            render_pix,
            icon_name=0,
            stock_id=1,
            stock_size=2,
            pixbuf=3)
        txt_column = gtk.TreeViewColumn(
            None,
            render_txt,
            text=4)
        self.treeview.append_column(pix_column)
        self.treeview.append_column(txt_column)
        scroll.add_with_viewport(self.treeview)
        parent.pack_start(scroll, True, True)

        # Action buttons.
        buttons = [
            ('gtk-go-up', None, self.arrange_up),
            ('gtk-go-down', None, self.arrange_down),
            ('gtk-remove', None, self.arrange_remove),
            ('gtk-add', None, self.arrange_add),
            ('gtk-clear', None, self.arrange_default)]
        MultiWidgetButtons(parent, False, buttons)


    def arrange_dump(self, index=None):

        # Get sort from config.
        self.sort = main.config.get('sort', self.arrange_group).split(',')

        # Reset the tree store list.
        self.store = gtk.ListStore(str, str, int, gtk.gdk.Pixbuf, str)
        self.treeview.set_model(self.store)
        self.store.connect('row-inserted', self.arrange_inserted_cb)
        self.store.connect('row-deleted', self.arrange_deleted_cb)

        # Dump items to treeview.
        self.iters = []
        for item in self.sort:

            # Get icon from plugin.
            icon = stock = pixbuf = None
            plugin = main.plugins.get_plugin(item)
            icon = plugin.icon if plugin else None

            # Switch between stock icon, themed icon, or pixbuf icon.
            if icon and icon.startswith('gtk-'):
                stock = icon
                icon = None
            if icon and icon.endswith('.png'):
                icon = None
                stock = None
                pixbuf_path = os.path.join(main.imgpath, plugin.icon)
                pixbuf = gtk.gdk.pixbuf_new_from_file(pixbuf_path)
                pixbuf = pixbuf.scale_simple(24, 24, 2)
            if plugin and plugin.type == 'toggle':
                stock = 'gtk-disconnect'

            # Set item name.
            item = item.replace('-', ' ')
            item = item.capitalize()
            if item == '[s]': item = '(%s)' % _('Separator')
            if item == '[n]': item = '(%s)' % _('New items')

            # Append icon and name to row, store iter.
            rowiter = self.store.append([icon, stock, 3, pixbuf, item])
            self.iters.append(rowiter)

        # If index is given, select it.
        if type(index) is int:
            selection = self.treeview.get_selection()
            selection.select_iter(self.iters[index])


    def get_arrange_index(self):

        selection = self.treeview.get_selection()
        treeview, path = selection.get_selected_rows()
        if not path: return None
        return path[0][0]


    def arrange_inserted_cb(self, treeview, path, itr):

        self.arrange_last_inserted = path[0]


    def arrange_deleted_cb(self, treeview, path):

        a = path[0]
        b = self.arrange_last_inserted
        if a < b: b -= 1
        if a > b: a -= 1
        self.arrange_move(a, b)


    def arrange_move(self, a, b):

        item = self.sort[a]
        self.sort.pop(a)
        self.sort.insert(b, item)
        sort = ','.join(self.sort)
        main.config.set('sort', self.arrange_group, sort)
        self.arrange_refresh(b)


    def arrange_up(self):

        index = self.get_arrange_index()
        if type(index) is not int: return
        newindex = index - 1 if index > 0 else 0
        self.arrange_move(index, newindex)


    def arrange_down(self):

        index = self.get_arrange_index()
        if type(index) is not int: return
        length = len(self.sort) - 1
        newindex = index + 1 if index < length else length
        self.arrange_move(index, newindex)


    def arrange_add(self):

        # Create menu, alias group.
        menu = gtk.Menu()
        group = self.arrange_group

        # Append separator item to popup.
        if group != 'toolbar':
            menuitem = gtk.MenuItem(_('Separator'), False)
            menuitem.show()
            menu.append(menuitem)
            menuitem.connect(
                'activate',
                lambda x, y='[S]': self.arrange_add_item(y))

        # Iterate over all plugins.
        for plugin in main.plugins.childs.values():

            # Filter available plugins for each group.
            if plugin.name in self.sort: continue
            if group == 'headbar' and plugin.type == 'tool': continue
            if group == 'toolbar' and plugin.type != 'tool': continue
            if group.startswith('menu') and not plugin.menu: continue
            if plugin.menu and not group.endswith(plugin.menu): continue

            # Append each valid plugin to add popup.
            name = plugin.name.replace('-', ' ')
            name = name.capitalize()
            menuitem = gtk.MenuItem(name, False)
            menuitem.show()
            menu.append(menuitem)
            menuitem.connect(
                'activate',
                lambda x, y=plugin.name: self.arrange_add_item(y))

        # Popup the menu.
        menu.popup(None, None, None, 1, 0)


    def arrange_add_item(self, name):

        index = self.get_arrange_index()
        self.sort.append(name)
        sort = ','.join(self.sort)
        main.config.set('sort', self.arrange_group, sort)
        length = len(self.sort) - 1
        self.arrange_refresh(length)


    def arrange_remove(self):

        index = self.get_arrange_index()
        if type(index) is not int: return
        if self.sort[index] == '[N]': return
        self.sort.pop(index)
        sort = ','.join(self.sort)
        main.config.set('sort', self.arrange_group, sort)
        self.arrange_refresh()


    def arrange_default(self):

        sort = main.config.cfgdef.get('sort', self.arrange_group)
        main.config.set('sort', self.arrange_group, sort)
        self.arrange_refresh()


    def arrange_refresh(self, index=None):

        self.arrange_dump(index)
        if self.arrange_group == 'headbar': main.gui.headbar.dump()
        if self.arrange_group == 'toolbar': main.gui.toolbar.dump()
        if self.arrange_group == 'menufile': main.gui.menubar.file.dump()
        if self.arrange_group == 'menuedit': main.gui.menubar.edit.dump()
        if self.arrange_group == 'menuview': main.gui.menubar.view.dump()
        if self.arrange_group == 'menuhelp': main.gui.menubar.help.dump()


    def response(self, widget, response):
        """Response (buttons) callbacks.
        @widget: Call widget.
        @response: Response int."""

        if response == 1: self.quit()


    def quit(self):
        """To do when the dialog is closed."""

        self.dialog.hide()
        self.dialog.destroy()
