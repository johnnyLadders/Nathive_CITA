#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os


class Plugins(object):
    """The plugin manager in app core (not the user plugin manager), it loads
    and stores plugins at program start and also set/get active tool.
    ⌥: Main > Plugins."""

    def __init__(self):

        main.log.info('loading plugins')

        self.childs = {}
        self.activetool = None
        paths = os.listdir('%s/nathive/plugins' % main.path)

        for path in paths:

            name, ext = os.path.splitext(path)
            if name.startswith('__'): continue
            if ext != '.py': continue

            plug = __import__('nathive.plugins', fromlist=[name])
            plug = getattr(plug, name)
            plug_class = name.split('-')
            plug_class = [x.capitalize() for x in plug_class]
            plug_class = ''.join(plug_class)
            plug_instance = getattr(plug, plug_class)
            self.childs[name] = plug_instance()

        toolsort = main.config.get('sort', 'toolbar').split(',')
        self.activetool = self.get_plugin(toolsort[0])


    def get_plugin(self, name):

        if name in self.childs:	return self.childs[name]
        else: return None


    def set_active_tool(self, toolname):

        tool = self.get_plugin(toolname)
        if tool == self.activetool: return
        oldtool = self.activetool
        self.activetool = tool
        if main.documents.active:
            if hasattr(self.activetool, 'disable'): oldtool.disable()
            tool.enable()
