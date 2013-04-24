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


class Config(object):
    """Load, get, and save config rules based on INI files."""

    def __init__(self):
        """Set config path and load it."""

        # Set config paths.
        user = '%s/user.cfg' % main.cfgpath
        default = '%s/default.cfg' % main.cfgpath

        # Test what path must be loaded.
        cfg_path = False
        if os.path.exists(user): cfg_path = user
        if not cfg_path: cfg_path = default

        # Print log info.
        main.log.info('loading cfg: %s' % cfg_path)

        # Load config.
        self.cfg = ConfigParser.RawConfigParser()
        self.cfg.read(cfg_path)

        # Load default config for missed rules.
        self.cfgdef = ConfigParser.RawConfigParser()
        self.cfgdef.read(default)


    def valid_attributes(self, plugin):
        """Search all valid (config-able) attributes into instance.
        @plugin: Plugin instance.
        =return: String list with attribute names."""

        # Getting attribute names from plugin.
        attributes = dict(plugin.__dict__)

        # Rules for valid cfg values.
        blacklist = ['name', 'author', 'type', 'menu', 'label', 'icon']
        whitelist = [str, int, float]

        # Filtering attributes.
        for (name, attribute) in attributes.items():
            if name in blacklist: attributes.pop(name)
            elif type(attribute) not in whitelist: attributes.pop(name)

        # Return attribute list.
        return attributes


    def push_from_plugin(self, plugin):

        # Get valid attributes.
        attributes = self.valid_attributes(plugin)

        # Setting valid attributes into config.
        for (name, attribute) in attributes.items():
            self.set(plugin.name, name, str(attribute))


    def push_from_all_plugins(self):

        for plugin in main.plugins.childs.values():
            self.push_from_plugin(plugin)


    def push_to_plugin(self, plugin):

        # Get valid attributes.
        attributes = self.valid_attributes(plugin)

        # Setting valid attributes into config.
        for (name, attribute) in attributes.items():
            if self.cfg.has_option(plugin.name, name):
                value = self.get(plugin.name, name)
                try:
                    if '.' in value: value = float(value)
                    else: value = int(value)
                except: pass
                setattr(plugin, name, value)


    def save(self):
        """Export current config to hard-drive"""

        self.push_from_all_plugins()

        path = os.path.join(main.cfgpath, 'user.cfg')
        main.log.info('saving cfg: %s' % path.replace(main.home, '~'))

        data = ''
        sections = sorted(self.cfg._sections)
        for section in sections:
            data += '[%s]\n' % section
            options = sorted(self.cfg._sections[section])
            for option in options:
                if option == '__name__': continue
                value = self.cfg._sections[section][option]
                data += '%s = %s\n' % (option, value)
            data += '\n'

        fileobj = open(path, 'w').write(data)


    def get(self, section, option):
        """Get a string from config rule.
        @section: Config rule group.
        @option: Config rule name."""

        try: return self.cfg.get(section, option)
        except: return self.cfgdef.get(section, option)


    def getint(self, section, option):
        """Get an int from config rule.
        @section: Config rule group.
        @option: Config rule name."""

        return int(self.get(section, option))


    def set(self, section, option, value):
        """Set an string in config rule.
        @section: Config rule group.
        @option: Config rule name.
        @value: New value to set."""

        if not self.cfg.has_section(section): self.cfg.add_section(section)
        self.cfg.set(section, option, value)


    def options(self, section):

        """Returns a list of options available in the specified section.
        @section: Config rule group."""

        try: return self.cfg.options(section)
        except: return self.cfgdef.options(section)
