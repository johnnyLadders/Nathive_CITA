#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import ConfigParser


class Presets(object):

    def __init__(self):

        self.main_dir = os.path.join(main.cfgpath, 'presets')


    def get_plugin_path(self, plugin_name):

        names = self.get_plugin_names()

        # Create preset folder if not exists.
        if plugin_name not in names:
            if plugin_name in main.plugins.childs:
                newfolder = os.path.join(self.main_dir, plugin_name)
                os.mkdir(newfolder)
                names = self.get_plugin_names()

        index = names.index(plugin_name)
        paths = self.get_plugin_paths()
        path = paths[index]
        return path


    def get_plugin_paths(self):

        tails = os.listdir(self.main_dir)
        paths = [os.path.join(self.main_dir, x) for x in tails]
        return [x for x in paths if os.path.isdir(x)]


    def get_plugin_names(self):

        paths = self.get_plugin_paths()
        return [os.path.split(x)[1] for x in paths]


    def get_preset_names(self, plugin_name):

        plugin_path = self.get_plugin_path(plugin_name)
        preset_tails = os.listdir(plugin_path)
        preset_tails.sort()
        preset_names = [os.path.splitext(x)[0] for x in preset_tails]
        return preset_names


    def get_preset_parsers(self, plugin_name):

        plugin_path = self.get_plugin_path(plugin_name)
        names = self.get_preset_names(plugin_name)
        tails = ['%s.cfg' % x for x in names]
        parsers = []
        for tail in tails:
            name, ext = os.path.splitext(tail)
            preset_path = os.path.join(plugin_path, tail)
            parser = ConfigParser.RawConfigParser()
            parser.read(preset_path)
            parsers.append(parser)
        return parsers


    def rename_preset(self, plugin_name, preset_name, newname):

        plugin_folder = os.path.join(self.main_dir, plugin_name)
        oldpath = os.path.join(plugin_folder, preset_name) + '.cfg'
        newpath = os.path.join(plugin_folder, newname) + '.cfg'
        os.rename(oldpath, newpath)


    def save_preset(self, plugin_name):

        # Create a new parser and set it with plugin attributes.
        parser = ConfigParser.RawConfigParser()
        parser.add_section('preset')
        plugin = main.plugins.childs[plugin_name]
        attributes = main.config.valid_attributes(plugin)
        for attribute, value in attributes.items():
            parser.set('preset', attribute, value)

        # Save parser to cfg file.
        folder = self.get_plugin_path(plugin_name)
        path = os.path.join(folder, ' .cfg')
        fileobj = open(path, 'w')
        parser.write(fileobj)
        fileobj.close()
