#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk


class Statusbar(object):
    """Define statusbar instance."""

    def __init__(self, box):
        """Create statusbar.
        @box: Parent widget."""

        self.statusbar = gtk.Statusbar()
        box.pack_start(self.statusbar, False, False, 0)
        self.statusbar.show_all()


    def update(self, x=0 ,y=0):

        message = ' %s x %s %s  ·  %s%%  ·  x%s  y%s' % (
            main.documents.active.width,
            main.documents.active.height,
            _('Pixels'),
            int(main.documents.active.canvas.sandbox.factor * 100),
            x,
            y)

        self.statusbar.pop(1)
        self.statusbar.push(1, message)
