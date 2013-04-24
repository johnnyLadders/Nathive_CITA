#!/usr/bin/env python
#coding=utf-8

# Nathive, The Usable Image Editor.
# Copyright (C) 2008-2010 Marcos Diaz Mencia <http://www.nathive.org/>.
#
# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import ctypes
import optparse
import shutil
import ConfigParser
import __builtin__

from nathive.lib.log import Log
from nathive.lib.config import Config
from nathive.lib.language import Language
from nathive.lib.color import Color
from nathive.lib.documents import Documents
from nathive.lib.clipboard import Clipboard
from nathive.lib.presets import Presets
from nathive.lib.plugins import Plugins
from nathive.lib.shortcuts import Shortcuts
from nathive.gui.main import Main as GuiMain


class Main:

    def main(self):

        # Change process name (only Linux).
        try:
            libc6 = ctypes.CDLL('libc.so.6')
            libc6.prctl(15, 'nathive\0', 0, 0, 0)
        except: pass

        # Get command line arguments and options.
        optparser = optparse.OptionParser()
        optparser.add_option(
            '-d',
            '--debug',
            dest="debug",
            action='store_true',
            help="enable debug log")
        self.options, self.args = optparser.parse_args()

        # Set meta variables.
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.home = os.path.expanduser('~')
        metapath = os.path.join(self.path, 'META')
        meta = ConfigParser.RawConfigParser()
        meta.read(metapath)
        self.version = meta.get('meta', 'version')
        self.phase = meta.get('meta', 'phase')
        appdir = meta.get('meta', 'appdir')

        # Set execution level.
        if self.path == appdir: self.level = 'installed'
        else: self.level = 'standalone'

        # Set contents paths.
        self.imgpath = os.path.join(self.path, 'img')
        self.cfgpath = os.path.join(self.path, 'cfg')
        self.potpath = os.path.join(self.path, 'po')
        self.palpath = os.path.join(self.path, 'palettes')
        if self.level == 'installed':
            self.cfgpath = os.path.join(self.home, '.nathive/cfg')
            self.userpalpath = os.path.join(self.home, '.nathive/palettes')
            self.userplgpath = os.path.join(self.home, '.nathive/plugins')

        # Set user space and subfolders.
        if self.level == 'installed':
            paths = [self.cfgpath, self.userpalpath, self.userplgpath]
            for path in paths:
                if not os.path.exists(path):
                    os.makedirs(path)

        # Copy cfg files to user space.
        if self.level == 'installed':
            sharedpath = os.path.join(self.path, 'cfg')
            for path, dirs, files in os.walk(sharedpath):
                for filename in files:
                    filepath = os.path.join(path, filename)
                    filepath_relative = filepath.replace(sharedpath, '')
                    filepath_relative = filepath_relative.strip('/')
                    mustpath = os.path.join(self.cfgpath, filepath_relative)
                    if not os.path.exists(mustpath):
                        mustdir = os.path.dirname(mustpath)
                        if not os.path.exists(mustdir): os.makedirs(mustdir)
                        shutil.copyfile(filepath, mustpath)

        # Overwrite default config in user space.
        if self.level == 'installed':
            default_source = os.path.join(sharedpath, 'default.cfg')
            default_dest = os.path.join(self.cfgpath, 'default.cfg')
            shutil.copyfile(default_source, default_dest)

        # Load logging system.
        self.log = Log()
        self.log.info('loading main: %s/' % self.path)

        # Load modules.
        self.config = Config()
        self.language = Language()
        __builtin__._ = self.language.gettext
        self.color = Color()
        self.documents = Documents()
        self.clipboard = Clipboard()
        self.presets = Presets()
        self.plugins = Plugins()
        self.shortcuts = Shortcuts()
        self.gui = GuiMain()
        self.gui.interface()

        # Open command line requested paths.
        for path in self.args:
            main.documents.new_from_path(path)

        # Start event listener.
        self.gui.loop()


if __name__ == "__main__":

    __builtin__.main = Main()
    main.main()
