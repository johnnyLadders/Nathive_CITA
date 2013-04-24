#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


from nathive.lib.action.layercontent import *
from nathive.lib.action.layermove import *
from nathive.lib.action.layermodify import *
from nathive.lib.action.layerremove import *
from nathive.lib.action.layercreate import *
from nathive.lib.action.docresize import *


class Actions(object):

    def __init__(self, document):

        # Allow debug tracking.
        main.log.allow_tracking(self)

        self.document = document
        self.action = None
        self.history = []
        self.rehistory = []


    def begin(self, actionname):

        layer = self.document.layers.active
        document = self.document

        actions = [
            ('layer-move', ActionLayerMove, layer),
            ('layer-content', ActionLayerContent, layer),
            ('layer-modify', ActionLayerModify, layer),
            ('layer-remove', ActionLayerRemove, layer),
            ('layer-create', ActionLayerCreate, layer),
            ('doc-resize', ActionDocResize, document)]

        for name, action, param in actions:
            if name == actionname:
                self.action = action(param)
                return

        raise Exception('Unknown action name %s' % actionname)


    def end(self, parameter=None):

        if not self.action: return
        if not parameter: self.action.final()
        else: self.action.final(parameter)
        self.history.append(self.action)
        self.rehistory = []
        self.action = None
        main.plugins.get_plugin('undo').update_sensitive()
        main.plugins.get_plugin('redo').update_sensitive()


    def undo(self):

        if self.action: self.end()          # Force incompleted actions to end.
        if not self.history: return
        action = self.history[-1]
        action.restore()
        self.history.pop()
        self.rehistory.append(action)


    def redo(self):

        if not self.rehistory: return
        action = self.rehistory[-1]
        action.unrestore()
        self.rehistory.pop()
        self.history.append(action)


    def get_bytes(self):

        bytes = 0
        for action in self.history: bytes += action.bytes
        for action in self.rehistory: bytes += action.bytes
        return bytes
